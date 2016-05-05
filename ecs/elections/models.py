from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from ecs.elections.geo.models import Point


class Election(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=150)
    committee_size = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('elections:election_details', args=(self.pk,))

    def is_set_up(self):
        """
        Indicates if candidates and voters where added to election.
        """
        if self.candidates.all() and self.voters.all():
            return True
        else:
            return False

    def is_generated(self):
        """
        Indicates if elections where
        generated from normal distribution.
        """
        return self.candidates.values_list('position__x', 'position__y')[0][0] is not None


class Candidate(models.Model):
    name = models.CharField(max_length=50, null=True)
    position = models.ForeignKey(Point, null=True)
    preferences = models.ManyToManyField('Voter', through='Preference')
    election = models.ForeignKey(Election, related_name='candidates')
    soc_id = models.IntegerField(null=True)

    def __unicode__(self):
        return self.name


class Voter(models.Model):
    repeats = models.IntegerField(default=1)
    position = models.ForeignKey(Point, null=True)
    election = models.ForeignKey(Election, related_name='voters')

    def set_preferences_by_ids(self, ids):
        for preference, candidate_id in enumerate(ids):
            Preference.objects.create(
                candidate=Candidate.objects.get(election=self.election, soc_id=candidate_id),
                voter=self,
                preference=preference+1
            )


class Preference(models.Model):
    class Meta:
        ordering = ['preference']

    candidate = models.ForeignKey(Candidate)
    voter = models.ForeignKey(Voter, related_name='preferences')
    preference = models.IntegerField(null=False)
