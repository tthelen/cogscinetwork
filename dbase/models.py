from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Profile(models.Model):

    # link to django user
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    valid = models.BooleanField(default=False)  # is the profile valid and can be shown to others?
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    nickname = models.CharField(max_length=200, blank=True)
    pronouns = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    place = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    slogan = models.CharField(max_length=256, blank=True)

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

    def __str__(self):
        return self.user.username

#    name = models.CharField(max_length=200)
#    email = models.EmailField(max_length=200)
#    password = models.CharField(max_length=200)
#    bio = models.TextField()
#    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)#
#
#    def __str__(self):
#        return self.name


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
    phase = models.CharField(max_length=50, choices=[('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Ph.D.', 'Ph.D.'), ('Postdoc', 'Postdoc'), ('Faculty', 'Faculty'), ('Other', 'Other')])
    start_date = models.IntegerField('Start Year', validators=[MinValueValidator(1960), max_value_current_year], )
    end_date = models.IntegerField('End Year', validators=[MinValueValidator(1960), max_value_current_year])

    def __str__(self):
        return f"{self.phase} in {self.subject} at {self.university} ({self.start_date}-{self.end_date})"