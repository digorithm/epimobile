FROM ubuntu:14.04

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git make g++ gcc \
    python wget \
    python-dev \
    autoconf \
    git \
    curl \
    python-pip \
    libgsl0-dev \
    zlib1g-dev \
    libpq-dev

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

# Add the PostgreSQL PGP key to verify their Debian packages.
# It should be the same key as https://www.postgresql.org/media/keys/ACCC4CF8.asc
RUN apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

# Add PostgreSQL's repository. It contains the most recent stable release
#     of PostgreSQL, ``9.3``.
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

# Install ``python-software-properties``, ``software-properties-common`` and PostgreSQL 9.3
#  There are some warnings (in red) that show up during the build. You can hide
#  them by prefixing each apt-get statement with DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python-software-properties software-properties-common postgresql-9.3 postgresql-client-9.3 postgresql-contrib-9.3

# Note: The official Debian and Ubuntu images automatically ``apt-get clean``
# after each ``apt-get``


RUN sudo usermod -aG sudo,adm postgres
RUN echo "root:docker" | chpasswd
RUN echo "postgres:docker" | chpasswd
# Run the rest of the commands as the ``postgres`` user created by the ``postgres-9.3`` package when it was ``apt-get installed``
USER postgres

# Create a PostgreSQL role named ``docker`` with ``docker`` as the password and
# then create a database `docker` owned by the ``docker`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker docker

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

ENV PG_VERSION 9.3
ENV PGDATA /var/lib/postgresql/$PG_VERSION/main
ENV PGRUN /var/run/postgresql

# Expose the PostgreSQL port
EXPOSE 5432

EXPOSE 5000

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

ADD . /epimobile
WORKDIR /epimobile

USER root
ADD /sudoers.txt /etc/sudoers
RUN chmod 440 /etc/sudoers


RUN sudo chmod -R 0777 src/bioinfo/data/ebov/
RUN sudo chmod -R 0777 src/bioinfo/

ENV DATABASE_NAME epimobile
ENV POSTGRESQL_USER postgres

USER postgres
# Set the default command to run when starting the container
CMD sh entrypoint.sh