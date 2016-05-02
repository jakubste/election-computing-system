from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from ecs.elections.geo.models import Point


class Election(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    committee_size = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name


class Candidate(models.Model):
    name = models.CharField(max_length=50, null=True)
    position = models.ForeignKey(Point, null=True)
    preferences = models.ManyToManyField('Voter', through='Preference')
    election = models.ForeignKey(Election, related_name='candidates')

    def __unicode__(self):
        return self.name


class Voter(models.Model):
    repeats = models.IntegerField(default=1)
    position = models.ForeignKey(Point, null=True)
    election = models.ForeignKey(Election, related_name='voters')


class Preference(models.Model):
    candidate = models.ForeignKey(Candidate)
    voter = models.ForeignKey(Voter, related_name='preferences')
    preference = models.IntegerField(null=False)
