import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.templatetags.static import static


def upload_avatar(instance, filename: str) -> str:
    return f'{instance.id}/avatars/{filename}'


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=25, null=True)
    email = models.EmailField('email address', unique=True)
    avatar = models.FileField(upload_to=upload_avatar, default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        # print('USER MODEL START SAVE METHOD')

        if not self.username:
            self.username = str(uuid.uuid4())

        super().save(*args, **kwargs)

        # print('USER MODEL FINISH SAVE METHOD')

    def avatar_url(self):
        if self.avatar:
            return self.avatar.url

        return static('img/def_avatar')
