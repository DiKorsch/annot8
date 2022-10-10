########################################
# build webui                          #
########################################

FROM node:16 as builder

# copy files
COPY  ./frontend /annot8/frontend/
WORKDIR /annot8/frontend

# install packages
RUN npx browserslist@latest --update-db
RUN npm install -g npm
RUN npm install

# build webui
RUN npm run build


########################################
# actuall webserver                    #
########################################

FROM nginx as annot8_frontend

COPY --from=builder /annot8/frontend/dist /usr/share/nginx/html
