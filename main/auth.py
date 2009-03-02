# -*- coding: UTF-8 -*-

from django.conf import settings
from django.contrib.auth.models import User, check_password

class OpenidBackend:
     def authenticate(self, query=None, session=None, return_to):
        
        
