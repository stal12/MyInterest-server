from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: No, never
        return False


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Person(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(Category)
    friends = models.ManyToManyField('self')
    pending_friends = models.ManyToManyField('self', symmetrical=False)    # richieste ricevute ma non ancora accettate
    image = models.URLField(null=True)


class Item(models.Model):
    link = models.URLField()
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    thumbnail = models.URLField(null=True)
    category = models.ForeignKey(Category)
    date = models.DateTimeField(auto_now=True)


class Post(models.Model):
    user = models.ForeignKey(Person, related_name='author')
    item = models.ForeignKey(Item)
    title = models.CharField(max_length=255)
    likes = models.ManyToManyField(Person)
    # tag


class Comment(models.Model):
    user = models.ForeignKey(Person)
    post = models.ForeignKey(Post)
    date = models.DateTimeField(auto_now=True)
    text = models.CharField(max_length=255)