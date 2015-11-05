#! /usr/bin/env python
import os, sys

sys.path.append('..')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from app.models import Trend, Location

import django
django.setup()

for location in Location.objects.all():
    for trend in location.trend_set.all():
        trend.saveSlug()
        trend.save()