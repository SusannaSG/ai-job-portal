from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Resume
from .matcher import extract_text, extract_skills_from_text, get_ranked_jobs
from jobs.models import Job


@login_required
def upload_resume(request):
    existing_resume = None
    try:
        existing_resume = request.user.resume
    except Exception:
        pass

    if request.method == 'POST':
        if 'resume_file' not in request.FILES:
            messages.error(request, 'Please select a file.')
            return redirect('upload_resume')

        uploaded_file = request.FILES['resume_file']

        allowed = ['.pdf', '.docx', '.doc', '.txt']
        ext = '.' + uploaded_file.name.split('.')[-1].lower()
        if ext not in allowed:
            messages.error(request, 'Only PDF, DOCX or TXT files allowed.')
            return redirect('upload_resume')

        if existing_resume:
            existing_resume.file = uploaded_file
            existing_resume.save()
            resume = existing_resume
        else:
            resume = Resume.objects.create(
                user=request.user,
                file=uploaded_file,
            )

        text = extract_text(resume.file.path)

        if not text.strip():
            messages.warning(request, 'Could not read text from file.')
            return redirect('upload_resume')

        resume.extracted_text = text
        resume.skills = extract_skills_from_text(text)
        resume.save()

        messages.success(request, 'Resume uploaded! Here are your matches.')
        return redirect('resume_matches')

    return render(request, 'resume/upload.html', {
        'existing_resume': existing_resume
    })


@login_required
def resume_matches(request):
    try:
        user_resume = request.user.resume
    except Exception:
        messages.warning(request, 'Please upload your resume first.')
        return redirect('upload_resume')

    jobs = Job.objects.filter(is_active=True)
    ranked_jobs = get_ranked_jobs(user_resume.extracted_text, jobs)

    return render(request, 'resume/matches.html', {
        'ranked_jobs': ranked_jobs,
        'resume': user_resume,
    })