from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


def has_perm(user, perm, company=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    if company:
        return True
    else:
        return False

User.add_to_class('age', models.DateTimeField(null=True, blank=True))
User.add_to_class('nickname', models.CharField(max_length=50, null=True, blank=True))
User.add_to_class('height', models.IntegerField(null=True, blank=True))
User.add_to_class('has_perm', has_perm)