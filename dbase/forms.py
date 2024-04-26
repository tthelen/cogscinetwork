from .models import Profile, Experience
from django import forms
from django_registration.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _
from django.forms import inlineformset_factory


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


class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = ['city', 'country', 'employer', 'job_title', 'start_date', 'end_date']
        widgets = {
            'city': forms.TextInput(),
            'country': forms.TextInput(),
            'employer': forms.TextInput(),
            'job_title': forms.TextInput(attrs={'style': 'width: 200px;'}),
            'start_date': forms.TextInput(attrs={'style': 'width: 4em;'}),
            'end_date': forms.TextInput(attrs={'style': 'width: 4em;'}),
            # Define other fields similarly
        }


ExperienceFormSet = inlineformset_factory(
    Profile,
    Experience,
    form=ExperienceForm,
    extra=1,  # Number of empty forms to display
    can_delete=True  # Allows deletion of experiences
)