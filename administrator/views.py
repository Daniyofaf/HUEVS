from django.shortcuts import render, reverse, redirect
from administrator.models import SenateMembers
from voting.models import Voter, Position, Candidate, Votes
from account.models import CustomUser
from account.forms import CustomUserForm
from voting.forms import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
import json  # Not used
from django_renderpdf.views import PDFView


def find_n_winners(data, n):
    """Read More
    https://www.geeksforgeeks.org/python-program-to-find-n-largest-elements-from-a-list/
    """
    final_list = []
    candidate_data = data[:]
    # print("Candidate = ", str(candidate_data))
    for i in range(0, n):
        max1 = 0
        if len(candidate_data) == 0:
            continue
        this_winner = max(candidate_data, key=lambda x: x['votes'])
        # TODO: Check if None
        this = this_winner['name'] + \
            " with " + str(this_winner['votes']) + " votes"
        final_list.append(this)
        candidate_data.remove(this_winner)
    return ", &nbsp;".join(final_list)


class PrintView(PDFView):
    template_name = 'admin/print.html'
    prompt_download = True

    @property
    def download_name(self):
        return "result.pdf"

    def get_context_data(self, *args, **kwargs):
        title = "E-voting"
        try:
            file = open(settings.ELECTION_TITLE_PATH, 'r')
            title = file.read()
        except:
            pass
        context = super().get_context_data(*args, **kwargs)
        position_data = {}
        for position in Position.objects.all():
            candidate_data = []
            winner = ""
            for candidate in Candidate.objects.filter(position=position):
                this_candidate_data = {}
                votes = Votes.objects.filter(candidate=candidate).count()
                this_candidate_data['name'] = candidate.fullname
                this_candidate_data['votes'] = votes
                candidate_data.append(this_candidate_data)
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            # ! Check Winner
            if len(candidate_data) < 1:
                winner = "Position does not have candidates"
            else:
                # Check if max_vote is more than 1
                if position.max_vote > 1:
                    winner = find_n_winners(candidate_data, position.max_vote)
                else:

                    winner = max(candidate_data, key=lambda x: x['votes'])
                    if winner['votes'] == 0:
                        winner = "No one voted for this yet position, yet."
                    else:
                        """
                        https://stackoverflow.com/questions/18940540/how-can-i-count-the-occurrences-of-an-item-in-a-list-of-dictionaries
                        """
                        count = sum(1 for d in candidate_data if d.get(
                            'votes') == winner['votes'])
                        if count > 1:
                            winner = f"There are {count} candidates with {winner['votes']} votes"
                        else:
                            winner = "Winner : " + winner['name']
            print("Candidate Data For  ", str(
                position.name), " = ", str(candidate_data))
            position_data[position.name] = {
                'candidate_data': candidate_data, 'winner': winner, 'max_vote': position.max_vote}
        context['positions'] = position_data
        print(context)
        return context


def dashboard(request):
    positions = Position.objects.all().order_by('priority')
    candidates = Candidate.objects.all()
    voters = Voter.objects.all()
    voted_voters = Voter.objects.filter(voted=1)
    list_of_candidates = []
    votes_count = []
    chart_data = {}

    for position in positions:
        list_of_candidates = []
        votes_count = []
        for candidate in Candidate.objects.filter(position=position):
            list_of_candidates.append(candidate.fullname)
            votes = Votes.objects.filter(candidate=candidate).count()
            votes_count.append(votes)
        chart_data[position] = {
            'candidates': list_of_candidates,
            'votes': votes_count,
            'pos_id': position.id
        }

    context = {
        'position_count': positions.count(),
        'candidate_count': candidates.count(),
        'voters_count': voters.count(),
        'voted_voters_count': voted_voters.count(),
        'positions': positions,
        'chart_data': chart_data,
        'page_title': "Dashboard"
    }
    return render(request, "admin/home.html", context)


def voters(request):
    voters = Voter.objects.all()
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)
    context = {
        'form1': userForm,
        'form2': voterForm,
        'voters': voters,
        'page_title': 'Voters List'
    }
    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)
            voter.admin = user
            user.save()
            voter.save()
            messages.success(request, "New voter created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/voters.html", context)


def view_voter_by_id(request):
    voter_id = request.GET.get('id', None)
    voter = Voter.objects.filter(id=voter_id)
    context = {}
    if not voter.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        voter = voter[0]
        context['first_name'] = voter.admin.first_name
        context['last_name'] = voter.admin.last_name
        context['phone'] = voter.phone
        context['id'] = voter.id
        context['email'] = voter.admin.email
    return JsonResponse(context)


def view_position_by_id(request):
    pos_id = request.GET.get('id', None)
    pos = Position.objects.filter(id=pos_id)
    context = {}
    if not pos.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        pos = pos[0]
        context['name'] = pos.name
        context['max_vote'] = pos.max_vote
        context['id'] = pos.id
    return JsonResponse(context)


def updateVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Voter.objects.get(id=request.POST.get('id'))
        user = CustomUserForm(request.POST or None, instance=instance.admin)
        voter = VoterForm(request.POST or None, instance=instance)
        user.save()
        voter.save()
        messages.success(request, "Voter's bio updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))


def deleteVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        admin = Voter.objects.get(id=request.POST.get('id')).admin
        admin.delete()
        messages.success(request, "Voter Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))


def viewPositions(request):
    positions = Position.objects.order_by('-priority').all()
    form = PositionForm(request.POST or None)
    context = {
        'positions': positions,
        'form1': form,
        'page_title': "Positions"
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.priority = positions.count() + 1  # Just in case it is empty.
            form.save()
            messages.success(request, "New Position Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/positions.html", context)


def updatePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Position.objects.get(id=request.POST.get('id'))
        pos = PositionForm(request.POST or None, instance=instance)
        pos.save()
        messages.success(request, "Position has been updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewPositions'))


def deletePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Position.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Position Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewPositions'))


def viewCandidates(request):
    candidates = Candidate.objects.all()
    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {
        'candidates': candidates,
        'form1': form,
        'page_title': 'Candidates'
    }
    if request.method == 'POST':
        if form.is_valid():
            form = form.save()
            messages.success(request, "New Candidate Created")
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/candidates.html", context)


def updateCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        candidate_id = request.POST.get('id')
        candidate = Candidate.objects.get(id=candidate_id)
        form = CandidateForm(request.POST or None,
                             request.FILES or None, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Data Updated")
        else:
            messages.error(request, "Form has errors")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewCandidates'))


def deleteCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Candidate.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Candidate Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewCandidates'))


def view_candidate_by_id(request):
    candidate_id = request.GET.get('id', None)
    candidate = Candidate.objects.filter(id=candidate_id)
    context = {}
    if not candidate.exists():
        context['code'] = 404
    else:
        candidate = candidate[0]
        context['code'] = 200
        context['fullname'] = candidate.fullname
        previous = CandidateForm(instance=candidate)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)


def ballot_position(request):
    context = {
        'page_title': "Ballot Position"
    }
    return render(request, "admin/ballot_position.html", context)


def update_ballot_position(request, position_id, up_or_down):
    try:
        context = {
            'error': False
        }
        position = Position.objects.get(id=position_id)
        if up_or_down == 'up':
            priority = position.priority - 1
            if priority == 0:
                context['error'] = True
                output = "This position is already at the top"
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority+1))
                position.priority = priority
                position.save()
                output = "Moved Up"
        else:
            priority = position.priority + 1
            if priority > Position.objects.all().count():
                output = "This position is already at the bottom"
                context['error'] = True
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority-1))
                position.priority = priority
                position.save()
                output = "Moved Down"
        context['message'] = output
    except Exception as e:
        context['message'] = e

    return JsonResponse(context)


def ballot_title(request):
    from urllib.parse import urlparse
    url = urlparse(request.META['HTTP_REFERER']).path
    from django.urls import resolve
    try:
        redirect_url = resolve(url)
        title = request.POST.get('title', 'No Name')
        file = open(settings.ELECTION_TITLE_PATH, 'w')
        file.write(title)
        file.close()
        messages.success(
            request, "Election title has been changed to " + str(title))
        return redirect(url)
    except Exception as e:
        messages.error(request, e)
        return redirect("/")


def viewVotes(request):
    votes = Votes.objects.all()
    context = {
        'votes': votes,
        'page_title': 'Votes'
    }
    return render(request, "admin/votes.html", context)


def resetVote(request):
    Votes.objects.all().delete()
    Voter.objects.all().update(voted=False, verified=False, otp=None)
    messages.success(request, "All votes has been reset")
    return redirect(reverse('viewVotes'))



from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from account.forms import CustomUserForm, AdminCandidateCreationform
from account.models import *


def candidate_accounts(request):
    candidate_accounts = AdminCandidateCreation.objects.all()
    userForm = CustomUserForm(request.POST, request.FILES)
    candidate_accountsForm = AdminCandidateCreationform(request.POST, request.FILES)

    context = {
        "form1": userForm,
        "candidate_accounts": candidate_accounts,
        "page_title": "Candidate Accounts",
    }
    if request.method == "POST":
        if userForm.is_valid():
            user = userForm.save(commit=False)
            candidate_account = candidate_accountsForm.save(commit=False)
            candidate_account.admin = user
            user.user_type = 4  # Set user_type to candidate account creation
            user.save()
            candidate_account.save()
            messages.success(request, "New candidate account created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/candidate_account.html", context)


def view_candidate_account_by_id(request):
    candidate_account_id = request.GET.get("id", None)

    candidate_account = AdminCandidateCreation.objects.filter(
        id=candidate_account_id, user_type=4
    )

    context = {}
    if not candidate_account.exists():
        context["code"] = 404
    else:
        context["code"] = 200
        candidate_account = candidate_account[0]
        context["id"] = candidate_account.id
        context["first_name"] = candidate_account.first_name
        context["middle_name"] = candidate_account.middle_name
        context["last_name"] = candidate_account.last_name
        context["id_number"] = candidate_account.id_number
        context["email"] = candidate_account.email
        context["phone"] = (
            candidate_account.phone_number
        )  # Assuming phone_number is the correct field name
        # Add other fields as needed

    return JsonResponse(context)


