
from labeltree.views import LabelViewSet as BaseLabelViewSet
from labeltree.views import LabelGroupViewSet as BaseLabelGroupViewSet

from annot8_api.views.base import BaseViewSet


class LabelViewSet(BaseLabelViewSet, BaseViewSet):
    pass

class LabelGroupViewSet(BaseLabelGroupViewSet, BaseViewSet):
    pass


