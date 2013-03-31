import os

os.environ['DJANGO_SETTINGS_MODULE'] = "sccontest.settings"

from django.contrib.auth.models import User

for u in User.objects.all():
    if not u.first_name:
        u.first_name = u.username
        u.save()
