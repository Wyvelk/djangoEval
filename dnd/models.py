from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    def __str__(self):
        return self.user.username