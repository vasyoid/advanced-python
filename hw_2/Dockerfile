FROM debian:stretch

RUN apt-get update && \
    apt-get install -y --no-install-recommends texlive-latex-recommended texlive-fonts-recommended && \
    apt-get install -y --no-install-recommends texlive-latex-extra texlive-fonts-extra texlive-lang-all texlive-xetex && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

# Default command
CMD ["bash"]