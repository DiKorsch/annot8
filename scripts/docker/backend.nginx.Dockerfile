FROM nginx:latest AS annot8_nginx

COPY backend/nginx.conf /etc/nginx/nginx.conf
COPY backend/annot8.conf /etc/nginx/sites-available/annot8.conf

RUN mkdir /etc/nginx/sites-enabled
RUN ln -s /etc/nginx/sites-available/annot8.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]
