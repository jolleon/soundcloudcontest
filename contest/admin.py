from django.contrib import admin
from contest.models import User, Contest, Submission, Vote

admin.site.register(User)
admin.site.register(Contest)
admin.site.register(Submission)
admin.site.register(Vote)
