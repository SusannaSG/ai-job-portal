from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    title           = models.CharField(max_length=200)
    company         = models.CharField(max_length=200)
    location        = models.CharField(max_length=100)
    description     = models.TextField()
    required_skills = models.TextField()
    salary          = models.CharField(max_length=100, blank=True)
    job_type        = models.CharField(max_length=20, choices=[
        ('full_time',  'Full Time'),
        ('part_time',  'Part Time'),
        ('contract',   'Contract'),
        ('internship', 'Internship'),
    ], default='full_time')
    is_active  = models.BooleanField(default=True)
    posted_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.company}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied',     'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('rejected',    'Rejected'),
        ('hired',       'Hired'),
    ]
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    job         = models.ForeignKey(Job,  on_delete=models.CASCADE)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    match_score = models.FloatField(default=0.0)
    applied_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'job']

    def __str__(self):
        return f"{self.user.username} → {self.job.title}"