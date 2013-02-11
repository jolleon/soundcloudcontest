from django.db import models

class User(models.Model):
    name = models.CharField(max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

class Contest(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_submission_closed = models.DateTimeField(null=True, blank=True)
    date_voting_closed = models.DateTimeField(null=True, blank=True) 

    admin = models.ForeignKey(User)

class Submission(models.Model):
    # SC URLs seem to be domain + username + title capped at 28 + 8 chars
    # assuming that stays below 200 chars which is the default
    sc_url = models.URLField()
    author = models.ForeignKey(User)
    date_created = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    submission = models.ForeignKey(Submission)
    voter = models.ForeignKey(User)
    score = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

