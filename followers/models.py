from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Follower(models.Model):

    owner = models.ForeignKey(related_name='following', on_delete=CASCADE)
    followed = models.ForeignKey(related_name='followed', on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} {self.followed}'
