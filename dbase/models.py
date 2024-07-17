from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import FileExtensionValidator

# import uuid4
from uuid import uuid4

def profile_pic_filename(instance, filename):
    ext = filename.split('.')[-1]
    return 'profile_pics/{}.{}'.format(uuid4().hex, ext)


# Create your models here.
class Profile(models.Model):

    # link to django user
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)  # is the profile valid and can be shown to others?
    last_activity = models.DateTimeField(auto_now=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, blank=True)
    pronouns = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=200, blank=True)
    slogan = models.CharField(max_length=256, blank=True)
    bio = models.TextField(null=True, blank=True)
    homepage = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    instagram = models.URLField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    profile_pic = models.ImageField(upload_to=profile_pic_filename, validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])], blank=True)

    def check_validity(self):
        """
        Check if the profile is valid. A profile is valid if it has at least one entry in academics or experiences with "Osnabrück".
        Sets the valid object variable.

        :return: True if the profile is valid, False otherwise
        """
        # we need at least one entry in academics or experiences with "Osnabrück"
        if self.academics.filter(university='Universität Osnabrück').exists() or self.experiences.filter(city='Osnabrück').exists():
            self.valid = True
            self.save()
        else:
            self.valid = False
            self.save()
        return self.valid

    def get_memberlist_string(self):
        """
        Returns a string for the memberlist, e.g. "Tobias Thelen (Cognitive Science)"
        :return: string
        """
        for acad in self.academics.order_by('-start_date'):
            if acad.university == 'Universität Osnabrück':
                return acad.__str__()
        for exp in self.experiences.order_by('-start_date'):
            if exp.city == 'Osnabrück':
                return exp.__str__()
        return "ERROR: No academic or experience entry with Osnabrück found."

    def __str__(self):
        return self.user.username


def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experiences', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)
    start_date = models.IntegerField('Start Year', validators=[MinValueValidator(1960), max_value_current_year], )
    end_date = models.IntegerField('End Year', validators=[MinValueValidator(1960), max_value_current_year])

    def __str__(self):
        return f"{self.job_title} at {self.employer} ({self.start_date}-{self.end_date})"

class Academic(models.Model):
    profile = models.ForeignKey(Profile, related_name='academics', on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    phase = models.CharField(max_length=50)
    start_date = models.IntegerField('Start Year', validators=[MinValueValidator(1960), max_value_current_year], )
    end_date = models.IntegerField('End Year', validators=[MinValueValidator(1960), max_value_current_year])

    def __str__(self):
        return f"{self.phase} {self.subject}, {self.university} ({self.start_date}-{self.end_date})"