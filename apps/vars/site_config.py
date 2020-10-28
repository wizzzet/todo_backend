import datetime

from snippets.utils.datetime import utcnow
from vars.models import SiteConfig


CACHE_TIMEOUT = datetime.timedelta(0, 30)


class SiteConfigs(object):
    def __init__(self):
        self.last_modified = None
        self.configs = None

    def index(self, force=False):
        now = utcnow()
        if force \
                or self.last_modified is None \
                or now - self.last_modified > CACHE_TIMEOUT:

            self.configs = SiteConfig.get_solo()
            self.last_modified = now

    def force_index(self):
        return self.index(force=True)

    def get(self, field_name, default_value=''):
        self.index()
        if not self.configs:
            return default_value

        return getattr(self.configs, field_name, default_value)

    def all(self):
        self.index()
        return self.configs


site_config = SiteConfigs()
