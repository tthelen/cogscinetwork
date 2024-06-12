from .models import Profile, Experience, Academic
from django import forms
from django_registration.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory
import datetime

class CogsciNetworkRegistrationForm(RegistrationForm):

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_("I have read and agree to the Terms of Service"),
        error_messages={"required": _("You must agree to the terms to register")},
    )


class ProfileForm(forms.ModelForm):
    class Meta:
            model = Profile
            exclude = ('valid', 'user', 'nickname')


def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r,r) for r in range(1960, datetime.date.today().year+10)]

class ExperienceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ExperienceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].choices = year_choices()
        self.fields['end_date'].choices = year_choices()

    class Meta:
        model = Experience
        fields = ['start_date', 'end_date', 'job_title', 'employer', 'city', 'country',  ]
        widgets = {
            'city': forms.TextInput(),
            'country': forms.TextInput(),
            'employer': forms.TextInput(),
            'job_title': forms.TextInput(),
            'start_date': forms.Select(choices=year_choices(), attrs={'class': 'form-control', 'style': 'width: 4em;'}),
            'end_date': forms.Select(choices=year_choices(), attrs={'class': 'form-control', 'style': 'width: 4em;'}),
            #    # Define other fields similarly
        }


ExperienceFormSet = inlineformset_factory(
    Profile,
    Experience,
    form=ExperienceForm,
    extra=1,  # Number of empty forms to display
    can_delete=True,  # Allows deletion of experiences
)

class AcademicForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AcademicForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].choices = year_choices()
        self.fields['end_date'].choices = year_choices()

    class Meta:
        model = Academic
        fields = ['start_date', 'end_date', 'phase', 'university', 'city', 'country',  ]
        widgets = {
            'city': forms.TextInput(),
            'country': forms.TextInput(),
            'university': forms.TextInput(),
            'phase': forms.Select(choices=[('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Ph.D.', 'Ph.D.'), ('Postdoc', 'Postdoc'), ('Faculty', 'Faculty'), ('Other', 'Other')], attrs={'class': 'form-control', 'style': 'width: 8em;'}),
            'start_date': forms.Select(choices=year_choices(), attrs={'class': 'form-control', 'style': 'width: 4em;'}),
            'end_date': forms.Select(choices=year_choices(), attrs={'class': 'form-control', 'style': 'width: 4em;'}),
            #    # Define other fields similarly
        }


AcademicFormSet = inlineformset_factory(
    Profile,
    Academic,
    form=AcademicForm,
    extra=1,  # Number of empty forms to display
    can_delete=True,  # Allows deletion of experiences
)
