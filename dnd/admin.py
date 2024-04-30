from django.contrib import admin

# Register your models here.
from .models import Skill, DiceRoll, Wallet

class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma')

admin.site.register(Skill, SkillAdmin)


class DiceRollAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'dice_roll', 'win')

admin.site.register(DiceRoll, DiceRollAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'gold')

admin.site.register(Wallet, WalletAdmin)