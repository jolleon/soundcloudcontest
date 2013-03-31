from django.contrib.auth.models import User
import random
import string

from models import SoundcloudUser
import util

class SoundcloudBackend():

    def authenticate(self, code=None):
        print "in auth"
        if code == None:
            return None

        print "code:", code
        sc_client = util.get_soundcloud_client()
        access_token = sc_client.exchange_token(code)
        print "access_token:", access_token
        try:
            print "aaa"
            current_user = sc_client.get('/me')
            print "bbb"
        except Exception as e:
            print "exception:", e
        print "got user:", current_user.username

        try:
            sc_user = SoundcloudUser.objects.get(sc_id=current_user.id)
            print "got a sc user"
        except SoundcloudUser.DoesNotExist:
            # build username if the sc one is already taken
            username = current_user.username
            while User.objects.filter(username=username):
                username = username + "_"
            # create Django User
            user = User(username=username)
            # need to give it a password, ewwwww this is such a hack :(
            user.set_password(
                ''.join(
                    random.choice(string.ascii_letters)
                    for x in range(32)
                )
            )
            user.save()
            sc_user = SoundcloudUser(user=user)
            print "created users"

        sc_user.access_token = access_token

        sc_user.sc_id = current_user.id
        sc_user.username = current_user.username
        sc_user.permalink_url = current_user.permalink_url
        sc_user.uri = current_user.uri
        sc_user.city = current_user.city
        sc_user.country = current_user.country
        sc_user.avatar_url = current_user.avatar_url

        sc_user.save()

        # keep django username in sync with soudcloud's
        if sc_user.user.first_name != sc_user.username:
            sc_user.user.first_name = sc_user.username
            sc_user.user.save()

        print "returning user:", sc_user.user.username, sc_user.user.get_full_name()
        return sc_user.user


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
