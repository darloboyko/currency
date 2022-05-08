import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.templatetags.static import static


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField('email address', unique=True)

    def save(self, *args, **kwargs):
        # print('USER MODEL START SAVE METHOD')

        if not self.username:
            self.username = str(uuid.uuid4())

        super().save(*args, **kwargs)

        # print('USER MODEL FINISH SAVE METHOD')
