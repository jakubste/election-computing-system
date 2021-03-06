from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.forms.models import model_to_dict

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
        Indicates if candidates and voters were added to election.
        """
        if self.candidates.all() and self.voters.all():
            return True
        else:
            return False

    def is_generated(self):
        """
        Indicates if elections were
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
        preferences = []
        for preference, candidate_id in enumerate(ids):
            preferences.append(Preference(
                candidate=Candidate.objects.get(election=self.election, soc_id=candidate_id),
                voter=self,
                preference=preference + 1
            ))
        Preference.objects.bulk_create(preferences)

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
        voter_preferences = [candidates_number - x for x in voter_preferences]
        return self.repeats * ell_p_norm(voter_preferences, p)


class Preference(models.Model):
    class Meta:
        ordering = ['preference']

    candidate = models.ForeignKey(Candidate)
    voter = models.ForeignKey(Voter, related_name='preferences')
    preference = models.IntegerField(null=False)


BRUTE_ALGORITHM = 'b'
GENETIC_ALGORITHM = 'g'
GREEDY_ALGORITHM = 'r'
GREEDY_CC = 'c'
ALGORITHM_CHOICES = (
    (BRUTE_ALGORITHM, 'Brute force'),
    (GENETIC_ALGORITHM, 'Genetic'),
    (GREEDY_ALGORITHM, 'Greedy Algorithm'),
    (GREEDY_CC, 'Greedy CC'),
)


class Result(models.Model):
    class Meta:
        ordering = ['p_parameter']

    election = models.ForeignKey(Election, related_name='results')
    p_parameter = models.PositiveIntegerField()
    winners = models.ManyToManyField(Candidate)
    algorithm = models.CharField(choices=ALGORITHM_CHOICES, max_length=1)
    time = models.FloatField(null=True)
    score = models.FloatField(null=True)

    def calculate_score(self):
        score = 0
        for voter in self.election.voters.all():
            score += voter.calculate_committee_score(
                self.winners.all(),
                self.p_parameter,
                self.election.candidates.count()
            )
        return score

    def get_absolute_url(self):
        return reverse('elections:result_details', args=(self.pk,))

    def __unicode__(self):
        return u'Result of {} with p={}'.format(
            self.election, self.p_parameter
        )


class GeneticAlgorithmSettings(models.Model):
    result = models.OneToOneField(Result)
    mutation_probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=10,
    )
    crossing_probability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=20,
    )
    cycles = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=50,
    )
