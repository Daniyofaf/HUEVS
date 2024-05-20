from django.db import models
from account.models import CustomUser
# Create your models here.

from django.db import models
from cryptography.fernet import Fernet

class Voter(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, unique=True)  
    voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.admin.last_name}, {self.admin.first_name}"


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)
    priority = models.IntegerField()

    def __str__(self):
        return self.name


class Candidate(models.Model):
    fullname = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to="candidates")
    bio = models.TextField()
    video = models.FileField(upload_to='candidate_videos/', null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    
    # POSITIONS = (
    #     ('President', 'President'),
    #     # Add more positions as needed
    # )

    # fullname = models.CharField(max_length=50)
    # bio = models.TextField()
    # position = models.CharField(max_length=50, choices=POSITIONS, default='President')

    def __str__(self):
        return self.fullname



class Votes(models.Model):
    voter = models.ForeignKey(Voter, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    candidate = models.CharField(max_length=100)  # Assuming max length for candidate names

   

class Nominee(models.Model):
    POSITIONS = (
        ('President', 'President'),
        # Add more positions as needed
    )

    fullname = models.CharField(max_length=50)
    bio = models.TextField()
    position = models.CharField(max_length=50, choices=POSITIONS, default='President')
    is_approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.fullname


