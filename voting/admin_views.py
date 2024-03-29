from django.shortcuts import render
from account.views import account_login
# Create your views here.


# def index(request):
#     # if not request.user.is_authenticated:
#     #     return account_login(request)
#     # context = {}
#     return render(request, "voting/login.html")


# def index(request):
#     if not request.user.is_authenticated:
#         return account_login(request)
#     return render(request, "voting/login.html")


from django.shortcuts import render
from . import views


def index(request):
    if not request.user.is_authenticated:
        # User is not authenticated, render the homepage template
        return render(request, "voting\templates\voting\homepage.html")
    else:
        # User is authenticated, render the login page template
        return render(request, "voting/login.html")