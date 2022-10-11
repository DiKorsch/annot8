FROM node:alpine as annot8_frontend

WORKDIR /code
COPY ./frontend/package.json /code
COPY ./frontend/package-lock.json /code

# install packages
RUN npm install -g npm
RUN npx browserslist@latest --update-db
RUN npm install

USER      ${UID}:${GID}
CMD ["npm", "run", "serve"]
