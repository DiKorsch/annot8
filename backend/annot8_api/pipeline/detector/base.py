import numpy as np

class Detection:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

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
