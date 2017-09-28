FROM ubuntu:16.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y \
    awscli \
    build-essential \
    bzip2 \
    ca-certificates \
    dbus \
    lsb-release \
    menu \
    openbox \
    python-dev \
    python-pip \
    sudo \
    unzip \
    wget \
    x11vnc \
    xvfb
# openwpm dependencies
RUN apt-get install -y firefox htop git python-dev libxml2-dev libxslt-dev libleveldb1v5 \
  libffi-dev libssl-dev build-essential xvfb libboost-python-dev libleveldb-dev libjpeg-dev

# Prevent errors when running xvfb as openwpm user
RUN mkdir /tmp/.X11-unix \
 && chmod 1777 /tmp/.X11-unix \
 && chown root /tmp/.X11-unix

RUN useradd openwpm \
         --shell /bin/bash  \
         --create-home \
  && usermod -a -G sudo openwpm \
  && echo 'ALL ALL = (ALL) NOPASSWD: ALL' >> /etc/sudoers \
  && echo 'openwpm:secret' | chpasswd

USER openwpm

# OpenWPM install
RUN mkdir -p /home/openwpm/OpenWPM

RUN cd /home/openwpm/ && \
    wget https://ftp.mozilla.org/pub/firefox/releases/45.9.0esr/linux-x86_64/en-US/firefox-45.9.0esr.tar.bz2 && \
    tar jxf firefox*.tar.bz2 && \
    rm -rf firefox-bin && \
    mv firefox firefox-bin && \
    rm firefox*.tar.bz2

COPY requirements.txt /home/openwpm/
RUN cd /home/openwpm/ && sudo pip install -U -r requirements.txt

COPY ./ /home/openwpm/OpenWPM
RUN rm -rf /home/openwpm/OpenWPM/firefox-bin && ln -s /home/openwpm/firefox-bin /home/openwpm/OpenWPM/

# Expose port for VNC
EXPOSE 5900
