"""Test specific models."""

from django.db import models

class Question(models.Model):
    pass

class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    votes = models.IntegerField(default=0)
