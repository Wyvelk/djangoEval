from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from .models import Skill, DiceRoll
from django.http import JsonResponse
from django.contrib.auth import logout
import random
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            skill = Skill(
                user=user,
                strength=request.POST['strength'],
                dexterity=request.POST['dexterity'],
                constitution=request.POST['constitution'],
                intelligence=request.POST['intelligence'],
                wisdom=request.POST['wisdom'],
                charisma=request.POST['charisma']
            )
            skill.save()  # Sauvegardez les compétences dans la base de données
            return redirect('login')
    else:
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

@login_required
def dice(request):
    return render(request, 'dice.html')

@login_required
def roll_dice(request):
    skills = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']

    dice_roll = random.randint(1, 20)

    skill = random.choice(skills)

    win = dice_roll <= getattr(Skill.objects.get(user=request.user), skill)

    result = DiceRoll(
        user=request.user,
        skill=skill,
        dice_roll=dice_roll,
        win=win
    )
    result.save()

    return JsonResponse({'dice_roll': dice_roll, 'skill': skill, 'win': win})

@login_required
def ranking(request):
    users = User.objects.all()
    skills = Skill.objects.all()
    dice_rolls = DiceRoll.objects.all()
    return render(request, 'ranking.html', {'users': users, 'skills': skills, 'dice_rolls': dice_rolls})

@login_required
def Logout(request):
    logout(request)
    return redirect('login')