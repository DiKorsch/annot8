FROM node:16-alpine as annot8_frontend

# get the user and group. if not defined, fallback to root
ARG UID=root
ARG GID=root

WORKDIR /code
COPY ./frontend/package.json /code
COPY ./frontend/package-lock.json /code

# install packages
RUN npm install -g npm
RUN npx browserslist@latest --update-db
RUN npm install

USER      ${UID}:${GID}
CMD ["npm", "run", "serve"]
