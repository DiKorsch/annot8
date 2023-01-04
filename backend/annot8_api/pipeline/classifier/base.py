import numpy as np

class BaseClassifier:
    name = None
    description = None

    def __init__(self):
        assert self.name is not None
        assert self.description is not None

    def __call__(self, im: np.ndarray) -> tuple[int, list[tuple[int, float]]]:
        """ Returns a prediction for a given bounding_box or image.
        """

        raise NotImplementedError()
