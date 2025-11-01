# from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


# Create your views here.
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("login")
