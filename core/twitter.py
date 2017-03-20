import twitter

from django.conf import settings


def client():
    return twitter.Api(
        consumer_key=settings.TW_CONSUMER_KEY,
        consumer_secret=settings.TW_CONSUMER_SECRET,
        access_token_key=settings.TW_ACCESS_TOKEN_KEY,
        access_token_secret=settings.TW_ACCESS_TOKEN_SECRET
    )
