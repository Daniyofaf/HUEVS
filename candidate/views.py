# board_member/views.py

from django.shortcuts import render

def dashboard(request):
    return render(request, 'candidate/dashboard.html')