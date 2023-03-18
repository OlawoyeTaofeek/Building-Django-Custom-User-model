from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class CustomManager(BaseUserManager):
    #Creates and saves a User with the given email, username and password.

	def create_user(self, email, username, password=None):

		if not email:
			raise ValueError('The user must have email')
		if not username:
			raise ValueError('The user must have username')

		user = self.model(
			email = self.normalize_email(email),
			username = username.lower()

		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_staff(self, email, username, password):

    #Creates and saves a staff user with the given email, username and password.

		user = self.create_user(
			email = self.normalize_email(email),
			password=password,
			username=username.lower()
		)
		user.staff = True
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):

		user = self.create_user(
			email = self.normalize_email(email),
			username = username.lower(),
			password = password,
		)
		user.admin=True
		user.staff = True
		user.superuser = True

		user.save(using=self._db)
		return user



class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    

    # notice the absence of a "Password field", that is built in.

    objects = CustomManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ] # Email & Password are required by default.
   

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
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
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
	































