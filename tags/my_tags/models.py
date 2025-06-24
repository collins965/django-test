from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Editor model
class Editor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='editors/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Blog model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
