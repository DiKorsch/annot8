import cv2
import numpy as np

from blob_detector import utils
from blob_detector.core.bbox import BBox
from blob_detector.core.bbox_proc import Splitter
from blob_detector.core.binarizers import BinarizerType
from blob_detector.core.pipeline import Pipeline

from annot8_api.pipeline.detector.base import BaseDetector

class MothDetector(BaseDetector):
    name = "Moth Detector"
    description = "This is a blob detector for moths."

    def __init__(self):
        super().__init__()
        self.det = Detector()

    def __call__(self, im: np.ndarray) -> int:
        return self.det(im).bboxes

class Detector:
    def __init__(self,
                 min_size: int = 1080,
                 sigma: float = 5.0,
                 window_size: int = 31,
                 C: int = 2,
                 morph_kernel: int = 5,
                 morph_iters: int = 2,
                 enlarge: float = 0.01,
                ):
        super().__init__()

        BBox.MIN_AREA = 4e-4
        self.img_proc = Pipeline()
        self.img_proc.find_border()
        if min_size > 0:
            self.img_proc.rescale(min_size=min_size, min_scale=0.1)

        self.img_proc.preprocess(equalize=False, sigma=sigma)
        self.img_proc.binarize(
            type=BinarizerType.gauss_local,
            use_masked=True,
            use_cv2=True,
            window_size=window_size,
            offset=C,
            )

        self.img_proc.remove_border()
        self.img_proc.open_close(
            kernel_size=morph_kernel,
            iterations=morph_iters)

        self.bbox_proc = Pipeline()
        self.bbox_proc.detect(use_masked=True)

        _, splitter = self.bbox_proc.split_bboxes(
            preproc=Pipeline(), detector=Pipeline())

        _, bbox_filter = self.bbox_proc.bbox_filter(
            score_threshold=0.5,
            nms_threshold=0.3,
            enlarge=enlarge,
        )
        _, scorer = self.bbox_proc.score()

        self.img_proc.requires_input(splitter.set_image)
        self.img_proc.requires_input(bbox_filter.set_image)
        self.img_proc.requires_input(scorer.set_image)

    def __call__(self, im):
        gray = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
        res = self.img_proc(gray)

        return self.bbox_proc(res)
