from __future__ import unicode_literals
from datetime import timedelta
import logging

from core.analytics import ScheduledAnalytics
from core.observables import Tag


class TagLogic(ScheduledAnalytics):

    default_values = {
        "frequency": timedelta(hours=1),
        "name": "TagLogic",
        "description": "Processes some tagging logic",
    }

    ACTS_ON = []  # act on all observables
    EXPIRATION = timedelta(days=1)

    @staticmethod
    def each(obj):

        all_tags = set([t.name for t in obj.tags])

        # if an URL is tagged blocklist, tag all related hostnames
        if obj.type == 'Url' and 'blocklist' in all_tags:
            for link in obj.neighbors(neighbor_type="Hostname").values()[0]:
                link[1].tag('blocklist')

        # tag absent produced tags
        for tag in obj.tags:
            t = Tag.objects.get(name=tag.name)
            produced_tags = t.produces
            obj.tag([t.name for t in produced_tags if t.name not in all_tags])
