from django.db import models
# Needed for User
from django.contrib.auth.models import User
from django.conf import settings

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), null=True)
    def __str__(self):
        return self.ticker

