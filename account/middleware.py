from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages

class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  # Who is the current user ?

        if user.is_authenticated:
            if user.user_type == 1:  # Admin
                if modulename.startswith('voting'):
                    if request.path != reverse('fetch_ballot'):
                        messages.error(request, "You do not have access to this resource")
                        return redirect(reverse('adminDashboard'))
            elif user.user_type == 2:  # Voter
                if modulename.startswith(('administrator', 'board_member', 'candidate')):
                    messages.error(request, "")
                    return redirect(reverse('voterDashboard'))
            elif user.user_type == 3:  # Board Member
                if modulename.startswith(('administrator', 'voting', 'candidate')):
                    messages.error(request, "")
                    return redirect(reverse('board_member_dashboard'))
            elif user.user_type == 4:  # Candidate
                if modulename.startswith(('administrator', 'voting', 'board_member')):
                    messages.error(request, "")
                    return redirect(reverse('candidatedashboard'))
            else:  # None of the aforementioned ? Please take the user to the login page
                return redirect(reverse('account_login'))
        else:
            # If the path is login or has anything to do with authentication, pass
            allowed_paths = [reverse('account_login'), reverse('account_register'), reverse('homepage')]
            if (request.path in allowed_paths or modulename.startswith('django.contrib.auth')):
                pass
            elif modulename.startswith(('voting', 'administrator', 'board_member', 'candidate')):
                # If a visitor tries to access voting, board, or candidate functions
                messages.error(request, "You need to be logged in to perform this operation")
                return redirect(reverse('account_login'))
            else:
                return redirect(reverse('account_login'))
