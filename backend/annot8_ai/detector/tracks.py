import re
import logging
import PIL.ExifTags
import datetime as dt
import numpy as np

from annot8_api import models as api_models

from PIL import Image
from dataclasses import dataclass
from pathlib import Path
from collections import defaultdict
from scipy.optimize import linear_sum_assignment


@dataclass
class CostWeights:
    area: float = .15
    distance: float = .65
    feature: float = .1
    iou: float = .1


def to_int(string) -> int:
    try:
        return int(string)
    except ValueError:
        return 0

def creation_date(file: "api_models.File",
                  FMT = "%Y:%m:%d %H:%M:%S",
                  regex = re.compile(r"(\d{4})[_-]?(\d{2})[_-]?(\d{2})[a-zA-Z-_]*(\d{2})(\d{2})(\d*)\..*")
                  ) -> dt.datetime:
    with Image.open(file.path.path) as img:
        try:
            exif = img._getexif()
            exif_data = {PIL.ExifTags.TAGS[k]: v for k, v in exif.items() if k in PIL.ExifTags.TAGS}
            if 'DateTimeOriginal' in exif_data:
                return dt.datetime.strptime(exif_data['DateTimeOriginal'], FMT)

        except AttributeError:
            logging.error(f"Could not extract creation date from EXIF data of {file.path}")
            fname = str(Path(file.path.path).name)
            match = regex.search(fname)
            if match:
                year, month, day, hour, minute, sequence = map(to_int, match.groups())
                # we just interpret the sequence number as microseconds
                return dt.datetime(year, month, day, hour, minute, microsecond=sequence)
            else:
                logging.error(f"Could not match {fname}. Using the creation date of the file!")
                return file.created

        except Exception as e:
            logging.error(f"Could not extract creation date from {file.path}: {e}")
            return file.created

def concat_tracks(connections):

    tracks = []
    end2idx = {}
    for step, cons in enumerate(connections):
        for start, end in cons:
            prev_key = (step-1, start.id)
            cur_key = (step, end.id)

            if step > 0 and prev_key in end2idx:
                idx = end2idx[prev_key]
                track = tracks[idx]
                track.append(end.id)

                del end2idx[prev_key]
                end2idx[cur_key] = idx

            else:
                tracks.append([start.id, end.id])
                end2idx[cur_key] = len(tracks) - 1

    return tracks

def iou(box0, box1) -> float:

    x00, y00 = box0.x, box0.y
    x01, y01 = box1.x, box1.y

    x10, y10 = box0.x + box0.width, box0.y + box0.height
    x11, y11 = box1.x + box1.width, box1.y + box1.height

    x_int, y_int = max(x00, x01), max(y00, y01)
    w_int, h_int = min(x10, x11) - x_int, min(y10, y11) - y_int
    w_int, h_int = max(w_int, 0), max(h_int, 0)

    intersect = api_models.BoundingBox(x=x_int, y=y_int, width=w_int, height=h_int)

    return intersect.area / (box0.area + box1.area - intersect.area)


def calc_costs(box0, box1, weights: CostWeights = CostWeights(0.25, 0.65, 0.1)) -> float:
    costs = []


    a0, a1 = box0.area, box1.area
    area_ratio = min(a0, a1) / max(a0, a1)
    area_cost = (1 - area_ratio)
    costs.append(area_cost *  weights.area)


    (cx0, cy0), (cx1, cy1) = box0.center, box1.center
    distance_cost = np.sqrt((cx0 - cx1)**2 + (cy0 - cy1)**2) / np.sqrt(2)
    costs.append(distance_cost * weights.distance)

    iou_cost = 1 - iou(box0, box1)
    costs.append(iou_cost * weights.iou)

    return sum(costs)

def assign_boxes(boxes0, boxes1):
    costs = np.zeros((len(boxes0), len(boxes1)), dtype=np.float32)

    for i, box0 in enumerate(boxes0):
        for j, box1 in enumerate(boxes1):
            costs[i, j] = calc_costs(box0, box1)

    return linear_sum_assignment(costs), costs

def group_tracks(boxes, files, cost_thresh: float = 0.1):

    # sort by creation date
    creations = {file: creation_date(file) for file in files}
    files = sorted(files, key=lambda file: creations[file])

    boxes_grouped = defaultdict(list)
    for box in boxes:
        boxes_grouped[box.described_file_id].append(box)

    connections = [[] for i in range(len(files) - 1)]

    prev = files[0]
    for step, current in enumerate(files[1:]):
        prev_boxes, curr_boxes = boxes_grouped[prev.id], boxes_grouped[current.id]
        (rows, cols), costs = assign_boxes(prev_boxes, curr_boxes)

        for row, col in zip(rows, cols):
            cost = costs[row, col]
            if cost >= cost_thresh:
                continue
            connection = prev_boxes[row], curr_boxes[col]
            connections[step].append(connection)

        prev = current

    return concat_tracks(connections)
