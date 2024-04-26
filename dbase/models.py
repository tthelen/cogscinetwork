from django.db import models


# Create your models here.
class Profile(models.Model):

    # link to django user
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    valid = models.BooleanField(default=False)  # is the profile valid and can be shown to others?

    nickname = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

#    name = models.CharField(max_length=200)
#    email = models.EmailField(max_length=200)
#    password = models.CharField(max_length=200)
#    bio = models.TextField()
#    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)#
#
#    def __str__(self):
#        return self.name

class Experience(models.Model):
    profile = models.ForeignKey(Profile, related_name='experiences', on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    job_title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title