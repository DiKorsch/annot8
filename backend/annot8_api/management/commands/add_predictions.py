from __future__ import annotations

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

import PIL.ExifTags
import datetime as dt
import json
import logging
import numpy as np
import typing as T
import yaml

from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from django.core.management.base import BaseCommand
from functools import partial
from labeltree.models import label
from matplotlib import pyplot as plt
from pathlib import Path
from scipy.optimize import linear_sum_assignment
from tqdm.auto import tqdm

from PIL import Image

@dataclass
class CostWeights:
    area: float = .15
    distance: float = .65
    feature: float = .1
    iou: float = .1

@dataclass
class Box:
    idx: int
    path: str = field(repr=False)
    box: dict = field(repr=False)

    x: float = None
    y: float = None
    w: float = None
    h: float = None

    def __post_init__(self):
        self.x = self.box["x"]
        self.y = self.box["y"]
        self.w = self.box["w"]
        self.h = self.box["h"]

        delattr(self, "box")

        self.path = Path(self.path)

    def costs(self, other: Box,
        features: np.ndarray = None,
        weights: CostWeights = CostWeights(0.25, 0.65, 0.1)
        ) -> float:
        costs = []

        a0, a1 = self.area, other.area
        area_ratio = min(a0, a1) / max(a0, a1)
        area_cost = (1 - area_ratio)
        costs.append(area_cost *  weights.area)

        (cx0, cy0), (cx1, cy1) = self.center, other.center
        distance_cost = np.sqrt((cx0 - cx1)**2 + (cy0 - cy1)**2) / np.sqrt(2)
        costs.append(distance_cost * weights.distance)

        if features is None:
            features_cost = distance_cost + area_cost
        else:
            feat0, feat1 = features[self.idx], features[other.idx]
            features_cost = 1 - (feat0 @ feat1.T / (np.linalg.norm(feat0) * np.linalg.norm(feat1)))
        costs.append(features_cost * weights.feature)


        iou_cost = 1-self.iou(other)
        # if "7019" in str(self.path) and 0.74 < cy1 < 0.75 and 0.25 < cx1 < 0.26:
        #     import pdb; pdb.set_trace()
        costs.append(iou_cost * weights.iou)


        return sum(costs)

    def iou(self, other: Box) -> float:
        x00, y00 = self.x, self.y
        x01, y01 = other.x, other.y

        x10, y10 = self.x + self.w, self.y + self.h
        x11, y11 = other.x + other.w, other.y + other.h

        x_int, y_int = max(x00, x01), max(y00, y01)
        w_int, h_int = min(x10, x11) - x_int, min(y10, y11) - y_int
        w_int, h_int = max(w_int, 0), max(h_int, 0)

        intersect = Box(idx=-1, path="", box=dict(x=x_int, y=y_int, w=w_int, h=h_int))

        return intersect.area / (self.area + other.area - intersect.area)


    @property
    def area(self) -> float:
        return self.w * self.h

    @property
    def center(self) -> T.Tuple[float, float]:
        return self.x + self.w/2, self.y + self.h/2

    def get_crop(self):
        im = plt.imread(self.path)
        H,W,C = im.shape

        x0, y0 = int(self.x * W), int(self.y * H)
        x1, y1 = int((self.x + self.w) * W), int((self.y + self.h) * H)

        return im[y0:y1, x0:x1]

@dataclass
class File:
    path: Path
    creation: dt.datetime = None


    def __post_init__(self):
        assert self.path.exists()
        img = Image.open(self.path)
        exif = {PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}

        FMT = "%Y:%m:%d %H:%M:%S"
        self.creation = dt.datetime.strptime(exif['DateTimeOriginal'], FMT)

    def __hash__(self):
        return hash(self.path)


def group_by_filename(boxes: T.List[Box]):
    groups = defaultdict(list)
    _look_up = {}
    for box in tqdm(boxes):
        path = Path(box.path)
        if path.name in _look_up:
            fobj = _look_up[path.name]
        else:
            fobj = File(path)
            _look_up[path.name] = fobj
        groups[fobj].append(box)

    return dict(groups)

def group_by_day(groups):
    result = defaultdict(list)
    for fobj, boxes in groups.items():
        day = (fobj.creation - dt.timedelta(hours=12)).date()
        result[day].append(dict(file=fobj, boxes=boxes))

    return dict(result)


