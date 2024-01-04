import api from "./api";

import File from "@/store/models/file"
import Label from "@/store/models/label"
import BBox from "@/store/models/bbox"
import Project from "@/store/models/project"
import Task from "@/store/models/task"

// credits to https://stackoverflow.com/a/53829223/1360842
// returns a promise once it gets ALL pages from API
function paginated(url) {
  return function paginatedFetcher(next, obj_list = []) {
    return api.get(next ? next : url)
      .then(({data}) => {
        obj_list.push(...data.results)
        if (!data.next)
          return obj_list
        return paginatedFetcher(data.next, obj_list)
      })
  }
}

function parse_taxonomy(labels){
  let lookup = labels.reduce(function(res, lab){res[lab.id] = lab; return res}, {})
  for (let label of labels){
    if (label.parent_id !== null){
      let parent = lookup[label.parent_id];

      parent.add_child(label.name);
      label.set_parent(parent.name);
    }
  }

  return labels
}

class DataService {
  helper = {
  }

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
          return null;
        })
        .catch((error) =>{
          return error.response.status
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

    crops: function(projectId, grouped){
      let url = `/project/${projectId}/crops/`;
      if (grouped)
        url = `${url}?group_tracks=true`
      return api.get(url)
        .then((response) => {
          let data = response.data;
          return {
            "files": new Map(data.files.map((file) => [file.id, new File(file)])),
            "tracks": data.tracks,
            "boxes": new Map(data.boxes.map((box) => [box.id, new BBox(box)]))};
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

    upload: async function(projectId, queuedFile, callback, progress,){
      let data = new FormData();
      let file = queuedFile.file;

      data.append('file', file);
      // setTimeout(callback, 2000, file, false, "TESTING")

      let config = {
        timeout: 0,
        headers: {'content-type': 'multipart/form-data'},
        onUploadProgress: function (progressEvent) {
          if (progress !== undefined)
            progress(queuedFile, progressEvent);
        },
      }

      // console.log(data, config)

      return api.post(`project/${projectId}/file/`, data, config,)
        .then((response) => {
          callback(queuedFile, true, response);
          return response
        })
        .catch((error) =>{
          callback(queuedFile, false, error);
          return error
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
          console.warn("[API] Error while generating bounding box:", error)
          return false;
        });
    },

    predict_bboxes: function(fileId) {
      return api.post(`file/${fileId}/bbox_predict/`)
        .then(() => {
          return true;
        }).catch((error) => {
          console.warn("[API] Error while generating bounding box:", error)
          return false;
        });

    },

    add_bbox: function(fileId, x, y, width, height, label) {
      let data = {x, y, width, height, label};

      return api.post(`file/${fileId}/bbox/`, data)
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

      return api.put(`bbox/${fileId}/label/`, {label})
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
          response.data;
        });
    },

    run: function(projectId){
      return api.post(`project/${projectId}/run_classifier/`)
      .then(
        (response) => {
          return new Task(response.data);
        })
      .catch((error) => {
          console.warn("[API] Error while classifying bounding boxes:", error)
          return undefined;
        });

    },
  }

  detector = {
    run: function(projectId){
      return api.post(`project/${projectId}/run_detector/`)
      .then(
        (response) => {
          return new Task(response.data);
        })
      .catch((error) => {
          console.warn("[API] Error while detecting bounding boxes:", error)
          return undefined;
        });
    },

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
            return response.data.map((data) => {
              return new BBox(data);
            })
          })
          .catch((error) =>{
            console.warn("[API]", error)
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
            console.warn("[API] Error while deleting bounding box: ", error)
            return false;
          })
      },

      set_label: function(bboxId, label) {
        if (bboxId === undefined || label === undefined)
          return false;

        return api.put(`bbox/${bboxId}/label/`, {label})
          .then(() => {
            return true;
          }).catch((error) => {
            console.warn("[API] Error while labeling bounding box:", error)
            return false;
          });
      },

      predict: function(bboxId) {
        return api.post(`bbox/${bboxId}/predict/`)
          .then((response) => {
            return new Task(response.data);
          }).catch((error) => {
            console.warn("[API] Error while predicting bounding box:", error)
            return undefined;
          });
      },

      update: function(bbox){
        let data = {x: bbox.x, y: bbox.y, width: bbox.width, height: bbox.height};

        return api.put(`bbox/${bbox.id}/`, data)
          .then(() => {
            return true;
          }).catch((error) => {
            console.warn("[API] Error while updating bounding box:", error)
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

  labels = {
    get: function() {
      return paginated("/label/?page_size=1000")().then((results) => {
        return parse_taxonomy(results.map((data) => {
          return new Label(data);
        }))
      })
    }
  }

  tasks = {
    get: function() {
      return api.get("/task/")
        .then((response) => {
          return response.data.map((data) => {
            return new Task(data);
          });
        });
    }
  }

}


export default new DataService();
