FROM docker.io/python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install enterprise self-signed certificate into the container

COPY enterprise-ca.crt /usr/local/share/ca-certificates/enterprise-ca.crt
RUN update-ca-certificates
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# OS deps (kept minimal; add more if you need them)
RUN apt-get update && apt-get install -y --no-install-recommends \
      tini \
      git \
      curl \
      ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create an unprivileged user (good default for rootless Podman)
ARG NB_USER=app
ARG NB_UID=1000
ARG NB_GID=1000
RUN groupadd -g ${NB_GID} ${NB_USER} \
 && useradd -m -s /bin/bash -u ${NB_UID} -g ${NB_GID} ${NB_USER}

# Install Python packages (CPU-only deep learning stack)
# - PyTorch CPU wheels are served from the pytorch CPU index.
RUN python -m pip install --upgrade pip \
 && python -m pip install \
      jupyterlab \
      ipykernel \
      numpy \
      pandas \
      scipy \
      scikit-learn \
      matplotlib \
      seaborn \
      tqdm \
      pillow \
      opencv-python-headless \
 && python -m pip install \
      torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Workspace
WORKDIR /workspace
RUN mkdir -p /workspace && chown -R ${NB_UID}:${NB_GID} /workspace

USER ${NB_USER}

EXPOSE 8888

# Jupyter settings:
# - bind to all interfaces
# - store runtime bits under the user's home
# - allow token/password to be configured via env (defaults are safe)
ENV JUPYTER_TOKEN="" \
    JUPYTER_PASSWORD=""

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash", "-lc", "jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --ServerApp.root_dir=/workspace --ServerApp.allow_origin='*'"]