def assign_boxes(boxes0, boxes1, features):
    costs = np.zeros((len(boxes0), len(boxes1)), dtype=np.float32)

    for i, box0 in enumerate(boxes0):
        for j, box1 in enumerate(boxes1):
            costs[i, j] = box0.costs(box1, features)

    return linear_sum_assignment(costs), costs


def concat_tracks(connections):

    tracks = []
    end2idx = {}
    for step, cons in enumerate(connections):
        for start, end in cons:
            prev_key = (step-1, start.idx)
            cur_key = (step, end.idx)

            if step > 0 and prev_key in end2idx:
                idx = end2idx[prev_key]
                track = tracks[idx]
                track.append(end)

                del end2idx[prev_key]
                end2idx[cur_key] = idx

            else:
                tracks.append([start, end])
                end2idx[cur_key] = len(tracks) - 1

    return tracks

def track_boxes(groups, features, cost_thresh: float = 0.1):
    result = {}
    for day, files in groups.items():
        files = sorted(files, key=lambda entry: entry["file"].creation)

        prev = files[0]
        connections = [[] for i in range(len(files) - 1)]
        for step, current in enumerate(files[1:]):
            (rows, cols), costs = assign_boxes(prev["boxes"], current["boxes"], features)


            for row, col in zip(rows, cols):
                cost = costs[row, col]
                if cost >= cost_thresh:
                    continue
                connection = prev["boxes"][row], current["boxes"][col]
                connections[step].append(connection)

            prev = current

        result[day] = dict(files=files, tracks=concat_tracks(connections))

    return result

def show_track(track, *, predictor = None):
    nrows = int(np.ceil(np.sqrt(len(track))))
    ncols = int(np.ceil(len(track) / nrows))

    fig, axs = plt.subplots(nrows, ncols, squeeze=False)
    [ax.axis("off") for ax in axs.ravel()]

    preds = []

    for i, box in enumerate(track):
        ax = axs[np.unravel_index(i, axs.shape)]
        crop = box.get_crop()

        ax.imshow(crop)
        center = box.center


        title = [
            f"{Path(box.path).name}",
            f"({center[0]:.3f}, {center[1]:.3f}), {box.area:.2%})",
        ]

        if predictor is not None:
            topKnames, topKpreds, logits = predictor(idx=box.idx)
            preds.append((topKnames, topKpreds, logits))
            title.append('\n'.join(topKnames))

        ax.set_title("\n".join(title))


    if len(preds):
        names, preds, logits = zip(*preds)
        names, preds = np.hstack(names), np.hstack(preds)
        logits = np.vstack(logits)

        pred2name = {pred: name for pred, name in zip(preds, names)}

        voted_preds = np.argsort(-np.bincount(preds))[:3]
        voted_names = [pred2name.get(pred, f"{pred} NOT FOUND") for pred in voted_preds]

        mean_preds = (-logits.mean(axis=0)).argsort()[:3]
        mean_names = [pred2name.get(pred, f"{pred} NOT FOUND") for pred in mean_preds]

        title = "\n".join([
            "Voted: " + ", ".join(voted_names),
            "Mean: " + ", ".join(mean_names),
        ])
        fig.suptitle(title)

    plt.tight_layout()
    plt.show()
    plt.close()

def plot_box(box, ax, size, box2trackId, colors, alpha: float = 1.0, *, predictor = None):
    H, W = size
    track_id = box2trackId.get(box.idx)
    col = None if track_id is None else colors[track_id]
    xy = (box.x * W, box.y * H)

    rect = plt.Rectangle(xy, box.w*W, box.h*H,
        fill=False, edgecolor=col)

    ax.add_patch(rect)
    text = None
    if track_id is not None and predictor is None:
        text = f"ID: {track_id}"

    elif None not in [track_id, predictor]:
        topKnames, *_ = predictor(idx=box.idx)
        topKnames = ', '.join(topKnames)
        text = f"ID: {track_id}\n[{topKnames}]"

    elif predictor is not None and track_id is None:
        topKnames, *_ = predictor(idx=box.idx)
        text = ', '.join(topKnames)

    if text is not None:
        ax.text(*xy, s=text, color=col)

def plot_boxes(boxes, ax, size, box2trackId, colors, prev_boxes = None, *, predictor = None):
    for box in boxes:
        plot_box(box, ax, size, box2trackId, colors, predictor=predictor)

        if prev_boxes is None:
            continue

        best_prev_box = prev_boxes[np.argmin([box.costs(b) for b in prev_boxes])]

        print(f"Track #{box2trackId.get(box.idx)}: {best_prev_box.idx} -> {box.idx}"\
            f" (costs: {box.costs(best_prev_box)})")


