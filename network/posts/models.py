from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='interesting_posts', blank=True)
    comment_to = models.ForeignKey('self', related_name='comments',blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.comment_to:
            return f'{self.author.username} post reply to {self.comment_to}'
        return f'{self.author.username} post'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})