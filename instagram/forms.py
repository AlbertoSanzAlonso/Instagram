from django.forms import ModelForm
from django.contrib.auth.models import User

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'username', 
            'email', 
            'password'
            ]
        