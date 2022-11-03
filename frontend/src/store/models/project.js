export default class Project {
  constructor(data) {
    if (data === undefined)
      data = {}
    this.id = data.id;
    this.name = data.name;
    this.description = data.description;
    this.user = data.user;
    this.created = data.created;
    this.collaborators = data.collaborators;
    this.rootFolder = data.root_folder;
    this.dataFolder = data.data_folder;
    this.model = data.model;
    this.labelProvider = data.label_provider;

    this.uuid = data.root_folder?.split("/").pop();
  }
}
