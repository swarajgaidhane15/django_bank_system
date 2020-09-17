from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",
                  "username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class AddTransaction(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("amount", "description", "trans_type")
