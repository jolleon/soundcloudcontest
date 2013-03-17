from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import urlresolvers
from django.utils import timezone

import soundcloud

import json

import forms
from contest.models import Contest
from contest.models import Submission
from contest.models import Vote

def index(request):
    contest_list = Contest.objects.all().order_by('-date_last_modified')
    return render(request, 'contest/index.html', {'contest_list': contest_list})

def contests(request):
    contests = Contest.objects.all().order_by('-date_last_modified')[4:]
    data = [{
        'title': contest.title,
        'id': contest.id,
        'url': urlresolvers.reverse('contest', args=(contest.id,)),
        'status': contest.status()
        } for contest in contests
    ]

    return render(request, 'contest/contest_table.html', {'contest_list': contests})

def contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
    sc_client = soundcloud.Client(client_id='296ab7d5973f378289cc72d56dc8eded')

    if not request.user.is_authenticated():
        return render(request, 'contest/contest.html', {'contest': contest})

    if contest.is_submission_open():
        # get existing submission for user if there is one
        submissions = Submission.objects.filter(contest=contest, author=request.user)
        existing_submission = submissions[0] if submissions else None
        submission = existing_submission
        # used for user feedback
        submission_success = False

        if request.method == 'POST':
            if existing_submission:
                # update existing submission
                form = forms.SubmissionForm(request.POST, instance=existing_submission)
            else:
                # create new submission
                form = forms.SubmissionForm(request.POST)
            if form.is_valid():
                # save what we have in db to get a Submission object
                submission = form.save(commit=False)
                # add missing fields
                submission.author = request.user
                submission.contest = contest
                submission.username = form.cleaned_data['username']
                submission.track_id = form.cleaned_data['track_id']
                submission.user_link = form.cleaned_data['user_link']
                submission.user_id = form.cleaned_data['user_id']
                submission.title = form.cleaned_data['title']
                submission.uri = form.cleaned_data['uri']
                # save with added fields
                submission.save()
                submission_success = True
            else:
                # get back the good one if there was one
                submissions = Submission.objects.filter(contest=contest,
                        author=request.user)
                submission = submissions[0] if submissions else None

        else: #GET
            form = forms.SubmissionForm()

        return render(request, 'contest/submission.html',
                {'contest': contest,
                    'form': form,
                    'submission': submission,
                    'success': submission_success})

    elif contest.is_voting_open():
        if request.method == 'POST':
            form = forms.VoteForm(request.POST)
            if form.is_valid():
                if form.cleaned_data['score'] != '0':
                    vote, created = Vote.objects.get_or_create(
                            voter=request.user,
                            submission=form.cleaned_data['submission'],
                            defaults={'score':form.cleaned_data['score']}
                        )
                    if not created:
                        # defaults have been ignored, need to override
                        vote.score = form.cleaned_data['score']
                        vote.save()
                else:
                    # if there is a vote we need to delete it
                    Vote.objects.filter(voter=request.user,
                        submission=form.cleaned_data['submission']
                    ).delete()
        else: #GET
            pass
        submissions = Submission.objects.filter(contest=contest)
        for submission in submissions:
            votes = Vote.objects.filter(
                    submission=submission,
                    voter=request.user)
            # TODO: should probably do something if there is more than 1
            vote = votes[0] if votes else None
            submission.score = vote.score if vote else ''
            submission.form = forms.VoteForm()
            submission.form.fields['score'].initial = submission.score
        return render(request, 'contest/voting.html',
                {'contest': contest, 'submissions': submissions})


    else:
        submissions = Submission.objects.filter(contest=contest)
        for submission in submissions:
            votes = Vote.objects.filter(submission=submission)
            scores = [vote.score for vote in votes]
            submission.n_votes = len(scores)
            if scores:
                submission.max = max(scores)
                submission.min = min(scores)
                submission.average = (sum(scores) * 100 / len(scores)) * 0.01
            else:
                submission.average = 0

        sorted_submissions = sorted(submissions, key=lambda s: -s.average)
        return render(request, 'contest/results.html',
                {'contest': contest, 'submissions': sorted_submissions})


def signin(request):
    if request.method == 'GET':
        form = forms.UserForm(initial={'username': '', 'email': ''})
        form['username'].value = ''
        return render(request, 'contest/signin.html', {'form': form})

    if request.method == 'POST':
        form = forms.UserForm(request.POST)
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


@login_required
def profile(request):
    contests = Contest.objects.filter(admin=request.user)
    submissions = Submission.objects.filter(author=request.user)
    votes = Vote.objects.filter(voter=request.user)

    context = {
        'contests': contests,
        'submissions': submissions,
        'votes': votes
    }
    return render(request, 'contest/profile.html', context)


@login_required
def edit(request, contest_id):
    if request.method == 'POST':
        form = forms.ContestForm(request.POST)
        if form.is_valid():
            if contest_id == '0':
                # new contest creation
                contest = Contest(
                    admin=request.user,
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description']
                )
                contest.save()
                contest_id = contest.id
            else:
                contest = get_object_or_404(
                        Contest,
                        pk=contest_id,
                        admin=request.user
                    )
                contest.title = form.cleaned_data['title']
                contest.description = form.cleaned_data['description']
                if form.cleaned_data['close']:
                    if contest.is_submission_open():
                        contest.date_submission_closed = timezone.now()
                    elif contest.is_voting_open():
                        contest.date_voting_closed = timezone.now()
                    else:
                        # TODO: should probably log an error or something
                        pass
                contest.save()
            return redirect('contest', contest.id)
        else: # form not valid
            if contest_id != '0': # '0' is for new contest creation
                contest = get_object_or_404(Contest, pk=contest_id, admin=request.user)
            else:
                # creating new contest
                contest = Contest(id=0)


    else: # GET request
        if contest_id != '0': # '0' is for new contest creation
            contest = get_object_or_404(Contest, pk=contest_id, admin=request.user)
            # at this point we have the correct contest and the user is its admin
            form = forms.ContestForm(initial={'title': contest.title, 'description': contest.description})
        else:
            # creating new contest
            form = forms.ContestForm()
            contest = Contest(id=0)

    return render(request, 'contest/edit.html', {'form': form, 'contest': contest})
