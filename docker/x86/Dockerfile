FROM nvidia/cuda:11.4.0-cudnn8-devel-ubuntu18.04
 
# Use bash as default shell
SHELL ["/bin/bash", "-c"]

# So that no question/dialog is asked during apt-get install:
ARG DEBIAN_FRONTEND=noninteractive

# nvidia repo public keys
# COPY keys/trusted-keys /trusted-keys

# # TensorRT required for Jetson Inference (apt-get install -y tensorrt)
# RUN printf 'deb https://repo.download.nvidia.com/jetson/common r32 main\ndeb https://repo.download.nvidia.com/jetson/t210 r32 main' > /etc/apt/sources.list.d/nvidia-l4t-apt-source.list && \
#      apt-key add /trusted-keysss

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl \
    cmake \
    build-essential \
    wget \
    gnupg \
    software-properties-common \ 
    git \
    python3-pip \
    libgsl-dev \
    libboost-system-dev \
    libboost-log-dev \
    libconfig++-dev  \
    libeigen3-dev \
    libproj-dev \
    libmove-base-msgs-dev \
    libglew-dev \
    libboost-all-dev



RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add

RUN apt-get update && apt-get install -y --no-install-recommends \ 
    ros-melodic-pcl-conversions \
    ros-melodic-pcl-msgs \
    ros-melodic-pcl-ros \
    ros-melodic-ros-base \
    ros-melodic-cv-bridge \
    ros-melodic-tf \
    ros-melodic-image-transport \
    python-catkin-tools \
    python-rosdep \
    ros-melodic-ompl \
    ros-melodic-eigen-conversions \
    libgoogle-glog-dev

#RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin 

#RUN mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600

#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
#RUN add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
#RUN apt-get update
#RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
#RUN apt install ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
#RUN apt-get update

#RUN apt-get install -y --no-install-recommends \
#    cuda-11-0 \
#    libcudnn8=8.0.4.30-1+cuda11.0  \
#    libcudnn8-dev=8.0.4.30-1+cuda11.0

#RUN apt-get install -y --no-install-recommends libnvinfer7=7.1.3-1+cuda11.0 \
#    libnvinfer-dev=7.1.3-1+cuda11.0 \
#    libnvinfer-plugin7=7.1.3-1+cuda11.0


RUN apt-get install -y python3-setuptools

RUN pip3 --no-cache-dir install \
    Cython \
    numpy

RUN OPENCV_VERSION=3.4.13 && \
    curl -L https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz | tar -xzf - && \
    curl -L https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.tar.gz | tar -xzf - && \
    cd /opencv-${OPENCV_VERSION} && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release \
          -DCMAKE_INSTALL_PREFIX=/usr/local \
          -DBUILD_SHARED_LIBS=OFF \
          -DBUILD_LIST=core,improc,imgcodecs,cudev,highgui,videoio,cudaimgproc,ximgproc,objdetect,video \
          -DBUILD_PNG=OFF \
          -DBUILD_TIFF=OFF \
          -DBUILD_TBB=OFF \
          -DBUILD_WEBP=OFF \
          -DBUILD_JPEG=OFF \
          -DBUILD_TIFF=OFF \
          -DWITH_JPEG=ON \
          -DWITH_TIFF=OFF \
          -DBUILD_JASPER=OFF \
          -DBUILD_ZLIB=ON \
          -DBUILD_EXAMPLES=OFF \
          -DBUILD_opencv_java=OFF \
          -DBUILD_opencv_python2=ON \
          -DBUILD_opencv_python3=OFF \
          -DENABLE_NEON=OFF \
          -DWITH_PROTOBUF=OFF \
          -DWITH_PTHREADS_PF=OFF \
          -DWITH_OPENCL=OFF \
          -DWITH_OPENMP=OFF \
          -DWITH_FFMPEG=ON \
          -DWITH_GSTREAMER=OFF \
          -DWITH_GSTREAMER_0_10=OFF \
          -DWITH_CUDA=ON \
          -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda/targets/x86_64-linux/ \
          -DCUDA_ARCH_BIN="6.2" \
          -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-${OPENCV_VERSION}/modules \
          -DCMAKE_LIBRARY_PATH=/usr/local/cuda/lib64/stubs \
          -DWITH_GTK=ON \
          -DWITH_VTK=OFF \
          -DWITH_TBB=OFF \
          -DWITH_1394=OFF \
          -DWITH_OPENEXR=OFF \
          -DINSTALL_C_EXAMPLES=OFF \
          -DINSTALL_TESTS=OFF \
          -DVIBRANTE=TRUE \
          VERBOSE=1 ../ && \
    make -j"$(grep ^processor /proc/cpuinfo | wc -l)" install && \
    rm -rf /opencv-${OPENCV_VERSION} && \
    rm -rf /opencv_contrib-{OPENCV_VERSION}

