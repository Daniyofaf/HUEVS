from django.db import models
from django.shortcuts import render, redirect


class SenateMembers(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)  
    cgpa = models.FloatField(max_length=20)
    # face_image = models.ImageField(upload_to='board_member_faces/')
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
