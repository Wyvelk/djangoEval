from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Skill(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class DiceRoll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=50)
    dice_roll = models.IntegerField()
    win = models.BooleanField()

    def __str__(self):
        return self.user.username

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gold = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class UserService:
    @staticmethod
    def get_all_users_with_rolls_skills_and_wallets():
        users_with_rolls_skills_and_wallets = {}
        for user in User.objects.prefetch_related('diceroll_set', 'skill', 'wallet').order_by('wallet__gold').all():
            wins = user.diceroll_set.filter(win=True).count()
            lose = user.diceroll_set.filter(win=False).count()
            users_with_rolls_skills_and_wallets[user.username] = {
                'wins': wins,
                'lose': lose,
                'skills': {
                    'strength': user.skill.strength,
                    'dexterity': user.skill.dexterity,
                    'constitution': user.skill.constitution,
                    'intelligence': user.skill.intelligence,
                    'wisdom': user.skill.wisdom,
                    'charisma': user.skill.charisma,
                },
                'wallet': user.wallet.gold,
            }
        return users_with_rolls_skills_and_wallets
