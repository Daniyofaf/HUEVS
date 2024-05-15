from django.shortcuts import render, redirect, reverse
from .email_backend import EmailBackend
from django.contrib import messages
# from .forms import CustomUserForm
from voting.forms import VoterForm
from django.contrib.auth import login, logout

# from .detection import FaceRecognition
from .forms import *


# Create your views here.

# faceRecognition = FaceRecognition()


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
            return redirect(reverse("board_member_dashboard"))
        elif request.user.user_type == 4:
            return redirect(reverse("candidatedashboard"))
        else:
            return redirect(reverse("account_login"))

    context = {}
    if request.method == "POST":
        user = EmailBackend.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user is not None:
            login(request, user)
            if user.user_type == 1:
                messages.success(request, "Welcome Back!")
                return redirect(reverse("adminDashboard"))
            elif user.user_type == 2:
                messages.success(request, "Welcome Back!")
                return redirect(reverse("voterDashboard"))
            elif user.user_type == 3:
                messages.success(request, "Welcome Back!")
                return redirect(reverse("board_member_dashboard"))
            elif user.user_type == 4:
                messages.success(request, "Welcome Back!")
                return redirect(reverse("candidatedashboard"))
        else:
            messages.error(request, "Invalid details")
            return redirect("account_login")

    # Perform face recognition
    # faceRecognition = FaceRecognition()
    # face_id = faceRecognition.recognizeFace()
    # if face_id:
    #     return redirect('greeting', str(face_id))  # Assuming 'greeting' is the URL pattern for the greeting page
    # else:
    #     messages.error(request, "Face recognition failed. Please login using email and password.")
    #     return redirect("account_login")

    return render(request, "voting/login.html", context)


# def account_register(request):
#     if request.method == "POST":
#         userForm = CustomUserForm(request.POST)
#         voterForm = VoterForm(request.POST)
#         if userForm.is_valid() and voterForm.is_valid():
#             user = userForm.save(commit=False)
#             user.user_type = 2  # Set user_type to Voter
#             user.save()

#             # Optionally, create a Voter instance and associate it with the user
#             # Adjust this part based on your Voter model
#             voter = voterForm.save(commit=False)
#             voter.admin = user
#             voter.save()

#             messages.success(request, "Account created. You can login now!")
#             return redirect(reverse("account_login"))
#         else:
#             messages.error(request, "")  # Provided data failed validation
#             # You might want to handle the error case here

#     else:
#         userForm = CustomUserForm()
#         voterForm = VoterForm()

#     context = {"form1": userForm, "form2": voterForm}
#     return render(request, "voting/reg.html", context)


# from Face_Detection.detection import addFace  # Import the function to add face data
# from Face_Detection.detection import FaceRecognition


def account_register(request):
    if request.method == "POST":
        userForm = CustomUserForm(request.POST)
        voterForm = VoterForm(request.POST)
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            user.user_type = 2  # Set user_type to Voter
            user.save()

            # Optionally, create a Voter instance and associate it with the user
            voter = voterForm.save(commit=False)
            voter.admin = user
            voter.save()

            # Add face registration
        #     face_id = request.POST.get('face_id')  # Assuming 'face_id' is the field in your form containing face data
        #     if face_id:
        #         addFace(face_id)  # Add the face data to the system

        #     messages.success(request, "Account created. You can login now!")
        #     return redirect(reverse("account_login"))
        # else:
        #     messages.error(request,
        #                    "Failed to create account. Please check your input.")  # Provided data failed validation

    else:
        userForm = CustomUserForm()
        voterForm = VoterForm()

    context = {"form1": userForm, "form2": voterForm}
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
        messages.error(request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))

