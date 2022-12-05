# Use the Python 3 Docker image
FROM python:3.11.0-slim-buster

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
ENTRYPOINT [ "python", "src/bot.py" ]
