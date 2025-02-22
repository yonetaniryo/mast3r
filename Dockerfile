
FROM ubuntu:22.04


# Install python
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y update && apt-get -y install --no-install-recommends python3.10-minimal python3-pip libgl1-mesa-glx libglib2.0-0 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set default python
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

WORKDIR /workspace


RUN pip install uv

COPY mast3r mast3r
COPY dust3r dust3r
COPY pyproject.toml .
COPY uv.lock .
COPY .python-version .
RUN uv sync --frozen 
COPY get_poses.py .