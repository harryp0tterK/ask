from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


def avatar_size(avatar):
    """This validator is to ensure that avatar file is not too big. """

    limit = 1048576    # 1 mb per file upload limit
    if avatar.size > limit:
        raise ValidationError('The file is too large!')


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars/', default='no-image.png',
                               validators=[avatar_size])

    def save(self, *args, **kwargs):
        """need this custom method to delete obsolete avatar files from disk"""

        if self.pk:
            user = CustomUser.objects.get(pk=self.pk)
            if user.avatar and user.avatar.name != 'no-image.png':
                user.avatar.delete(save=False)
        super(CustomUser, self).save(*args, **kwargs)
