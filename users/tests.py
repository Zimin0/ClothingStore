from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Profile

# Create your tests here.
admin = User.objects.get(pk=1)
Profile.objects.create(user=admin)