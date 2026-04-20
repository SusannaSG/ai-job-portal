from django.db import models
from django.contrib.auth.models import User


class Resume(models.Model):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    file           = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True)
    skills         = models.TextField(blank=True)
    uploaded_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resume of {self.user.username}"

    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []