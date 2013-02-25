from django import forms

from models import Submission
from django.contrib.auth.models import User


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('sc_url',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'username', 'email', 'password'}
    password_confirm = forms.CharField(label=u'Password again')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Passwords didn't match.")

        return cleaned_data
