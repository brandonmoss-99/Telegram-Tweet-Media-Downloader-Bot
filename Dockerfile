# Use the Python 3 Docker image
FROM python:3.11.1-slim-buster

LABEL org.opencontainers.image.source=https://github.com/brandonmoss-99/Telegram-Tweet-Media-Downloader-Bot
LABEL org.opencontainers.image.description="A telegram bot which downloads media from twitter links sent to it"
LABEL org.opencontainers.image.licenses=GPL-2.0-only

RUN apt-get update && apt-get install tini

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# gallery-dl expects the conf to live at /etc/gallery-dl.conf
# Both files use .*, so that if the file doesn't exist, Docker won't error
COPY gallery-dl.* /etc/gallery-dl.conf
COPY twitter_cookies.* /etc/twitter_cookies.txt

# Copy the source files over
COPY ./src ./src

# Run the bot.py file
ENTRYPOINT [ "/usr/bin/tini", "--", "python", "src/bot.py" ]
