from django.db import models

class NominationPost(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    is_posted = models.BooleanField('Posted', default=False)
    # Add any other fields as necessary

    def __str__(self):
        return f"{self.start_date} {self.start_time} - {self.end_date} {self.end_time}"

class ElectionPost(models.Model):
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    is_posted = models.BooleanField('Posted', default=False)
    # Add any other fields as necessary

    def __str__(self):
        return f"{self.start_date} {self.start_time} - {self.end_date} {self.end_time}"
    