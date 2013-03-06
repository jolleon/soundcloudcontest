from django.contrib import admin
from contest.models import User, Contest, Submission, Vote


class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'description', )

admin.site.register(Contest, ContestAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('author', 'contest', 'sc_url', 'title')

admin.site.register(Submission, SubmissionAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'submission', 'score')
admin.site.register(Vote, VoteAdmin)
