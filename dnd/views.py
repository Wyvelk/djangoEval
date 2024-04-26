from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.template import loader
from django.contrib.auth.models import User
from .models import Skill



# Create your views here.
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