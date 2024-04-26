from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .models import Profile
from .forms import ProfileForm, CogsciNetworkRegistrationForm, ExperienceForm, ExperienceFormSet

from django_registration.backends.activation.views import RegistrationView


# class based django view for home
class HomeView(View):

    def get(self, request):
        # check if we have a logged in user
        if request.user.is_authenticated:
            if not request.user.profile.valid:
                # add django message: please update your profile
                messages.add_message(request, messages.INFO, 'Please update your profile')
                # redirect to profile update page
                return redirect('profile_update', pk=request.user.pk)
            return render(request, "dbase/dashboard.html", {'user': request.user})
        else:
            return render(request, "dbase/home.html", {})


class SettingsView(TemplateView):

    template_name = 'dbase/settings.html'


class CogsciNetworkRegistrationView(RegistrationView):
    form_class = CogsciNetworkRegistrationForm

    def create_inactive_user(self, form):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.save()
        # create empty profile for new user
        new_user.profile = Profile()
        new_user.profile.valid = False
        new_user.profile.save()

        self.send_activation_email(new_user)

        return new_user



class ProfileDetailsView(TemplateView):

    template_name = 'dbase/networkuser_show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=kwargs['pk'])
        return context


class ProfileCreateView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dbase/profile_form.html'
    # fields = ["name"]


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dbase/profile_form.html'
    # all fields except user and valid
    exclude = ('user', 'valid')
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['experiences'] = ExperienceFormSet(self.request.POST, instance=self.object)
        else:
            data['experiences'] = ExperienceFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """If the form is valid, save the associated model.

        Addition: Make user profile valid. This is used for first-time profile update a
        nd for re-activation  after a certain time of inactivity.
        """
        form.instance.valid = True
        messages.add_message(self.request, messages.INFO, 'Profile updated')
        context = self.get_context_data()
        experiences = context['experiences']
        self.object = form.save()
        if experiences.is_valid():
            experiences.instance = self.object
            experiences.save()
        return super().form_valid(form)



class ProfileDeleteView(DeleteView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dbase/profile_confirm_delete.html'
    success_url = reverse_lazy("author-list")


class MemberList(ListView):

    model = Profile
    template_name = 'dbase/member_list.html'
    context_object_name = 'members'
    queryset = Profile.objects.filter(valid=True)
    paginate_by = 10