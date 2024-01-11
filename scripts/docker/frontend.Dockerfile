# get the user and group. if not defined, fallback to root
ARG UID=root
ARG GID=root

########################################
# build webui                          #
########################################

FROM node:20 as builder

# copy files
COPY  ./frontend /code
WORKDIR /code

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

COPY --from=builder /code/dist /usr/share/nginx/html
USER      ${UID}:${GID}
