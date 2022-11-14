export default class BBox {
  constructor(data) {
    this.id = data.id
    this.fileId = data.described_file;
    this.x = data.x;
    this.y = data.y;
    this.width = data.width;
    this.height = data.height;
    if (data.annotation !== null) {
      this.label = data.annotation.label;
      this.annotator = data.annotation.annotator;
      this.confirmators = data.annotation.confirmators;
    } else {
      this.label = null;
      this.annotator = null;
      this.confirmators = null;
    }
  }
}
