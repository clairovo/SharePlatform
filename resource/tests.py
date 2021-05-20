from django.test import TestCase
import os
# Create your tests here.
from .models import Resource
path = 'E:\\receive\\resources'
course = Resource.objects.get(id=2)
print(course.path)
path = os.path.join(path,str(course.path))
print(path)
if not os.path.exists(path):
    print('no such path')
else:
    print('exit path')
