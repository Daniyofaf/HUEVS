# # from django.contrib.auth.models import AbstractUser, UserManager
# # from django.db import models
# # from django.contrib.auth.hashers import make_password


# # class CustomUserManager(UserManager):
# #     def _create_user(self, email, password, **extra_fields):
# #         email = self.normalize_email(email)
# #         user = self.model(email=email, **extra_fields)
# #         user.set_password(password)
# #         user.save(using=self._db)
# #         return user

# #     def create_user(self, email, password=None, **extra_fields):
# #         extra_fields.setdefault("is_staff", False)
# #         extra_fields.setdefault("is_superuser", False)
# #         return self._create_user(email, password, **extra_fields)

# #     def create_superuser(self, email, password=None, **extra_fields):
# #         extra_fields.setdefault("is_staff", True)
# #         extra_fields.setdefault("is_superuser", True)
# #         extra_fields.setdefault("user_type", 1)  # Set default user type to Admin
# #         extra_fields.setdefault("last_name", "System")
# #         extra_fields.setdefault("first_name", "Administrator")

# #         assert extra_fields["is_staff"]
# #         assert extra_fields["is_superuser"]
# #         return self._create_user(email, password, **extra_fields)


# # class CustomUser(AbstractUser):
# #     USER_TYPE = ((1, "Admin"), (2, "Voter"), (3, "Board Member"), (4, "Candidate"))

# #     username = None

# #     # New fields
# #     first_name = models.CharField(max_length=50)
# #     middle_name = models.CharField(max_length=50)
# #     last_name = models.CharField(max_length=50)
# #     id_number = models.CharField(max_length=20)  
# #     email = models.EmailField(unique=True)
# #     # password = models.CharField(max_length=128)
# #     phone_number = models.CharField(
# #         max_length=15,
# #     )  # Provide a default value for phone_number
# #     # live_camera_photo = models.ImageField(
# #     #     upload_to="media\live_camera_photos/", null=True, blank=True
# #     # )
# #     # finger_data = models.BinaryField(null=True, blank=True)

# #     # Existing fields
# #     user_type = models.PositiveSmallIntegerField(default=2, choices=USER_TYPE)
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)
# #     cgpa = models.FloatField(null=True, blank=True)

# #     USERNAME_FIELD = "email"
# #     REQUIRED_FIELDS = []

# #     objects = CustomUserManager()

# #     def __str__(self):
# #         return f"{self.last_name} {self.first_name}"





# from django.contrib.auth.models import AbstractUser, UserManager
# from django.db import models


# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_user(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(email, password, **extra_fields)

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("user_type", 1)  # Set default user type to Admin
#         extra_fields.setdefault("last_name", "System")
#         extra_fields.setdefault("first_name", "Administrator")

#         assert extra_fields["is_staff"]
#         assert extra_fields["is_superuser"]
#         return self._create_user(email, password, **extra_fields)


# class CustomUser(AbstractUser):
#     USER_TYPE = ((1, "Admin"), (2, "Voter"), (3, "Board Member"), (4, "Candidate"))

#     username = None

#     # New fields
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     id_number = models.CharField(max_length=20)  
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15)  # Provide a default value for phone_number

#     # Existing fields
#     user_type = models.PositiveSmallIntegerField(default=2, choices=USER_TYPE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     cgpa = models.FloatField(null=True, blank=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = CustomUserManager()

#     def __str__(self):
#         return f"{self.last_name} {self.first_name}"



# class Candidate(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # Add additional fields specific to candidates
#     # For example:
#     # platform = models.TextField()

#     def __str__(self):
#         return self.user.get_full_name()


# class BoardMember(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # Add additional fields specific to board members
#     # For example:
#     # department = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user.get_full_name()




from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", 1)  # Set default user type to Admin
        extra_fields.setdefault("last_name", "System")
        extra_fields.setdefault("first_name", "Administrator")

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE = ((1, "Admin"), (2, "Voter"), (3, "Board Member"), (4, "Candidate"))

    username = None

    # New fields
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20)  
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)  # Provide a default value for phone_number

    # Existing fields
    user_type = models.PositiveSmallIntegerField(default=2, choices=USER_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cgpa = models.FloatField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# class Candidate(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # Add additional fields specific to candidates
#     # For example:
#     # platform = models.TextField()

#     def __str__(self):
#         return self.user.get_full_name()


# class BoardMember(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # Add additional fields specific to board members
#     # For example:
#     # department = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user.get_full_name()
