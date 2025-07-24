FROM ubuntu:22.04 AS build

LABEL authors="bhawks"

# Install Miniforge
USER root
SHELL ["/bin/bash", "-c", "-l"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh" \
    && bash Miniforge3-$(uname)-$(uname -m).sh -b -p /opt/conda \
    && source "/opt/conda/etc/profile.d/conda.sh" \
    && echo "export PATH=/opt/conda/bin:$PATH" > /etc/profile.d/conda.sh \

ENV PATH=/opt/conda/bin:$PATH

#setups stuff

RUN source /opt/conda/etc/profile.d/conda.sh && \
    conda init bash && \
    conda config --set auto_activate_base false

RUN cat ~/.bashrc

RUN source ~/.bashrc

RUN conda install -y -c conda-forge conda-pack

RUN echo $PATH
#install packages
COPY files/env.yml /tmp/env.yml
RUN conda env create --name mlcommons-benchmark --file /tmp/env.yml


RUN conda-pack -n mlcommons-benchmark -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

RUN /venv/bin/conda-unpack

FROM texlive/texlive:latest AS deploy
LABEL authors="bhawks"
# Copy the conda environment from the build stage
COPY --from=build /venv /venv
ENV PATH=/venv/bin:$PATH
ENV LD_LIBRARY_PATH=/venv/lib:$LD_LIBRARY_PATH

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

RUN apt-get update && \
    apt-get install -y \
    locales

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN dpkg-reconfigure --frontend noninteractive locales

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    biber \
    bibtool \
    cmake \
    git \
    latexmk \
    locales \
    libboost-all-dev \
    libeigen3-dev \
    libopencv-dev \
    python3-dev \
    python3-pip \
    && \
    rm -rf /var/lib/apt/lists/*


