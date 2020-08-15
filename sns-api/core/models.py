from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

def upload_path(instance, filename):
    """To be used for profile image"""
    # split file extension and store it
    ext = filename.split('.')[-1]
    
    # Add 'image' folder under the '_media' folder 
    # and then normalize the filename as below    
    return '/'.join(['image', str(instance.base_user.id)+ '_' +str(instance.name)+str('.')+str(ext)])    


class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Profile model"""
    name = models.CharField(max_length=50)
    base_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='base_user',
        on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_path)

    def __str__(self):
        return self.name


class FriendRequest(models.Model):
    """Friend Request model"""
    requestFrom = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='requestFrom',
        on_delete=models.CASCADE
    )
    requestTo = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='requestTo',
        on_delete=models.CASCADE
    )
    approved = models.BooleanField(default=False)

    """Sets of field names that are taken together, must be unique"""
    class Meta:
        unique_together = (('requestFrom', 'requestTo'),)

    def __str__(self):
        return str(self.requestFrom) + ' --> ' + str(self.requestTo)


class Message(models.Model):
    """Message model"""
    message = models.CharField(max_length=150)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sender',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='receicer',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return 'From : ' + str(self.sender.base_user)


class Post(models.Model):
    """Post model"""
    content = models.CharField(max_length=150)
    postBy = models.ForeignKey(
        'Profile',
        related_name='postBy',
        on_delete=models.CASCADE
    )
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.postBy) + ' : ' + self.content