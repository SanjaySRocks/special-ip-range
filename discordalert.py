from discord_webhook import DiscordWebhook


webhook_url = ''


def AlertDiscord(msg):
    webhook = DiscordWebhook(url=webhook_url, content=msg)
    response = webhook.execute()