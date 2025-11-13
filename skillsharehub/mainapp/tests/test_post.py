from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

import logging

from skillsharehub.mainapp.models import CustomUser, Chanel, Post
