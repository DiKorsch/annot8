export default class File {
  constructor(data) {
    this.id = data.id;
    this.projectId = data.projectId;
    this.url = data.url;
    this.thumbs = data.thumbs;
    this.name = data.url?.split("/").pop();
    if (data.annotation !== null) {
      this.label = data.annotation.label;
    } else {
      this.label = null;
    }
  }
}
