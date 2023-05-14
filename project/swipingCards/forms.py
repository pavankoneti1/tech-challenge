from django.forms import ModelForm
from .models import *

class SignupForm(ModelForm):
    class Meta:
        model = LoginModel
        fields = '__all__'