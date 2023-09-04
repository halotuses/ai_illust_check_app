FROM debian:bullseye-slim

RUN apt-get update && apt-get install -y wget
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH="/miniconda/bin:${PATH}"

RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN conda create -n app python==3.11.3

SHELL ["conda", "run", "-n", "app", "/bin/bash", "-c"]

RUN conda install nomkl -c conda-forge --override-channels
RUN conda install flask=2.2.2 -c conda-forge --override-channels
RUN conda install flask-cors=3.0.10 -c conda-forge  --override-channels
RUN conda install opencv=4.6.0 -c conda-forge --override-channels
RUN conda install numpy=1.24.3 -c conda-forge  --override-channels
RUN conda install pillow=9.4.0 -c conda-forge  --override-channels
RUN conda install scikit-learn=1.3.0 -c conda-forge  --override-channels
RUN conda install scipy=1.11.1 -c conda-forge --override-channels

RUN pip3 install --upgrade pip
RUN pip3 install gunicorn

ADD . /app/
ENV PORT 8080
WORKDIR /app
CMD gunicorn --bind 0.0.0.0:$PORT app:app