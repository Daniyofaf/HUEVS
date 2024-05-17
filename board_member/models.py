from django.db import models

class NominationPost(models.Model):
    start_date = models.DateField(max_length=50)
    start_time = models.TimeField(max_length=50)
    end_date = models.DateField(max_length=50)
    end_time = models.TimeField(max_length=50)
    is_posted = models.BooleanField('Posted', default=False)
    
    # Add any other fields as necessary

    def __str__(self):
        return f"{self.start_date} {self.start_time} - {self.end_date} {self.end_time}"

class ElectionPost(models.Model):
    start_date = models.DateField(max_length=50)
    start_time = models.TimeField(max_length=50)
    end_date = models.DateField(max_length=50)
    end_time = models.TimeField(max_length=50)
    is_posted = models.BooleanField('Posted', default=False)
    # Add any other fields as necessary

    def __str__(self):
        return f"{self.start_date} {self.start_time} - {self.end_date} {self.end_time}"
    
class ElectionResult(models.Model):
    isposted = models.BooleanField('isPosted', default=False)    
    
    
    