
from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout
# Create your views here.

def home(request):
    # welcome_message = "Welcome to the Voting System!"

    # context = {
    #     # 'welcome_message': welcome_message,
    # }

    return render(request, "voting/homepage.html")


def account_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 1:
            return redirect(reverse("adminDashboard"))
        elif request.user.user_type == 2:
            return redirect(reverse("voterDashboard"))
        elif request.user.user_type == 3:
            return redirect(reverse("BoardMemberDashboard"))
        elif request.user.user_type == 4:
            return redirect(reverse("CandidateDashboard"))
        else:
            return redirect(reverse("account_login"))


    context = {}
    if request.method == 'POST':
        user = EmailBackend.authenticate(request, username=request.POST.get(
            'email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            if user.user_type == 1:
                return redirect(reverse("adminDashboard"))
            elif user.user_type == 2:
                return redirect(reverse("voterDashboard"))
            elif user.user_type == 3:
                return redirect(reverse("BoardMemberDashboard"))
            elif user.user_type == 4:
                return redirect(reverse("CandidateDashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("account_login")

    return render(request, "voting/login.html", context)








def account_register(request):
    if request.method == 'POST':
        userForm = CustomUserForm(request.POST)
        voterForm = VoterForm(request.POST)
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            user.user_type = 2  # Set user_type to Voter
            user.save()
            
            # Optionally, create a Voter instance and associate it with the user
            # Adjust this part based on your Voter model
            voter = voterForm.save(commit=False)
            voter.admin = user
            voter.save()

            messages.success(request, "Account created. You can login now!")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "") # Provided data failed validation
            # You might want to handle the error case here
            
    else:
        userForm = CustomUserForm()
        voterForm = VoterForm()
    
    context = {
        'form1': userForm,
        'form2': voterForm
    }
    return render(request, "voting/reg.html", context)


# def account_register(request):
#     userForm = CustomUserForm(request.POST or None)
#     voterForm = VoterForm(request.POST or None)
#     context = {
#         'form1': userForm,
#         'form2': voterForm
#     }
#     if request.method == 'POST':
#         if userForm.is_valid() and voterForm.is_valid():
#             # Print form data before saving
#             print("User Form Data:", userForm.cleaned_data)
#             print("Voter Form Data:", voterForm.cleaned_data)

#             user = userForm.save(commit=False)
#             voter = voterForm.save(commit=False)
#             voter.admin = user
#             user.save()
#             voter.save()

#             # Print form data after saving
#             print("User Form Data after saving:", userForm.cleaned_data)
#             print("Voter Form Data after saving:", voterForm.cleaned_data)

#             messages.success(request, "Account created. You can login now!")
#             return redirect(reverse('account_login'))
#         else:
#             messages.error(request, "")  # "Provided data failed validation"
#     return render(request, "voting/reg.html", context)





def account_logout(request):
    user = request.user
    if user.is_authenticated:
        logout(request)
        messages.success(request, "Thank you for visiting us!")
    else:
        messages.error(
            request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))


