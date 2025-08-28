FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
# override: --build-arg PYTHON_VERSION=3.12
ARG PYTHON_VERSION=3.11
ARG UID=1000
ARG GID=1000

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common curl ca-certificates gnupg make git \
    build-essential pkg-config locales \
 && add-apt-repository -y ppa:deadsnakes/ppa \
 && apt-get update && apt-get install -y --no-install-recommends \
    python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev \
 && rm -rf /var/lib/apt/lists/*

# Locale (LaTeX + Unicode friendliness)
RUN sed -i 's/# *en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen && locale-gen
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8

RUN /usr/bin/python${PYTHON_VERSION} -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --upgrade pip

WORKDIR /workspace

COPY Makefile requirements.txt ./

RUN make install_latex
RUN make install

COPY . .

CMD ["bash"]