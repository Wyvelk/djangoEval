from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.template import loader
from .models import Skill, DiceRoll, UserService, Wallet
from django.http import JsonResponse
from django.contrib.auth import logout
import random
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})

def rules(request):
    return render(request, 'rules.html')

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
            skill.save()
            wallet = Wallet(
                user=user,
                gold=100
            )
            wallet.save()
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
    
    end = False

    request.session['round'] += 1

    dice_roll = random.randint(1, 20)

    dice_target = random.randint(1, 20)

    skill = random.choice(skills)

    userSkill = getattr(Skill.objects.get(user=request.user), skill)

    modificateur = (userSkill - 10) // 2

    win = dice_roll + modificateur >= dice_target

    if(win):
        wallet = Wallet.objects.get(user=request.user)
        wallet.gold += 10
    else:
        wallet = Wallet.objects.get(user=request.user)
        wallet.gold -= 10
    wallet.save()

    if(request.session['round'] == 3 or request.session['life'] <= 0):
        end = True

    return JsonResponse({'end': end, 'dice_roll': dice_roll, 'skill': skill, 'win': win, 'dice_target': dice_target, 'modificateur': modificateur})

@login_required
def ranking(request):
    users = UserService.get_all_users_with_rolls_skills_and_wallets()
    return render(request, 'ranking.html', {'users': users})

@login_required
def Logout(request):
    logout(request)
    return redirect('login')

@login_required
def startAdventure(request):
    wallet = Wallet.objects.get(user=request.user)
    if request.method == "POST":
        difficulty = request.POST['adventure']
        request.session['round'] = 0
        request.session['bet'] = request.POST['bet']
        if difficulty == "easy":
            request.session['life'] = 3
            request.session['gain'] = float(request.POST['bet']) * 1.5
        elif difficulty == "medium":
            request.session['life'] = 2
            request.session['gain'] = float(request.POST['bet']) * 2.0
        elif difficulty == "hard":
            request.session['life'] = 1
            request.session['gain'] = float(request.POST['bet']) * 2.5
        return redirect('adventure')
    return render(request, 'startAdventure.html', {'wallet': wallet})

@login_required
def adventure(request):
    userSkills = Skill.objects.get(user=request.user)
    print(userSkills.strength)
    return render(request, 'adventure.html', {'life': range(request.session['life']), 'difficulty': request.session['difficulty'], 'userSkills': userSkills})

@login_required
def endAdventure(request):
    win = request.session['life'] > 0

    result = DiceRoll(
        user=request.user,
        skill="adventure",
        dice_roll=-1,
        win=win
    )
    result.save()

    wallet = Wallet.objects.get(user=request.user)
    if(win):
        wallet.gold += request.session['gain']
        wallet.save()
    else:
        wallet.gold -= request.session['bet']
        wallet.save()

    return render(request, 'endAdventure.html', {'win': win, 'gain': request.session['gain'], 'bet': request.session['bet'], 'wallet': wallet})