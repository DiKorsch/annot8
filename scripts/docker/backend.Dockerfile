FROM python:3.9-slim AS annot8_backend

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# get the user and group. if not defined, fallback to root
ARG UID=root
ARG GID=root

RUN apt update && \
	apt install -y \
		python3-dev \
		libc-dev \
		pkg-config \
		gcc \
		g++ \
		libmariadb-dev

WORKDIR /code

# install dependencies
COPY ./backend/requirements.txt /code/
RUN python -m pip install --upgrade pip
RUN pip install numpy uwsgi
RUN pip install -r /code/requirements.txt
RUN rm /code/requirements.txt

# #
# RUN python -c "from django.core.management.utils import get_random_secret_key as new_key; print(new_key())" > /code/secret.txt
# RUN chown -R ${UID}:${GID} /code/
# RUN chmod 600 /code/secret.txt

USER      ${UID}:${GID}
