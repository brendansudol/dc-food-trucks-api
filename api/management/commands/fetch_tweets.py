import logging

from django.core.management import BaseCommand

from api.models import Truck
from core.twitter import client


logger = logging.getLogger(__name__)


def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


class Command(BaseCommand):
    tw = client()

    def handle(self, *args, **options):
        trucks = Truck.objects.all()
        truck_chunks = chunks(trucks, 50)

        for trucks in truck_chunks:
            handles = [t.handle for t in trucks]
            results = self.tw.UsersLookup(screen_name=handles)

            logger.info('{} results on twitter'.format(len(results)))

            for r in results:
                if not r.status:
                    continue

                handle = r.screen_name.lower()
                tweet = self.get_last_tweet(r.status, handle)

                truck, = [t for t in trucks if t.handle.lower() == handle]
                truck.image = r.profile_image_url
                truck.last_tweet = {
                    'id': tweet.id,
                    'ts': tweet.created_at_in_seconds,
                    'text': tweet.text,
                }
                truck.save()

    def get_last_tweet(self, status, handle):
        text = status.text
        if text[0] != '@' and text[:2] != 'RT':
            return status

        logger.info('fetching timeline for {}...'.format(handle))

        tweets = self.tw.GetUserTimeline(
            screen_name=handle,
            exclude_replies=True,
            include_rts=False
        )

        return tweets[0] if len(tweets) > 0 else None
