FROM tensorflow/tensorflow:2.6.0

# The code below is all based off the repos made by https://github.com/fbcotter
RUN apt-get update

WORKDIR /cv-inference-engine

COPY . .

# Core linux dependencies. 
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get install -y \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config

# Python dependencies
RUN pip3 --no-cache-dir install \
    numpy \
    opencv-python==4.5.3.56

ENTRYPOINT [ "python3", "test.py" ]