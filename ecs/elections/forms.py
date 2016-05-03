from django.forms import ModelForm, Form, forms

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
