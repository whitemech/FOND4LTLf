FROM ubuntu:22.04

RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    cmake           \
    g++             \
    git             \
    libgmp3-dev     \
    make            \
    wget            \
    time            \
    zlib1g-dev

# Set up some environment variables.
ENV CXX=g++

RUN apt-get install -y mona && \
    apt-get install -y libssl-dev && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip

RUN git clone https://github.com/whitemech/FOND4LTLf.git && \
    cd FOND4LTLf && \
    pip install .

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

CMD ["fond4ltlf"]
