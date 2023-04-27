from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User

print(User.objects.get(username="admin").promocode)
#profile = Profile.objects.create(user=User.objects.get(username="admin"))