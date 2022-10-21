import api from "./api";

import File from "@/store/models/file"
import Project from "@/store/models/project"

class DataService {

  project = {
    get: function(projectId){
      if (projectId === undefined)
        return api.get("/project/")
          .then((response) => {
            return response.data.map((data) => {
              return new Project(data);
            });
          });

      return api.get(`/project/${projectId}`)
        .then((response) => {
          return new Project(response.data);
        })
        .catch((error) =>{
          if (error.response.status == 404)
            return null;
        });
    },

    delete: function(projectId) {
      return api.delete(`/project/${projectId}`)
        .then(() => {
          return true;
        })
        .catch((error) =>{
          if (error.response.status == 404)
            return false;
        });
    },

    create: function(project){
      let data = {
        'name': project.name,
        'description': project.description,
      };
      return api.post("/project/", data).then(
        (response) => {
          return response.data;
        });

    }
  }

  files = {
    get: function(projectId){
      return api.get(`/project/${projectId}/files/`)
        .then((response) => {
          return response.data.map((data) => {
            return new File(data);
          })
        })
        .catch((error) =>{
          console.warn(error)
          if (error.response?.status == 404)
            return null;
        });
    },

    upload: function(projectId, file){
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
    },

    delete: function(fileId){
      if (fileId === undefined)
        return false;
      return api.delete(`file/${fileId}/`)
        .then(() => {
          return true;
        })
        .catch((error) => {
          console.warn("Error while deleting image: ", error)
          return false;
        })
    }
  }

  collaborator = {
    remove: function(projectId, username){
      return api.delete(`project/${projectId}/collaborator/${username}/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("ERROR:", error)
          return false;
        });
    },

    add: function(projectId, username){
      let data = new FormData();

      data.append('username', username);

      let config = {
        headers: {'content-type': 'multipart/form-data'},
      }

      return api.post(`project/${projectId}/collaborator/`, data, config)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("ERROR:", error)
          return false;
        });
    }
  }

}


export default new DataService();
