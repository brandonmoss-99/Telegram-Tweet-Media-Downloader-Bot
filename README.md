# Telegram Tweet Media Downloader Bot

## What does this do?
This is a bot for the Telegram messaging service, with the purpose of downloading and saving media from tweets to a local machine (thanks to [gallery-dl](https://github.com/mikf/gallery-dl)). It is intended to be run within a containerised solution.

## Configuration
### Environment variables
The following environment variables are used by the bot, and should be passed into the container's environment when run:
  - `T_TOKEN` - The Telegram Bot API token to use. Should be a String, `"12345:AAAABBBBCCCCDDDD"`
  - `ALLOWED_IDS` - The Telegram user IDs to accept messages from. This is required, as without it, anyone who finds your bot username on Telegram will be able to send a link, and download media to your server. Should be a comma separated String of IDs, `"123456,654321"`

### Cookies
A valid Twitter cookie file allows gallery-dl to access the same tweets you can see. Without this, it will only be able to access what is publicly visible. A file named `twitter_cookies.txt` should be present in the top directory.

### gallery-dl configuration
gallery-dl accepts a wide range of configuration options. An example `gallery-dl.conf` file is included, but this can be adjusted to your requirements (See [gallery-dl configuration](https://github.com/mikf/gallery-dl#configuration) for more).

