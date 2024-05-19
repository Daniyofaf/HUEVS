from django.db import models
from django.contrib.auth import get_user_model

class CampaignMessage(models.Model):
    candidate = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message = models.TextField()
    photo = models.ImageField(upload_to='campaign_photos/', null=True, blank=True)
    video = models.FileField(upload_to='campaign_videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.candidate}'s Campaign Message"
