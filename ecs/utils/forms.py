from django.forms import ModelForm, Form


# noinspection PyArgumentList,PyUnresolvedReferences
class BootstrapMixin(object):
    def __init__(self, *args, **kwargs):
        super(BootstrapMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            try:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
            except:
                pass


class BootstrapModelForm(BootstrapMixin, ModelForm):
    pass


class BootstrapForm(BootstrapMixin, Form):
    pass
