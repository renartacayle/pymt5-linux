# Production Dockerfile for MT5 Headless Gateway & Linux Python Environment
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV WINEPREFIX=/root/.wine
ENV DISPLAY=:99

# Install base dependencies, WineHQ, Xvfb, Python 3
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        wine64 wine32 xvfb ca-certificates curl wget cabextract \
        python3 python3-pip python3-venv git procps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Initialize wine prefix
RUN wineboot --init || true

# Copy project files
COPY . /app

# Install pymt5-linux
RUN pip3 install --no-cache-dir .

EXPOSE 18812

CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 -ac & pymt5-linux gateway --port 18812"]
