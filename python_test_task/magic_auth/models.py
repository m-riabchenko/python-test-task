from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    token = models.CharField(verbose_name="token auth user", unique=True, max_length=6)
    count_link = models.PositiveIntegerField(verbose_name="count link", default=0)
    count_total = models.PositiveIntegerField(verbose_name="count total link", default=0)
    is_active = models.BooleanField(
        'active',
        default=True,

    )
    is_staff = models.BooleanField(
        'staff',
        default=False,
    )

    is_admin = models.BooleanField(
        'superuser status',
        default=False,
        help_text='Designates whether this user can be a super user.'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
