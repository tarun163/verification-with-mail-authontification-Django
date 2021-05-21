from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_varified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class ForReset(models.Model):
    email = models.EmailField(max_length=254)
    auth_token = models.CharField( max_length=100)    

    def __str__(self):
        return self.user.email    