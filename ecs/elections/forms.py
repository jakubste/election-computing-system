from django.forms import ModelForm, Form, forms
from django.forms.fields import IntegerField

from ecs.elections.models import Election


class ElectionForm(ModelForm):
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


class ElectionLoadDataForm(Form):
    file = forms.FileField(required=True)

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(ElectionLoadDataForm, self).__init__(*args, **kwargs)


class ElectionGenerateDataForm(Form):
    candidates_amount = IntegerField(min_value=0, max_value=1000, initial=100)
    voters_amount = IntegerField(min_value=0, max_value=1000, initial=100)

    candidates_mean_x = IntegerField(min_value=-1000, max_value=1000, initial=0)
    candidates_mean_y = IntegerField(min_value=-1000, max_value=1000, initial=0)
    candidates_sigma = IntegerField(min_value=0, max_value=1000, initial=300)

    voters_mean_x = IntegerField(min_value=-1000, max_value=1000, initial=0)
    voters_mean_y = IntegerField(min_value=-1000, max_value=1000, initial=0)
    voters_sigma = IntegerField(min_value=0, max_value=1000, initial=300)

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election')
        super(ElectionGenerateDataForm, self).__init__(*args, **kwargs)
