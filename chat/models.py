from django.db import models

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    embedding = models.JSONField(null=True, blank=True)  # Store OpenAI vector
