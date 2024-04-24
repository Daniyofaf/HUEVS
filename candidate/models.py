from django.db import models
from django.contrib.auth import get_user_model

class CampaignMessage(models.Model):
    candidate = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate}'s Campaign Message"
