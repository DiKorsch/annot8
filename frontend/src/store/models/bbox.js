export default class BBox {
  constructor(data) {
    this.id = data.id
    this.fileId = data.described_file;
    this.pipelineGenerated = data.pipeline_generated;
    if (!data.pipeline_generated) {
      this.creator = data.creator;
    }
    this.x = data.x;
    this.y = data.y;
    this.width = data.width;
    this.height = data.height;
    if (data.annotation !== null) {
      this.label = data.annotation.label;
      this.annotator = data.annotation.annotator;
      this.annotationId = data.annotation.id;
      this.confirmators = data.annotation.confirmators;
    } else {
      this.label = null;
      this.annotator = null;
      this.annotationId = null;
      this.confirmators = null;
    }
    if (data.prediction !== null) {
      this.predicted_label = data.prediction.top_1_label;
      this.prediction_model = data.prediction.model;
    } else {
      this.predicted_label = null;
      this.prediction_model = null;
    }

    this.thumbs = data.thumbs;
  }
}