RUN CERES_VERSION=2.0.0 && \
    curl -L https://github.com/ceres-solver/ceres-solver/archive/refs/tags/${CERES_VERSION}.tar.gz | tar -xzf - && \
    cd ceres-solver-${CERES_VERSION} && \
    mkdir build && cd build && \
    cmake .. && \
    make -j"$(grep ^processor /proc/cpuinfo | wc -l)" install && \
    rm -rf /ceres-solver-${CERES_VERSION}

ARG PANGOLIN_COMMIT=ad8b5f83222291c51b4800d5a5873b0e90a0cf81
WORKDIR /tmp
RUN set -x && \
  git clone https://github.com/stevenlovegrove/Pangolin.git && \
  cd Pangolin && \
  git checkout ${PANGOLIN_COMMIT} && \
  sed -i -e "193,198d" ./src/utils/file_utils.cpp && \
  mkdir -p build && \
  cd build && \
  cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX} \
    -DBUILD_EXAMPLES=OFF \
    -DBUILD_PANGOLIN_DEPTHSENSE=OFF \
    -DBUILD_PANGOLIN_FFMPEG=OFF \
    -DBUILD_PANGOLIN_LIBDC1394=OFF \
    -DBUILD_PANGOLIN_LIBJPEG=OFF \
    -DBUILD_PANGOLIN_LIBOPENEXR=OFF \
    -DBUILD_PANGOLIN_LIBPNG=OFF \
    -DBUILD_PANGOLIN_LIBREALSENSE=OFF \
    -DBUILD_PANGOLIN_LIBREALSENSE2=OFF \
    -DBUILD_PANGOLIN_LIBTIFF=OFF \
    -DBUILD_PANGOLIN_LIBUVC=OFF \
    -DBUILD_PANGOLIN_LZ4=OFF \
    -DBUILD_PANGOLIN_OPENNI=OFF \
    -DBUILD_PANGOLIN_OPENNI2=OFF \
    -DBUILD_PANGOLIN_PLEORA=OFF \
    -DBUILD_PANGOLIN_PYTHON=OFF \
    -DBUILD_PANGOLIN_TELICAM=OFF \
    -DBUILD_PANGOLIN_TOON=OFF \
    -DBUILD_PANGOLIN_UVC_MEDIAFOUNDATION=OFF \
    -DBUILD_PANGOLIN_V4L=OFF \
    -DBUILD_PANGOLIN_VIDEO=OFF \
    -DBUILD_PANGOLIN_ZSTD=OFF \
    -DBUILD_PYPANGOLIN_MODULE=OFF \
    .. && \
  make -j"$(grep ^processor /proc/cpuinfo | wc -l)" install && \
  cd /tmp && \
  rm -rf *
ENV Pangolin_DIR=${CMAKE_INSTALL_PREFIX}/lib/cmake/Pangolin


COPY applications /workspace/applications
COPY docker/x86/build.sh /workspace/build.sh
COPY docker/x86/patches /workspace/applications/patches
RUN pip3 install psutil==5.8.0

RUN mkdir -p /workspace
WORKDIR /workspace

RUN /bin/bash /workspace/build.sh
COPY scripts /workspace/scripts


WORKDIR /workspace/scripts

# RUN rosdep init
# RUN rosdep update

WORKDIR /workspace/scripts/end-to-end
RUN [ -d wss ] && rm -rf wss
RUN git clone https://github.com/brendangregg/wss
COPY data /workspace/data

WORKDIR /workspace/scripts/
RUN /bin/bash /workspace/scripts/download_rosbag.sh

WORKDIR /workspace/scripts/end-to-end
RUN source /opt/ros/melodic/setup.bash
RUN apt-get install -y --no-install-recommends ros-melodic-map-server ros-melodic-hector-trajectory-server libxmlrpcpp-dev file
RUN rm -rf /workspace/applications/path_planning/hybrid-astar/lib

RUN mkdir -p /workspace/logs

CMD ["python3","runner.py"]

