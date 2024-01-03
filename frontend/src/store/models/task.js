export default class Task {
  constructor(content){
    this.id = content.id;
    this.uuid = content.task_uuid;
    this.nqueued = content.nqueued;
    this.nready = content.nready;
  }
}
