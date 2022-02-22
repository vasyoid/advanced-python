FROM debian:stretch

WORKDIR /root

RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all texlive-xetex

RUN apt-get install -y wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    wget https://www.python.org/ftp/python/3.9.5/Python-3.9.5.tgz && \
    tar xzf Python-3.9.5.tgz && \
    cd Python-3.9.5 && \
    ./configure --enable-optimizations && \
    make altinstall && \
    cd ../ && rm -rf * && \
    apt-get install -y git

RUN git clone https://github.com/vasyoid/advanced-python && \
    cd advanced-python/ && \
    pip3.9 install -r requirements.txt

WORKDIR /root/advanced-python/hw_2

CMD ["python3.9", "main.py"]