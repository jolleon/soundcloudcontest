from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Contest(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_submission_closed = models.DateTimeField(null=True, blank=True)
    date_voting_closed = models.DateTimeField(null=True, blank=True) 

    admin = models.ForeignKey(User)

    def is_submission_open(self):
        return not self.date_submission_closed

    def is_voting_open(self):
        return self.date_submission_closed and not self.date_voting_closed

    def is_finished(self):
        if self.date_voting_closed:
            return True
        else:
            return False

    def status(self):
        if self.is_submission_open():
            return "Open"
        if self.is_voting_open():
            return "Voting"
        return "Finished"

    def __unicode__(self):
        return self.title

class Submission(models.Model):
    # SC URLs seem to be domain + username + title capped at 28 + 8 chars
    # assuming that stays below 200 chars which is the default
    sc_url = models.URLField()
    author = models.ForeignKey(User)
    contest = models.ForeignKey(Contest)
    date_created = models.DateTimeField(auto_now_add=True)

    # from SC
    username = models.CharField(max_length=100, null=True, blank=True)
    track_id = models.IntegerField(null=True, blank=True)
    user_id = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    uri = models.URLField(null=True, blank=True)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return self.sc_url

class Vote(models.Model):
    submission = models.ForeignKey(Submission)
    voter = models.ForeignKey(User)
    score = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

