export default class File {
  constructor(data) {
    this.id = data.id;
    this.projectId = data.projectId;
    this.url = data.url;
    this.thumbs = data.thumbs;
    this.name = data.url?.split("/").pop();

    this.annotations = {
      label: "Some label",
      boxes: [
        {
          label: "box label1",
          x: 0.3,
          y: 0.3,
          w: 0.2,
          h: 0.4,
        },
        {
          label: "box label2",
          x: 0.4,
          y: 0.5,
          w: 0.1,
          h: 0.2,
        },
      ]
    }
  }
}
