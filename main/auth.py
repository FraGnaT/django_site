# -*- coding: UTF-8 -*-

from django.conf import settings
from django.contrib.auth.models import User, check_password
from openid.consumer.consumer import Consumer, SUCCESS, DiscoveryFailure
from openid.store.filestore import FileOpenIDStore

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str, smart_unicode

class OpenidBackend(object):
    def authenticate(self, query=None, session=None, return_to):
        query = dict([(k, smart_str(v)) for k, v in query.items()])
        consumer = get_consumer(session)
        info = consumer.complete(query, 'http://localhost'+return_path.encode('UTF-8'))
        if info.status != SUCCESS:
            return None
        try:
            user = User.objects.get(username=info.identity_url[info.identity_url.index('://')+3:])
        except Profile.DoesNotExist:
            user = User.objects.create_user(info.identity_url[info.identity_url.index('://')+3:], 'openid@openid', User.object.make_random_password())
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
