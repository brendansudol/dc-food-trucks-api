import json
import logging
import requests

from collections import defaultdict
from django.core.management import BaseCommand

from api.models import Truck


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        locs = self.fetch_locations()

        if not locs:
            logger.info('no locations found :(')
            return

        trucks = Truck.objects.all()
        trucks.update(location=None)

        locs_by_truck = self.munge_locations(locs)
        for name, locs in locs_by_truck.items():
            truck, = [t for t in trucks if t.handle.lower() == name] or [None]

            if not truck:
                continue

            truck.location = locs
            truck.save()

    def fetch_locations(self):
        url = 'http://foodtruckfiesta.com/apps/map_json.php' + \
              '?num_days=365&minimal=0&alert_nc=y&alert_hc=0&alert_pm=0&rand=1'

        try:
            data = json.loads(requests.get(url, timeout=10).content)
            return data.get('markers')
        except Exception as e:
            logger.warn('fetch error: {}'.format(e))

    def munge_locations(self, locs, threshold=0.00025):
        data = []
        for loc in locs:
            try:
                loc['lat'] = float(loc['coord_lat'])
                loc['lng'] = float(loc['coord_long'])
                data.append(loc)
            except Exception:
                pass

        by_truck = defaultdict(list)
        data = sorted(data, key=lambda k: k['lat'])
        prev = {'lat': 0, 'lng': 0}

        for i, d in enumerate(data):
            lat, lng, name = d['lat'], d['lng'], d.get('truck') or ''
            d['loc_adj'] = {'lat': lat, 'lng': lng, 'base': name}

            if lat - prev['lat'] < threshold:
                matches = [
                    d2 for d2 in data[:i] if
                    lat - d2['lat'] < threshold and
                    lng - d2['lng'] < threshold and
                    lng - d2['lng'] > 0
                ]
                if len(matches) > 0:
                    d['loc_adj'] = matches[0]['loc_adj']

            by_truck[name].append(d['loc_adj'])
            prev['lat'], prev['lng'] = lat, lng

        return dict(by_truck)
