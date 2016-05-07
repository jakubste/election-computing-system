from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from ecs.geo.models import Point
from ecs.utils.math import ell_p_norm


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
        try:
            if self.candidates.all()[0].position:
                return True
            else:
                return False
        except:
            return False


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
                preference=preference + 1
            )

    def calculate_committee_score(self, committee, p, candidates_number):
        """
        Calculate committee score multiplied by vote repeats

        :param candidates_number: number of candidates in election
        :type candidates_number: int
        :type committee: list of ecs.elections.models.Candidate
        :type p: int
        :rtype: Decimal
        :return: committee score
        """
        # create pos_v sequence, but order actually
        # does not matter in our election system:
        voter_preferences = self.preferences.filter(candidate__in=committee).values_list('preference', flat=True)
        voter_preferences = map(
            lambda x: candidates_number - x,
            voter_preferences
        )
        return self.repeats * ell_p_norm(voter_preferences, p)


class Preference(models.Model):
    class Meta:
        ordering = ['preference']

    candidate = models.ForeignKey(Candidate)
    voter = models.ForeignKey(Voter, related_name='preferences')
    preference = models.IntegerField(null=False)


BRUTE_ALGORITHM = 'b'
GENETIC_ALGORITHM = 'g'
ALGORITHM_CHOICES = (
    (BRUTE_ALGORITHM, 'Brute force'),
    (GENETIC_ALGORITHM, 'Genetic')
)


class Result(models.Model):
    class Meta:
        ordering = ['p_parameter']

    election = models.ForeignKey(Election, related_name='results')
    p_parameter = models.PositiveIntegerField()
    winners = models.ManyToManyField(Candidate)
    algorithm = models.CharField(choices=ALGORITHM_CHOICES, max_length=1)

    def get_absolute_url(self):
        return reverse('elections:result_details', args=(self.pk,))

    def __unicode__(self):
        return u'Result of {} with p={}'.format(
            self.election, self.p_parameter
        )
