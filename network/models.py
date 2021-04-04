from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", blank=True, symmetrical = False, related_name = "Ufollowing")
    followers = models.ManyToManyField("self", blank=True, symmetrical = False, related_name = "Ufollowers")
class Post(models.Model):
    PostCreator = models.ForeignKey(User, on_delete=models.CASCADE)
    PostContent = models.CharField(max_length=360, null=False)
    PostCreatedAt = models.DateTimeField(auto_now_add=True)
    PostLikes = models.IntegerField(default=0, null=False)

    def serialize(self):
        return {
            "id": self.id,
            "PostCreator": self.PostCreator.username,
            "PostContent": self.PostContent,
            "PostLikes": self.PostLikes,
        }

    def __str__(self):
        return f"{self.PostCreator}:{self.PostContent} at {self.PostCreatedAt}"
    