def show_tracks(result, *, predictor = None, by_tracks: bool = True):

    for day, files_and_tracks in result.items():
        tracks = files_and_tracks["tracks"]

        if by_tracks:
            max_tracks = 25
            for track in tracks:

                show_track(track if max_tracks is None else track[:max_tracks], predictor=predictor)

                plt.show()
                plt.close()

        else:
            files = sorted(files_and_tracks["files"], key=lambda entry: entry["file"].creation)
            colIds = np.linspace(0,1, len(tracks))
            np.random.shuffle(colIds)
            colors = plt.cm.rainbow(colIds)

            box2trackId = {box.idx: i for i, boxes in enumerate(tracks) for box in boxes }
            prev_boxes = None
            for fobj in files:
                fpath = Path(fobj["file"].path)
                im = plt.imread(fpath)
                fig, ax = plt.subplots()
                ax.imshow(im)
                ax.set_title(f"{fpath.name}")
                ax.axis("off")

                plot_boxes(fobj["boxes"], ax, im.shape[:-1], box2trackId,
                    colors=colors, prev_boxes=prev_boxes, predictor=predictor)
                prev_boxes = fobj["boxes"]
                plt.show()
                plt.close()


def get_predictions(preds, idx, labels, clsID_lookup, *, topk: int = 3):

    pred = preds[idx]
    topKpreds = (-pred).argsort()[:topk]
    topKcls_ids = list(map(clsID_lookup.get, topKpreds))

    # following line does not preserve the ordering,
    # so we have to create a mapping!
    topKnames = {lab.pk: lab.name for lab in labels.filter(pk__in=topKcls_ids)}
    topKnames = [topKnames.get(int(i)) for i in topKcls_ids]
    return topKnames, topKpreds, pred


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("boxes")
        parser.add_argument("predictions")
        parser.add_argument("features")
        parser.add_argument("class_names")

    def handle(self, *args, boxes, predictions, features, class_names, **kwargs):


        # paths = boxes, predictions # < in case one needs the paths
        logging.info("Loading class names...")
        with open(class_names) as f:
            id2cls_id = yaml.load(f, Loader=Loader)

        class_ids = [int(i) for i in id2cls_id.values()]

        labels = label.Label.objects.filter(pk__in=class_ids)

        if labels.count() != len(class_ids):
            found = {lab.id: lab.name for lab in labels}
            missing = [idx for idx in class_ids if idx not in found]
            raise ValueError("not all labels could be found in the database!"\
                f" {len(missing)} labels missing!\n" \
                + ("\n".join(map(str, missing))))

        logging.info("Loading boxes...")
        with open(boxes, "r") as f:
            boxes = [Box(**box) for box in json.load(f)[:10000]]

        file_groups = group_by_filename(boxes)
        day_groups = group_by_day(file_groups)

        logging.info("Loading features...")
        features = np.load(features)
        logging.info(f"Features loaded: {features.shape}...")

        tracks = track_boxes(day_groups, features)

        logging.info("Loading predictions...")
        predictions = np.load(predictions)

        show_tracks(tracks,
            predictor=partial(get_predictions,
                preds=predictions, labels=labels, clsID_lookup=id2cls_id))

        import pdb; pdb.set_trace()


        assert len(boxes) == len(predictions), \
            f"Lengths of boxes ({len(boxes)}) and predictions ({len(predictions)})"\
            "does not match!"

        assert len(class_ids) == predictions.shape[1], \
            f"Lengths of class names ({len(class_ids)}) and " \
            f"predictions ({predictions.shape}) does not match!"


        for box in tqdm(boxes):
            impath = box.path
            topKnames, topKpreds = get_predictions(predictions, box.idx, labels, id2cls_id)
            im = plt.imread(impath)
            h, w, c = im.shape
            x0, y0 = int(box.x * w), int(box.y * h)
            x1, y1 = x0 + int(box.w * w), y0 + int(box.h * h)
            crop = im[y0:y1, x0:x1]
            fig, ax = plt.subplots()

            ax.imshow(crop)
            ax.set_title(', '.join(topKnames)) #+ f"\n[{', '.join(map(str, topKpreds))}]")


            plt.show()
            plt.close()

