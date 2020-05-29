from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class EmailOrUsernameModelBackend(object):
    User = settings.AUTH_USER_MODEL
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


from django.db.models import Q

from django.contrib.auth import get_user_model

MyUser = get_user_model()

class UsernameOrEmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
           # Try to fetch the user by searching the username or email field
            user = MyUser.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            MyUser().set_password(password)