def update_candidate_account(request):
    if request.method == "POST":
        candidate_account_id = request.POST.get("id")
        candidate_account = AdminCandidateCreation.objects.get(id=candidate_account_id)
        candidate_account.first_name = request.POST.get("first_name")
        candidate_account.last_name = request.POST.get("last_name")
        candidate_account.email = request.POST.get("email")
        candidate_account.phone_number = request.POST.get("phone")
        candidate_account.save()
        return redirect("adminViewCandidates")


def delete_candidate_account(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        # candidate_account = AdminCandidateCreation.objects.get(
        #     id=request.POST.get("id")
        # )

        admin = AdminCandidateCreation.objects.get("id").admin
        admin.delete()

        # candidate_account.delete()
        messages.success(request, "candidate account has been deleted")
    except:
        messages.error(request, "Access To This Resource Denied")
    return redirect(reverse("adminViewCandidates"))


from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from account.forms import *
from account.models import *


def board_members(request):
    board_member = BoardMember.objects.all()
    userForm = CustomUserForm(request.POST or None)
    board_memberForm = BoardMemberForm(request.POST or None)

    context = {
        "form1": userForm,
        "board_member": board_memberForm,
        "page_title": "Board Member Account",
    }
    if request.method == "POST":
        if userForm.is_valid():
            user = userForm.save(commit=False)
            board_member = board_memberForm.save(commit=False)
            board_member.admin = user
            user.user_type = 3  # Set user_type to Voter
            user.save()
            board_member.save()
            messages.success(request, "New board member created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/BoardMemberAccount.html", context)


def view_board_member_by_id(request):
    board_member_id = request.GET.get("id", None)
    # Filter BoardMember objects based on the custom user type
    board_member = BoardMember.objects.filter(id=board_member_id)
    context = {}
    if not board_member.exists():
        context["code"] = 404
    else:
        context["code"] = 200
        board_member = board_member[0]
        context["id"] = board_member.id
        context["first_name"] = board_member.admin.first_name
        context["middle_name"] = board_member.admin.middle_name
        context["last_name"] = board_member.admin.last_name
        context["email"] = board_member.admin.email
        context["phone"] = board_member.admin.phone_number
        # Add other fields as needed

    return JsonResponse(context)


def update_board_member(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        instance = BoardMember.objects.get(id=request.POST.get("id"))
        user = CustomUserForm(request.POST or None, instance=instance.admin)
        board_member = BoardMemberForm(request.POST or None, instance=instance)
        user.save()
        board_member.save()
        messages.success(request, "Board member's details updated")
    except:
        messages.error(request, "Access To This Resource Denied")
    return redirect(reverse("adminViewBoardMembers"))


def delete_board_member(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        admin = BoardMember.objects.get(id=request.POST.get("id")).admin
        admin.delete()
        messages.success(request, "Board member has been deleted")
    except:
        messages.error(request, "Access To This Resource Denied")
    return redirect(reverse("adminViewBoardMembers"))


from .forms import SenateMembersForm


def senate_members(request):
    senate_member = SenateMembers.objects.all()
    senatemembersForm = SenateMembersForm(request.POST or None)
    context = {
        "senate_members": senate_member,
        "senatemembersForm": senatemembersForm,
        "page_title": "Senate Members List",
    }
    if request.method == "POST":
        if senatemembersForm.is_valid():
            senate_members_instance = senatemembersForm.save()
            # senate_members.save()
            messages.success(request, "New Senate Member created")
        else:
            messages.error(request, "Form validation failed")
    return render(request, "admin/senatemember.html", context)


def view_senate_members_by_id(request):
    senate_members_id = request.GET.get("id", None)
    senate_member = SenateMembers.objects.filter(id=senate_members_id)
    context = {}
    if not senate_member.exists():
        context["code"] = 404
    else:
        context["code"] = 200
        senate_member = senate_member[0]
        context["id"] = senate_members.id
        context["first_name"] = senate_members.first_name
        context["middle_name"] = senate_members.middle_name
        context["last_name"] = senate_members.last_name
        context["id_number"] = senate_members.phone_number
        context["email"] = senate_members.email
        context["phone_number"] = senate_members.id_number
        context["cgpa"] = senate_members.cgpa
    return JsonResponse(context)


def update_senate_members(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        instance = SenateMembers.objects.get(id=request.POST.get("id"))
        senate_member = SenateMembersForm(request.POST or None, instance=instance)
        senate_member.save()
        messages.success(request, "senate_members bio updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse("adminViewSenateMembers"))


def delete_senate_members(request):
    if request.method != "POST":
        messages.error(request, "Access Denied")
    try:
        admin = SenateMembers.objects.get(id=request.POST.get("id")).admin
        admin.delete()
        messages.success(request, "Senate Member Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse("adminViewSenateMembers"))

from django.shortcuts import render
from voting.models import Nominee


def viewNominatedCandidates(request):
    nominated_candidates = Nominee.objects.all()
    return render(
        request,
        "admin/Nominatedcandidates.html",
        {"nominated_candidates": nominated_candidates},
    )
