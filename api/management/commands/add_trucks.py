import json
import logging

from django.core.management import BaseCommand

from api.models import Truck


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    default_filename = 'data/trucks.json'

    def add_arguments(self, parser):
        parser.add_argument(
            '-f', '--filename',
            default=self.default_filename,
            help='input filename (.csv)'
        )

        parser.add_argument(
            '-a', '--append',
            dest='replace',
            action='store_false',
            default=True,
            help='Append data (default is to replace).'
        )

    def handle(self, *args, **options):
        if options['replace']:
            logger.info('erasing existing trucks')
            Truck.objects.all().delete()

        with open(options['filename']) as f:
            data = json.load(f)

        for d in data:
            Truck.objects.create(
                name=d['name'],
                handle=d['tw_handle'],
                website=d['website'],
            )

        print('{} total trucks'.format(Truck.objects.count()))
