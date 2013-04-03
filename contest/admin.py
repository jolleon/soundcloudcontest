from django.contrib import admin
from contest.models import Contest, Submission, Vote, SoundcloudUser


class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'description', )

admin.site.register(Contest, ContestAdmin)

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('author', 'contest', 'sc_url', 'title')

admin.site.register(Submission, SubmissionAdmin)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('voter', 'contest', 'submission', 'score')
admin.site.register(Vote, VoteAdmin)

admin.site.register(SoundcloudUser)


# customize admin user
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# add some methods to User

# counting objects related to a user
# this will SO not scale...
def count_objects(model, user_field):
    def f(self):
        l = len(model.objects.filter(**{user_field: self}))
        return str(l) if l != 0 else ''
    f.func_name = model.__name__.lower() + 's'
    return f

User.add_to_class('contests', count_objects(Contest, 'admin'))
User.add_to_class('submissions', count_objects(Submission, 'author'))
User.add_to_class('votes', count_objects(Vote, 'voter'))

UserAdmin.list_display = ('username', 'first_name', 'soundclouduser', 'email', 'contests',
    'submissions', 'votes', 'last_login', 'is_staff')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
