import api from "./api";

class DataService {

  getProjects() {
    return api.get("/project/")
      .then((response) => {
        return response.data;
      });
  }

  getProject(projectId) {
    return api.get(`/project/${projectId}`)
      .then((response) => {
        return response.data;
      })
      .catch((error) =>{
        if (error.response.status == 404)
          return null;
      });
  }

  deleteProject(projectId) {
    return api.delete(`/project/${projectId}`)
      .then(() => {
        return true;
      })
      .catch((error) =>{
        if (error.response.status == 404)
          return false;
      });
  }

  createProject(project) {
    return api.post("/project/", {
      'name': project.name,
      'description': project.description,
    }).then(
      (response) => {
        return response.data;
      });
  }

  getFiles(projectId) {
    return api.get(`/project/${projectId}/files`)
      .then((response) => {
        return response.data;
      })
      .catch((error) =>{
        if (error.response.status == 404)
          return null;
      });
  }

  uploadFile(projectId, file){
    let data = new FormData();

    data.append('file', file);

    let config = {
      headers: {'content-type': 'multipart/form-data'},
      onUploadProgress: function (progressEvent) {
        console.log(progressEvent)
      },
    }

    return api.post(`project/${projectId}/file/`, data, config)
      .then((response) => {
        console.log("OK", response.status);
      })
      .catch((error) =>{
        console.log("ERROR:", error)
      })
  }
}


export default new DataService();
