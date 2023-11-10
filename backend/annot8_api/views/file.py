import logging

from django.db.models import Q
from tqdm.auto import tqdm

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from annot8_api.models import Annotation
from annot8_api.models import BoundingBox
from annot8_api.models import File
from annot8_api.serializers import BoundingBoxSerializer
from annot8_api.serializers import FileSerializer
from annot8_api.views.base import BaseViewSet

class FileViewSet(BaseViewSet):

    serializer_class = FileSerializer
    def get_queryset(self):
        user = self.request.user
        return File.objects.filter(
            Q(project__user=user) |
            Q(project__collaborators__in=[user])
        ).distinct()

    @action(detail=True)
    def bboxes(self, request, pk=None):
        file = self.get_object()

        bboxes = file.bboxes

        serializer = BoundingBoxSerializer(bboxes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="bbox_generate")
    def bbox_generate(self, request, pk=None):
        file = self.get_object()
        project = file.project

        # Get detector.
        detector = project.get_detector()
        if detector is None:
            return Response({"status": "Project does not have a detector"},
                status=status.HTTP_400_BAD_REQUEST)

        # Get classifier.
        classifier = project.get_classifier()

        # Remove all prior pipeline-generated bounding boxes.
        BoundingBox.objects.filter(described_file=file, pipeline_generated=True).delete()

        # Perform detection.
        generated_bboxes = detector(file.as_numpy())
        logging.info(f"Estimated {len(generated_bboxes)} detections")
        boxes = []
        for bbox in generated_bboxes:
            # Generate bounding boxes.
            w = bbox.x1 - bbox.x0
            h = bbox.y1 - bbox.y0
            if not bbox.is_valid or w <= 0 or h <= 0:
                continue
            boxes.append(BoundingBox.create(file, bbox.x0, bbox.y0, w, h, True))
        return Response({'status': 'BBoxes generated'})

        logging.info(f"Estimating species for {len(boxes)} valid boxes")
        for bbox in tqdm(boxes):
            # If possible, generate predictions.
            if classifier is not None:
                try:
                    label, logits = classifier(bbox.as_numpy())
                    bbox.prediction_add(label, logits, project.classifier)
                except Exception as e:
                    print("Generating prediction for bounding box failed due to: " + str(e))


        return Response({'status': 'BBoxes generated'})

    @action(detail=True, methods=["post"], url_path="bbox")
    def bbox_add(self, request, pk=None):
        x, y, width, height, label = [request.data.get(key) for key in ["x", "y", "width", "height", "label"]]

        if None in [y, x, width, height]:
            return Response({"status": "Argument for bbox missing"},
                status=status.HTTP_400_BAD_REQUEST)

        file = self.get_object()
        user = self.request.user

        try:
            bbox = BoundingBox.create(file, x, y, width, height, False, user)
            if label is not None:
                Annotation.create(described_object=bbox, label=label, annotator=user)

        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'BBox added'})

    @action(detail=True, methods=["put"], url_path="label")
    def label_set(self, request, pk=None):
        label = request.data.get("label")
        if label is None:
            return Response({"status": "Label missing"},
                status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        file = self.get_object()

        # Create a corresponding annotation / update the existing one.
        try:
            annotation, created = Annotation.objects.get_or_create(described_object=file)
            annotation.label = label
            annotation.annotator = user
            annotation.confirmators.clear()
            annotation.save()
        except Exception as e:
            print(e)
            return Response({"status": str(e)},
                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': 'Label added to file'})
