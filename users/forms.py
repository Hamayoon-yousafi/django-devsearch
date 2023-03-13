from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for label, field in self.fields.items():
            if label == 'username':
                field.widget.attrs.update({'autofocus': 'false'})
            if label == 'first_name':
                field.widget.attrs.update({'autofocus': 'true'})
            field.widget.attrs.update({'class': 'input'})