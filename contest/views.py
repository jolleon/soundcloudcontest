from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from forms import SubmissionForm

from contest.models import Contest
from contest.models import Submission

def index(request):
    contest_list = Contest.objects.all()
    return render(request, 'contest/index.html', {'contest_list': contest_list})


@login_required
def contest(request, contest_id):
    contest = get_object_or_404(Contest, pk=contest_id)
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
        return render(request, 'contest/submission.html', {'contest': contest, 'form': form})
