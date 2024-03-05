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

  area() {
    return this.width * this.height
  }

  iou(other){
    const x1 = this.x, y1 = this.y;
    const x2 = x1 + this.width, y2 = y1 + this.height;
    const x3 = other.x, y3 = other.y;
    const x4 = x3 + other.width, y4 = y3 + other.height;

    const x_inter1 = Math.max(x1, x3), y_inter1 = Math.max(y1, y3);
    const x_inter2 = Math.min(x2, x4), y_inter2 = Math.min(y2, y4);

    const w_inter = x_inter2 - x_inter1, h_inter = y_inter2 - y_inter1;
    if (w_inter < 0 || h_inter < 0)
      return 0;

    const area_inter = w_inter * h_inter;
    const area_union = this.area() + other.area() - area_inter;

    return area_inter / area_union;

  }
}
