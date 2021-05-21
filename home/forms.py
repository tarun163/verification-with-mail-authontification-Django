
from django.contrib.auth.forms import UserCreationForm,User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1'] 