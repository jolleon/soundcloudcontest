from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


from forms import SubmissionForm
from forms import UserForm

from contest.models import Contest
from contest.models import Submission

def index(request):
    contest_list = Contest.objects.all()
    return render(request, 'contest/index.html', {'contest_list': contest_list})


def contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)

    if not request.user.is_authenticated():
        return render(request, 'contest/contest.html', {'contest': contest})

    submissions = Submission.objects.filter(contest=contest, author=request.user)
    
    submission = submissions[0] if submissions else None
    submission_success = False
    
    if contest.is_submission_open():
        if request.method == 'POST':
            if submission:
                form = SubmissionForm(request.POST, instance=submission)
            else:
                form = SubmissionForm(request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.author = request.user
                submission.contest = contest
                submission.save()
                submission_success = True

        else: #GET
            form = SubmissionForm()

        return render(request, 'contest/submission.html', {'contest': contest, 'form': form, 'submission': submission, 'success': submission_success})

    else:
        submissions = Submission.objects.filter(contest=contest)

        return render(request, 'contest/voting.html', {'contest': contest, 'submissions': submissions})


def signin(request):
    if request.method == 'GET':
        form = UserForm(initial={'username': '', 'email': ''})
        form['username'].value = ''
        return render(request, 'contest/signin.html', {'form': form})

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = user.password
            user.set_password(user.password) # need that to hash it
            user.save()
            auth_user = authenticate(username=user.username, password=password)
            if auth_user is not None:
                login(request, auth_user)
            return redirect('/')
        else:
            return render(request, 'contest/signin.html', {'form': form})
            
        
