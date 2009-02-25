# -*- coding:UTF-8 -*-

from openid.consumer.consumer import Consumer, SUCCESS, DiscoveryFailure
from openid.extensions.sreg import SRegRequest, SRegResponse
from openid.store.filestore import FileOpenIDStore

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils.encoding import smart_str, smart_unicode
from django.conf import settings


def create_request(openid_url, session):
    errors = []
    try:
        consumer = get_consumer(session)
        request = consumer.begin(openid_url)
        if request is None:
            errors.append('OpenID сервис не найден')
    except (DiscoveryFailure, OpenIdSetupError, ValueError), e:
        errors.append(str(e[0]))
    if errors:
        raise OpenIdError(errors)
    sreg_request = SRegRequest(optional=['nickname', 'fullname'])
    request.addExtension(sreg_request)
    return request


def get_consumer(session):
    if not settings.CICERO_OPENID_STORE_ROOT:
        raise OpenIdSetupError('CICERO_OPENID_STORE_ROOT is not set')
    return Consumer(session, FileOpenIDStore(settings.CICERO_OPENID_STORE_ROOT))

class OpenIdSetupError(Exception):
    pass

class OpenIdError(Exception):
    pass

def absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    return 'http://%s%s' % (Site.objects.get_current().domain, url)
