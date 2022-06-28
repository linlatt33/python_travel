from django.forms import ModelForm
from .models import Places, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PlaceForm(ModelForm):
    class Meta:
        model = Places
        fields = '__all__'
        exclude = ['upload_by', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
