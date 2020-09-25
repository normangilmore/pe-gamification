FROM ubuntu:focal-20200916
ENV PYTHONUNBUFFERED 1
ENV TERM xterm

# helpful aliases
COPY ./docker/bashrc_to_docker /root/.bashrc

# ARG vars exist only during build
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -q && apt-get install -y --no-install-recommends \
        git-core curl less psmisc rsync \
        software-properties-common \
        build-essential libssl-dev libffi-dev

RUN apt-get update -q && apt-get install -y --no-install-recommends \
        python3 python3-dev python3-virtualenv \
        python3-setuptools python3-pip python3-apt \
        libjpeg-dev swig \
        dbus libdbus-1-dev libdbus-glib-1-dev \
        libsasl2-dev libldap2-dev libssl-dev

# for admin convenience
RUN apt-get update -q && apt-get install -y --no-install-recommends \
        postgresql-client-12

RUN rm -rf /var/lib/apt/lists/*

ARG USER=dashboard
ARG USER_ID=9001
ARG GROUP_ID=9001
ARG HOME=/home/dashboard
RUN groupadd -g ${GROUP_ID} ${USER} && \
      useradd --shell /bin/bash --home ${HOME} -u ${USER_ID} -g ${GROUP_ID} ${USER}

ARG VIRTUAL_ENV=/home/python3_env
ENV ACTIVATE=${VIRTUAL_ENV}/bin/activate
WORKDIR ${VIRTUAL_ENV}
RUN /usr/bin/python3 -m virtualenv --python=python3 ${VIRTUAL_ENV}

RUN . ${ACTIVATE} && pip3 install --upgrade pip

WORKDIR ${HOME}
COPY ./requirements.txt .
RUN . ${ACTIVATE} && pip3 install -r requirements.txt

USER ${USER}
COPY ./docker/bashrc_to_docker ${HOME}/.bashrc
