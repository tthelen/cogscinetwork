from .models import Profile
from django import forms
from django_registration.forms import RegistrationForm
from django.utils.translation import gettext_lazy as _


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

    def clean(self):
        cd = self.cleaned_data

        if not cd['ba_start_year'] \
                and not cd['ba_end_year'] \
                and not cd['ma_start_year'] \
                and not cd['ma_end_year'] \
                and not cd['phd_start_year'] \
                and not cd['phd_end_year']:
            raise forms.ValidationError('Please provide at least one date range')
        return cd
