from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Post(models.Model):
    image = models.ImageField(upload_to='images')
    name = models.CharField(max_length=250)
    about = models.TextField(max_length=250, default='')
    address = models.CharField(max_length=250, default='')
    city = models.CharField(max_length=250, default='')
    state = models.CharField(max_length=250, default='')
    zip = models.IntegerField()

    def get_absolute_url(self):
        return reverse('UserPost:index', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Details(models.Model):
    model = models.ForeignKey(Post, on_delete=models.CASCADE)
    details = models.TextField(max_length=250)

    def get_absolute_url(self):
        return reverse('UserPost:index', kwargs={'pk': self.pk})

    def __str__(self):
        return self.details


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=100, default='')
    website = models.URLField(default='')
    profile_image = models.ImageField(upload_to='profile_image')

    def __str__(self):
        return self.user.username










