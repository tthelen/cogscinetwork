from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
# import json_response from utils
from django.http import JsonResponse

from django.contrib.auth.models import User
from .models import Profile, Academic
from .forms import ProfileForm, CogsciNetworkRegistrationForm, ExperienceForm, ExperienceFormSet, AcademicForm, AcademicFormSet

from django_registration.backends.activation.views import RegistrationView

# class based django view for home
class HomeView(View):

    def get(self, request):

        # count the total number of valid members
        member_count = Profile.objects.filter(valid=True).count()

        # check if we have a logged in user
        if request.user.is_authenticated:
            if not request.user.profile.valid:
                # add django message: please update your profile
                messages.add_message(request, messages.INFO, 'Please update your profile. Fill all required fields and add your Cognitive Science at Universität Osnabrück related experiences.')
                # redirect to profile update page
                return redirect('profile_update', pk=request.user.profile.pk)

            # count how many users were active in the last 24 hours
            users_active_last_24h = Profile.objects.filter(last_activity__gte=timezone.now() - timezone.timedelta(days=1)).count()

            return render(request, "dbase/dashboard.html", {'user': request.user, 'users_active_last_24h': users_active_last_24h, 'member_count': member_count})
        else:
            return render(request, "dbase/home.html", {'member_count': member_count})



class SettingsView(LoginRequiredMixin, TemplateView):

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


class ProfileDetailsView(LoginRequiredMixin, TemplateView):

    template_name = 'dbase/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(pk=kwargs['pk'])
        return context


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dbase/profile_form.html'
    # fields = ["name"]


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
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
            data['academics'] = AcademicFormSet(self.request.POST, instance=self.object)
        else:
            data['experiences'] = ExperienceFormSet(instance=self.object)
            data['academics'] = AcademicFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        """If the form is valid, save the associated model.

        Addition: Make user profile valid. This is used for first-time profile update a
        nd for re-activation  after a certain time of inactivity.
        """
        form.instance.valid = False
        context = self.get_context_data()
        experiences = context['experiences']
        academics = context['academics']
        self.object = form.save()
        self.object.check_validity()
        if experiences.is_valid():
            experiences.instance = self.object
            experiences.save()
        else:
            pass
        if academics.is_valid():
            academics.instance = self.object
            academics.save()
        else:
            pass

        messages.add_message(self.request, messages.INFO, 'Profile updated')
        return super().form_valid(form)


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    form_class = ProfileForm
    template_name = 'dbase/profile_confirm_delete.html'
    success_url = reverse_lazy("author-list")


class MemberList(LoginRequiredMixin, ListView):

    model = Profile
    template_name = 'dbase/member_list.html'
    context_object_name = 'members'
    queryset = Profile.objects.filter(valid=True)
    paginate_by = 10

class SendMessageView(View):

    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'You must be logged in to send a message.'}, status=403)
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipient = request.POST.get('recipient')
        if not subject or not message or not recipient:
            return JsonResponse({'error': 'Subject and message are required.'}, status=400)
        # TODO: check if recipient allows messages!
        recipient = get_object_or_404(User, profile__pk=recipient)
        email = recipient.email
        # send email
        from django.core.mail import EmailMessage
        email_msg = EmailMessage(
            subject="[CogSci Network Message] "+subject,
            body=message+" \n\nThis message was sent by {} {} via the CogSci Network.".format(request.user.profile.firstname, request.user.profile.lastname),
            # from_email='cogsci-network@uni-osnabrueck.de',  # use default from email (configured in settings)
            to=[recipient.email],
            cc=[], # to send a copy to the sender for debugging:: request.user.email
            reply_to=[request.user.email]
        )
        print("Sending email to "+recipient.email)
        success = email_msg.send(fail_silently=False)
        if success:
            return JsonResponse({'success': 'Message sent to '+recipient.username}, status=200)
        else:
            return JsonResponse({'error': 'Could not send message.'}, status=500)