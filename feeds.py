from django.contrib.syndication.feeds import Feed
from tst.main.models import content, site_setting
from django.core.exceptions import ObjectDoesNotExist


class LastEntries(Feed):
    title = site_setting.objects.get(id=1).title
    link = "/feeds/"
    description = site_setting.objects.get(id=1).description

    def items(self):
        return content.objects.order_by('-date')

class CategoryLastEntries(Feed):
    title = site_setting.objects.get(id=1).title
    link = "/feeds/"
    def get_object(self, category):
        if len(category) != 1:
            raise ObjectDoesNotExist
        if not content.objects.filter(category__url=category[0]):
            raise ObjectDoesNotExist
        description = category[0]
        return content.objects.filter(category__url=category[0])
    def items(self, obj):
        return obj

