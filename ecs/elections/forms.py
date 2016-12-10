from django.forms import forms
from django.forms.fields import IntegerField

from ecs.elections.models import Election, Result, GeneticAlgorithmSettings
from ecs.settings import ELECTION_GENERATOR
from ecs.utils.forms import BootstrapModelForm, BootstrapForm


class ElectionForm(BootstrapModelForm):
    class Meta:
        model = Election
        fields = ['name', 'committee_size']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ElectionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        election = super(ElectionForm, self).save(False)
        if commit:
            election.user = self.user
            election.save()
        return election


class ElectionLoadDataForm(BootstrapForm):
    file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(ElectionLoadDataForm, self).__init__(*args, **kwargs)


class ElectionGenerateDataForm(BootstrapForm):
    candidates_amount = IntegerField(min_value=0, max_value=ELECTION_GENERATOR['MAX_CANDIDATES'], initial=20)
    voters_amount = IntegerField(min_value=0, max_value=ELECTION_GENERATOR['MAX_VOTERS'], initial=20)

    candidates_mean_x = IntegerField(
        min_value=-ELECTION_GENERATOR['MAX_MEAN'], max_value=ELECTION_GENERATOR['MAX_MEAN'], initial=0)
    candidates_mean_y = IntegerField(
        min_value=-ELECTION_GENERATOR['MAX_MEAN'], max_value=ELECTION_GENERATOR['MAX_MEAN'], initial=0)
    candidates_sigma = IntegerField(
        min_value=0, max_value=ELECTION_GENERATOR['MAX_SIGMA'], initial=30)

    voters_mean_x = IntegerField(
        min_value=-ELECTION_GENERATOR['MAX_MEAN'], max_value=ELECTION_GENERATOR['MAX_MEAN'], initial=0)
    voters_mean_y = IntegerField(
        min_value=-ELECTION_GENERATOR['MAX_MEAN'], max_value=ELECTION_GENERATOR['MAX_MEAN'], initial=0)
    voters_sigma = IntegerField(
        min_value=0, max_value=ELECTION_GENERATOR['MAX_SIGMA'], initial=30)

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(ElectionGenerateDataForm, self).__init__(*args, **kwargs)


class ResultForm(BootstrapModelForm):
    class Meta:
        model = Result
        fields = ['p_parameter', 'algorithm']

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(ResultForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        result = super(ResultForm, self).save(False)
        if commit:
            result.election = self.election
            result.save()
        return result


class GeneticAlgorithmForm(BootstrapModelForm):
    class Meta:
        model = GeneticAlgorithmSettings
        exclude = ['result']

    def __init__(self, *args, **kwargs):
        try:
            self.result = kwargs.pop('result')
        except KeyError:
            self.result = None
        super(GeneticAlgorithmForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        settings_object = super(GeneticAlgorithmForm, self).save(False)
        if commit:
            settings_object.result = self.result
            settings_object.save()
        return settings_object
