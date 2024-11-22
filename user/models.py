import re
from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver                                                                                                                                                                                                                                                                                                                                                                                                                                    



class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('O nome de usuário fornecido deve ser definido!'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username, email, password, True, True, **extra_fields)                                                                                                                     
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=15, unique=True,
                                                  help_text=_('Obrigatório. 15 caracteres ou menos. Letras, números e caracteres @/./+/-/_'),
                                 validators=[
                                     validators.RegexValidator(
                                       re.compile(r'^[\w.@+-]+$'),
                                         _('Insira um nome de usuário válido.'),
                                         _('inválido')
                                     )
                                 ])
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,  help_text=_('Designa se o usuário pode efetuar login neste site de administração.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designa se este usuário deve ser tratado como ativo.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

@receiver(post_save, sender=User)
def create_collection(sender, instance, created, **kwargs):
    if created:        
        from book.models import Collection         
        Collection.objects.create(name=f"Coleção de {instance.username}", collector=instance)
