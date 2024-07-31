from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class AccountManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("User need username")
        if not email:
            raise ValueError("User need email")
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
def profil_picture_path(instance, filename):
    return f'profile_pictures/{instance.pk}/profile_picture.png'


def default_profile_picture():
    return "default/default1.png"

class Account(AbstractBaseUser):

    username            = models.CharField(max_length=20, unique=True)
    email               = models.EmailField(verbose_name="email", max_length=60, unique=True)
    hide_email          = models.BooleanField(default=True)
    profile_picture     = models.ImageField(max_length=255, upload_to=profil_picture_path, null=True, blank=True, default=default_profile_picture)
    date_joined         = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login          = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active           = models.BooleanField(default=True)
    is_in_game          = models.BooleanField(default=False)
    is_admin            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_connected        = models.BooleanField(default=False)
    nb_win              = models.IntegerField(default=0)
    nb_loose            = models.IntegerField(default=0)
    nb_games            = models.IntegerField(default=0)
    coef                = models.IntegerField(default=40)
    elo                 = models.IntegerField(default=1000)
    nb_top8             = models.IntegerField(default=0)
    nb_top4             = models.IntegerField(default=0)
    nb_top2             = models.IntegerField(default=0)
    nb_top1             = models.IntegerField(default=0)
    highest_score       = models.IntegerField(default=0)

    objects = AccountManager()

    USERNAME_FIELD = 'email' # --> si on veut se connecter avec l'email plutot que le username
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def profile_picture_name(self):
        return str(self.profile_picture)[str(self.profile_picture).index(f'profile_picture/{self.pk}/'):]
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


    


