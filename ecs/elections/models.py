from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Election(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    committee_size = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('elections:election_details', args=(self.pk,))
