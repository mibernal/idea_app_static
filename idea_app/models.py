from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, editable=True)
    description = models.TextField(editable=True)
    image = models.ImageField(upload_to='ideas/', editable=True)
    software_idea = models.TextField(editable=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
exit
