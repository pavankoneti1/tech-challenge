import random

from django.test import TestCase

# Create your tests here.
print(type(''.join(random.sample('012345689', 5))))