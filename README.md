# Telegram Tweet Media Downloader Bot
[![Tests](https://img.shields.io/github/actions/workflow/status/brandonmoss-99/Telegram-Tweet-Media-Downloader-Bot/tests.yml?label=tests&logo=github)](https://github.com/brandonmoss-99/Telegram-Tweet-Media-Downloader-Bot/actions/workflows/tests.yml)
[![License](https://img.shields.io/github/license/brandonmoss-99/Telegram-Tweet-Media-Downloader-Bot?logo=github)](https://github.com/brandonmoss-99/Telegram-Tweet-Media-Downloader-Bot/blob/main/LICENSE) [![Docker image pulls](https://img.shields.io/docker/pulls/brandonmoss99/telegram-tweet-media-downloader?logo=docker)](https://hub.docker.com/r/brandonmoss99/telegram-tweet-media-downloader) [![Docker image size](https://img.shields.io/docker/image-size/brandonmoss99/telegram-tweet-media-downloader?logo=docker)](https://hub.docker.com/r/brandonmoss99/telegram-tweet-media-downloader)

## What does this do?
This is a bot for the Telegram messaging service, with the purpose of downloading and saving media from tweets to a local machine (thanks to [gallery-dl](https://github.com/mikf/gallery-dl)). It is intended to be run within a containerised solution.

## Configuration
### Environment variables
The following environment variables are used by the bot, and should be passed into the container's environment when run:
#### Required:
  - `T_TOKEN` - The Telegram Bot API token to use. Should be a String, `"12345:AAAABBBBCCCCDDDD"`
  - `ALLOWED_IDS` - The Telegram user IDs to accept messages from. This is required, as without it, anyone who finds your bot username on Telegram will be able to send a link, and download media to your server. Should be a comma separated String of IDs, `"123456,654321"`

#### Optional:
  - `LOG_LEVEL` - The lowest level of logging to output, as a String. Can be one of the following: `"debug"`, `"info"`, `"warn"`, `"error"`, or `"critical"`. Defaults to `"info"`

### Cookies
A valid Twitter cookie file allows gallery-dl to access the same tweets you can see. Without this, it will only be able to access what is publicly visible. A file named `twitter_cookies.txt` should be present in the top directory.

### gallery-dl configuration
gallery-dl accepts a wide range of configuration options. An example `gallery-dl.conf` file is included, but this can be adjusted to your requirements (See [gallery-dl configuration](https://github.com/mikf/gallery-dl#configuration) for more).

