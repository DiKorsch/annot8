import api from "./api";

import File from "@/store/models/file"
import BBox from "@/store/models/bbox"
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
        'classifier': project.classifier,
        'detector': project.detector,
      };
      return api.post("/project/", data).then(
        (response) => {
          return response.data;
        });
    },
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

    upload: function(projectId, file, callback, progress,){
      let data = new FormData();

      data.append('file', file);

      let config = {
        headers: {'content-type': 'multipart/form-data'},
        onUploadProgress: function (progressEvent) {
          if (progress !== undefined)
            progress(file, progressEvent);
        },
      }

      return api.post(`project/${projectId}/file/`, data, config)
        .then((response) => {
          callback(file, true, response);
        })
        .catch((error) =>{
          callback(file, false, error);
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
    },

    generate_bboxes: function(fileId) {
      return api.post(`file/${fileId}/bbox_generate/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("Error while generating bounding box:", error)
          return false;
        });
    },

    add_bbox: function(fileId, x, y, width, height, label) {
      let data = new FormData();

      data.append('x', x);
      data.append('y', y);
      data.append('width', width);
      data.append('height', height);
      if (!(typeof label === "undefined")) {
          data.append('label', label);
      }

      let config = {
        headers: {'content-type': 'multipart/form-data'},
      }

      return api.post(`file/${fileId}/bbox/`, data, config)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("ERROR:", error)
          return false;
        });
    },

    set_label: function(fileId, label) {
      if (fileId === undefined || label === undefined)
        return false;

      let data = new FormData();

      data.append('label', label);

      let config = {
        headers: {'content-type': 'multipart/form-data'},
      }

      return api.post(`bbox/${fileId}/label/`, data, config)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("Error while labeling file:", error)
          return false;
        });
    }
  }

  classifier = {
    select: function(projectId, classifier) {
      let data = new FormData();

      data.append('classifier', classifier);

      let config = {
        headers: {'content-type': 'multipart/form-data'},
      }

      return api.post(`project/${projectId}/classifier/`, data, config).then(
        (response) => {
          return response.data;
        });
    }
  }

  detector = {
    select: function(projectId, detector) {
      let data = new FormData();

      data.append('detector', detector);

      let config = {
        headers: {'content-type': 'multipart/form-data'},
      }

      return api.post(`project/${projectId}/detector/`, data, config).then(
        (response) => {
          return response.data;
        });
    }
  }

  bboxes = {
      get: function(fileId) {
        return api.get(`/file/${fileId}/bboxes/`)
          .then((response) => {
            console.log(response);
            return response.data.map((data) => {
              return new BBox(data);
            })
          })
          .catch((error) =>{
            console.warn(error)
            if (error.response?.status == 404)
              return null;
          });
      },

      delete: function(bboxId){
        if (bboxId === undefined)
          return false;
        return api.delete(`bbox/${bboxId}/`)
          .then(() => {
            return true;
          })
          .catch((error) => {
            console.warn("Error while deleting bounding box: ", error)
            return false;
          })
      },

      set_label: function(bboxId, label) {
        if (bboxId === undefined || label === undefined)
          return false;

        let data = new FormData();

        data.append('label', label);

        let config = {
          headers: {'content-type': 'multipart/form-data'},
        }

        return api.post(`bbox/${bboxId}/label/`, data, config)
          .then(() => {
            return true;
          }).catch((error) => {
            console.log("Error while labeling bounding box:", error)
            return false;
          });
      },

      predict: function(bboxId) {
        return api.post(`bbox/${bboxId}/predict/`)
          .then(() => {
            return true;
          }).catch((error) => {
            console.log("Error while predicting bounding box:", error)
            return false;
          });
      }
    }

  confirmator = {
    add: function(annotationId) {
      return api.post(`annotation/${annotationId}/confirmator/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("Error while confirming annotation:", error)
          return false;
        });
    },

    toggle: function(annotationId) {
      return api.post(`annotation/${annotationId}/toggle_confirmator/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("Error while changing confirmation status of annotation:", error)
          return false;
        });
    },

    remove: function (annotationId) {
      return api.remove(`annotation/${annotationId}/confirmator/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.log("Error while un-confirming annotation:", error)
          return false;
        });
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
