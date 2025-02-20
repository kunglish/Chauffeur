FROM nvcr.io/nvidia/l4t-base:r32.2

# Use bash as default shell
SHELL ["/bin/bash", "-c"]

# So that no question/dialog is asked during apt-get install:
ARG DEBIAN_FRONTEND=noninteractive

# nvidia repo public keys
COPY keys/trusted-keys /trusted-keys

# TensorRT required for Jetson Inference (apt-get install -y tensorrt)
RUN printf 'deb https://repo.download.nvidia.com/jetson/common r32 main\ndeb https://repo.download.nvidia.com/jetson/t210 r32 main' > /etc/apt/sources.list.d/nvidia-l4t-apt-source.list && \
     apt-key add /trusted-keys

# Add ROS package server
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
     apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 

RUN apt-get update && apt-get install -y --no-install-recommends \
     ca-certificates curl \
     cmake \
     build-essential \
     # *** Jetson inference starts ***
     libgstreamer1.0-dev \                   
     libgstreamer-plugins-base1.0-dev \
     libglew-dev\ 
     tensorrt \
     # *** Jetson inference ends ***
     # *** Lane detection starts ***
     libgsl-dev \
     libboost-system-dev \
     libboost-log-dev \
     libconfig++-dev \
     # *** Lane detection ends ***
     # *** OpenCV starts ***
     libhdf5-dev \
     python3-pip \
     libgtk2.0-dev \
     # *** OpenCV ends ***
     # *** FFMpeg (OpenCV) starts ***
     libavcodec-dev \
     libavformat-dev \
     libavutil-dev \
     libswscale-dev \
     libswresample-dev \
     # *** FFMpeg (OpenCV) ends ***
     # *** ROS starts ***
     ros-melodic-ros-base \
     ros-melodic-cv-bridge \
     ros-melodic-tf \
     ros-melodic-image-transport \
     python-catkin-tools \
     python-rosdep \
     # *** ROS ends ***
     # *** Path planner starts ***
     ros-melodic-ompl \
     libeigen3-dev \
     # *** Path planner ends ***
     # Floam
    ros-melodic-eigen-conversions \
     # CERES
    libgoogle-glog-dev

RUN apt-get install python3-setuptools

RUN pip3 --no-cache-dir install \
     Cython \
     numpy

# OpenCV
RUN OPENCV_VERSION=3.4.13 && \
    curl -L https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz | tar -xzf - && \
    curl -L https://github.com/opencv/opencv_contrib/archive/${OPENCV_VERSION}.tar.gz | tar -xzf - && \
    cd /opencv-${OPENCV_VERSION} && \
#     wget -O cmake/FindCUDA.cmake https://raw.githubusercontent.com/opencv/opencv/master/cmake/FindCUDA.cmake && \
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
          -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda/targets/aarch64-linux/ \
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

# Docker best practise
# RUN rm -rf /var/lib/apt/lists/*

# ROS key update
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# try eigen three installation
RUN apt-get update && apt-get install -y --no-install-recommends \
     ros-melodic-pcl-conversions \
     ros-melodic-pcl-msgs \
     ros-melodic-pcl-ros \
     libeigen3-dev \
     libproj-dev \
     libmove-base-msgs-dev
RUN ln -s /usr/include/eigen3/Eigen /usr/local/include/Eigen


RUN apt-get install -y --no-install-recommends git

# Pangolin
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

RUN mkdir -p /workspace
WORKDIR /workspace

# Required for orb-slam-3 cmake file
RUN rosdep init
RUN rosdep update

CMD [ "bash", "/workspace/build.sh" ]