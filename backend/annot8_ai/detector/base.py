import numpy as np

from dataclasses import dataclass


@dataclass
class Detection:
    x1: int
    x2: int
    y1: int
    y2: int

class BaseDetector:
    name = None
    description = None

    def __init__(self):
        assert self.name is not None
        assert self.description is not None

    def __call__(self, im: np.ndarray) -> Detection:
        """ Returns predicted bounding boxes for a given bounding_box or image.
        """

        raise NotImplementedError()
