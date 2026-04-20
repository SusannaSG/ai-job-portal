from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jobs import views as job_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('resume/', include('resume.urls')),
    path('accounts/register/', job_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('jobs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)