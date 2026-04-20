from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from resume.matcher import calculate_match_score
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def job_list(request):
    jobs = Job.objects.filter(is_active=True)

    query = request.GET.get('q', '').strip()
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(required_skills__icontains=query)
        )

    jobs_with_scores = []
    has_resume = False

    if request.user.is_authenticated:
        try:
            user_resume = request.user.resume
            has_resume = True
            for job in jobs:
                job_text = f"{job.description} {job.required_skills}"
                score = calculate_match_score(user_resume.extracted_text, job_text)
                jobs_with_scores.append({'job': job, 'score': score})
            jobs_with_scores.sort(key=lambda x: x['score'], reverse=True)
        except Exception:
            jobs_with_scores = [{'job': j, 'score': None} for j in jobs]
    else:
        jobs_with_scores = [{'job': j, 'score': None} for j in jobs]

    context = {
        'jobs_with_scores': jobs_with_scores,
        'query': query,
        'has_resume': has_resume,
    }
    return render(request, 'jobs/list.html', context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    match_score = None
    already_applied = False

    if request.user.is_authenticated:
        try:
            user_resume = request.user.resume
            job_text = f"{job.description} {job.required_skills}"
            match_score = calculate_match_score(user_resume.extracted_text, job_text)
        except Exception:
            pass

        already_applied = Application.objects.filter(
            user=request.user, job=job
        ).exists()

    context = {
        'job': job,
        'match_score': match_score,
        'already_applied': already_applied,
    }
    return render(request, 'jobs/detail.html', context)


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)

    try:
        user_resume = request.user.resume
    except Exception:
        messages.warning(request, 'Please upload your resume first!')
        return redirect('upload_resume')

    if Application.objects.filter(user=request.user, job=job).exists():
        messages.info(request, 'You already applied for this job.')
        return redirect('my_applications')

    job_text    = f"{job.description} {job.required_skills}"
    match_score = calculate_match_score(user_resume.extracted_text, job_text)

    Application.objects.create(
        user=request.user,
        job=job,
        match_score=match_score,
    )

    messages.success(request, f'Applied to {job.title}! Match score: {match_score:.1f}%')
    return redirect('my_applications')


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        user=request.user
    ).select_related('job')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Account created! Welcome {user.username}!')
            return redirect('job_list')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    return render(request, 'registration/register.html', {})