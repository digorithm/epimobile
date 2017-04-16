FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git make g++ gcc \
    python wget \
    autoconf \
    git \
    curl \
    python-pip \
    libgsl0-dev \
    zlib1g-dev \
    libpq-dev \
    postgresql

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install Capnproto (mash dependency)

RUN curl https://capnproto.org/capnproto-c++-0.5.3.tar.gz --output capnproto-c++-0.5.3.tar.gz

RUN tar zxf capnproto-c++-0.5.3.tar.gz
RUN sh capnproto-c++-0.5.3/configure
RUN make -j6 check
RUN make install

RUN git clone https://github.com/marbl/Mash.git
RUN cd Mash \
    && sh bootstrap.sh \
    && ./configure \
    && make \
    && make install

ADD . /epimobile
WORKDIR /epimobile

EXPOSE 5000
CMD ["python", "src/app.py"]
