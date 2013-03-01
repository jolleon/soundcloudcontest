from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

import soundcloud

from forms import SubmissionForm, UserForm, VoteForm

from contest.models import Contest
from contest.models import Submission

def index(request):
    contest_list = Contest.objects.all()
    return render(request, 'contest/index.html', {'contest_list': contest_list})


def contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    sc_client = soundcloud.Client(client_id='296ab7d5973f378289cc72d56dc8eded')

    if not request.user.is_authenticated():
        return render(request, 'contest/contest.html', {'contest': contest})

    if contest.is_submission_open():
        # get existing submission for user if there is one
        submissions = Submission.objects.filter(contest=contest, author=request.user)
        existing_submission = submissions[0] if submissions else None
        # used for user feedback
        submission_success = False

        if request.method == 'POST':
            if existing_submission:
                # update existing submission
                form = SubmissionForm(request.POST, instance=existing_submission)
            else:
                # create new submission
                form = SubmissionForm(request.POST)
            if form.is_valid():
                # save what we have in db to get a Submission object
                submission = form.save(commit=False)
                # add missing fields
                submission.author = request.user
                submission.contest = contest
                submission.username = form.cleaned_data['username']
                submission.track_id = form.cleaned_data['track_id']
                submission.user_id = form.cleaned_data['user_id']
                submission.title = form.cleaned_data['title']
                submission.uri = form.cleaned_data['uri']
                # save with added fields
                submission.save()
                submission_success = True

        else: #GET
            form = SubmissionForm()

        # ugly
        submissions = Submission.objects.filter(contest=contest, author=request.user)
        submission = submissions[0] if submissions else None
        return render(request, 'contest/submission.html',
                {'contest': contest,
                    'form': form,
                    'submission': submission,
                    'success': submission_success})

    elif contest.is_voting_open():
        if request.method == 'POST':
            pass
        else: #GET
            submissions = Submission.objects.filter(contest=contest)
            for submission in submissions:
                submission.form = VoteForm()
        return render(request, 'contest/voting.html',
                {'contest': contest, 'submissions': submissions})



    else:
        submissions = Submission.objects.filter(contest=contest)

        return render(request, 'contest/voting.html',
                {'contest': contest, 'submissions': submissions})


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
            
        
