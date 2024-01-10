from annot8_ai.classifier import base

import chainer
import numpy as np
import typing as T

import yaml
from django.conf import settings
from pathlib import Path

from chainercv import transforms as tr
from cvmodelz.models import ModelFactory

class MothClassifier(base.BaseClassifier, metaclass=base.Singleton):
    name = "Moth Classifier"
    description = "This is a classifier for moth species."

    def __init__(self):
        super().__init__()

        print(f"Creating {self.name}")
        classifier_dir = Path(settings.BASE_DIR, "fixtures/classifier/jena_moths_aug")

        with open(classifier_dir / "unq2gbif.yml") as f:
            id2gbif = yaml.safe_load(f)

        self.cls = Classifier(
            model_type="cvmodelz.InceptionV3",
            input_size=299,
            weights=classifier_dir / "weights.npz",
            n_classes=len(id2gbif),
            id2gbif=id2gbif
        )

    def __call__(self, im: np.ndarray) -> int:
        return self.cls(im)


class Classifier:
    def __init__(self,
                 model_type: str,
                 n_classes: int,
                 weights: str,
                 input_size: int,
                 id2gbif: T.Dict[int, str],
                ):

        weights = Path(weights)
        assert weights.exists(), \
            f"could not find classifier weights: {weights}!"
        assert n_classes == len(id2gbif), \
            "number of classes does not match the size of the mapping!"

        self.input_size = input_size
        self.model = ModelFactory.new(model_type)
        self.model.load_for_inference(weights.resolve(),
                                      n_classes=n_classes,
                                      path="model/",
                                      strict=True)

        self._id2gbif = id2gbif


    def _transform(self, im: np.ndarray) -> int:
        _prepare = self.model.meta.prepare_func
        size = (self.input_size, self.input_size)

        # print(f"{'Orig:': <14s} {im.shape=}")
        im = _prepare(im, size=size, keep_ratio=True, swap_channels=False)
        # print(f"{'Prepare:': <14s} {im.shape=}")
        im = tr.center_crop(im, size)
        # print(f"{'CenterCrop:': <14s} {im.shape=}")
        return im

    def __call__(self, im: np.ndarray) -> int:

        assert isinstance(im, (list, np.ndarray)), \
            "im should be either a list or a numpy array!"

        if isinstance(im, np.ndarray):
            assert im.ndim == 3, \
                "Classifier accepts only RGB images (3D input)!"
            im = [im]

        im = [self._transform(_im) for _im in im]
        X = self.model.xp.array(im)
        with chainer.using_config("train", False), chainer.no_backprop_mode():
            pred = chainer.as_array(self.model(X))

        top1 = self._id2gbif[np.argmax(pred, axis=1)[0]]
        logits = [(self._id2gbif[i], logit) for i, logit in enumerate(pred[0])]

        return top1, logits
