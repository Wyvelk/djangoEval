from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.template import loader

# Create your views here.
def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def authView(request):
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})