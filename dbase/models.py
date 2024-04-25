from django.db import models


# Create your models here.
class Profile(models.Model):

    # link to django user
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    valid = models.BooleanField(default=False)  # is the profile valid and can be shown to others?

    nickname = models.CharField(max_length=200, blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    ba_start_year = models.IntegerField(null=True, blank=True)  # year of first year of BA
    ba_end_year = models.IntegerField(null=True, blank=True)  # year of last year of BA
    ma_start_year = models.IntegerField(null=True, blank=True)  # year of first year of MA
    ma_end_year = models.IntegerField(null=True, blank=True)  # year of last year of MA
    phd_start_year = models.IntegerField(null=True, blank=True)  # year of first year of PhD
    phd_end_year = models.IntegerField(null=True, blank=True)  # year of last year of PhD


#    name = models.CharField(max_length=200)
#    email = models.EmailField(max_length=200)
#    password = models.CharField(max_length=200)
#    bio = models.TextField()
#    #profile_pic = models.ImageField(upload_to='profile_pics', blank=True)#
#
#    def __str__(self):
#        return self.name
