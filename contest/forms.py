from django import forms

from models import Submission, Vote
from django.contrib.auth.models import User

import soundcloud

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ('sc_url',)

    def clean(self):
        cleaned_data = super(SubmissionForm, self).clean()
        sc_client = soundcloud.Client(client_id='296ab7d5973f378289cc72d56dc8eded')
        if not cleaned_data.get('sc_url'):
            return cleaned_data

        try:
            track = sc_client.get('/resolve', url=cleaned_data['sc_url'])
        except Exception, e:
            if e.response.status_code == 404:
                raise forms.ValidationError("Oops! This doesn't seem to be a valid SoundCloud link.")
            else:
                raise forms.ValidationError("Something terrible happened: " + e)

        cleaned_data['username'] = track.user['username']
        cleaned_data['track_id'] = track.id
        cleaned_data['user_id'] = track.user_id
        cleaned_data['title'] = track.title
        cleaned_data['uri'] = track.uri

        return cleaned_data

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


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = {'submission'}
    SCORES = (
            (0, ''),
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (6, '6'),
            (7, '7'),
            (8, '8'),
            (9, '9'),
            (10, '10'),
        )
    score = forms.ChoiceField(
            choices=SCORES,
            widget=forms.Select
        )

