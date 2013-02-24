from django.contrib import admin
from contest.models import User, Contest, Submission, Vote

admin.site.register(Vote)

class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'description', )

admin.site.register(Contest, ContestAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('author', 'contest', 'sc_url')

admin.site.register(Submission, SubmissionAdmin)
