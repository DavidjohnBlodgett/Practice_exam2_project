from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]+')
NUM_REGEX = re.compile(r'\d+')

class UserManager(models.Manager):
    def _input_val(self,request):
        errors = {}
        # NAME
        # check name exists...
        if 'name' in request.POST:

            # check name length...
            if len(request.POST['name']) < 2:
                errors['name_len'] = 'User name should be more than 2 characters'

            # check chars...
            if not NAME_REGEX.match(request.POST['name']):
                errors['name_char'] = 'User name should only contain characters'
        else:
            errors['name_missing'] = 'User must enter a name'

        # EMAIL
        # check email exists...
        if 'email' in request.POST:

            # check if valid email...
            if not EMAIL_REGEX.match(request.POST['email']):
                errors['email_char'] = 'User email should be a valid email'

            # check for email already being used...
            test = User.objects.filter(email=request.POST['email'])
            if len(test) > 0:
                errors['user_collision'] = 'User with that email already exists'
        else:
            errors['email_missing'] = 'User must enter a valid email'

        # PASSWORD
        # check password exists...
        if 'password' in request.POST:

            # check name length...
            if len(request.POST['password']) < 5:
                errors['password_len'] = 'User password should be more than 5 characters'
        else:
            errors['password_missing'] = 'User must enter a password'

        # CONF_PASS
        # check conf_pass exists...
        if 'conf_pass' in request.POST:

            # check name length...
            if request.POST['conf_pass'] != request.POST['password']:
                errors['password_conf'] = 'Entered password and confirmation do not match'
        else:
            errors['conf_pass_missing'] = 'User must confirm password'

        return errors
    def create_user(self, request):
        errors = self._input_val(request)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return False
        else:
            newHash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            temp = User.objects.create(name=request.POST['name'],email=request.POST['email'],gold=0,password=newHash)
            temp.save()
            # auto login user...
            request.session['id'] = temp.id
            return True

    def login_user(self,request):
        try:
            temp = User.objects.get(email=request.POST['email'])
            if bcrypt.checkpw(request.POST['password'].encode(), temp.password.encode()):
                request.session['id'] = temp.id
            return True
        except:
            messages.error(request, 'Input incorrect password', extra_tags='bad_pass')
            return False

    def get_current_user(self,request):
        # maybe return info based on session id
        pass

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    gold = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # *************************
    objects = UserManager()
    # *************************


class Activity(models.Model):
    content = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name = 'activity')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
