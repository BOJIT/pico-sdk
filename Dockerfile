FROM ubuntu:20.04

WORKDIR /home

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update

# Build dependencies
RUN apt-get install -y \
    git \
    cmake \
    gcc-arm-none-eabi \
    libnewlib-arm-none-eabi \
    libstdc++-arm-none-eabi-newlib \
    build-essential \
    python3

# Debug dependencies
RUN apt-get install -y \
    gdb-multiarch

# Clone pico-sdk corresponding tag + get submodules
RUN git clone --depth 1 -b 1.3.0 https://github.com/raspberrypi/pico-sdk.git
RUN git -C pico-sdk submodule init
RUN git -C pico-sdk submodule update --depth 1
