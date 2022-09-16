from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default='Lorem ipsum')
    image = models.ImageField(
        upload_to='images/%d/%m/%Y/', blank=True, null=True)
    summary = models.TextField(default='Lorem ipsum dolor sit amet')
    content = models.TextField(default='Lorem ipsum dolor sit amet')
    category = models.CharField(max_length=100, default='test')
    publication_date = models.DateTimeField(default=datetime.now, blank=True)
    post_is_published = models.BooleanField()

    def __str__(self):
        return self.title
