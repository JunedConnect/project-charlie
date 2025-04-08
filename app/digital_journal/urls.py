"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from journals import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),

    path('journals/', views.JournalsView.as_view(), name='journals_home'),
    path('journals/create_journal/', views.CreateJournalView.as_view(), name='create_journal'),
    path('journals/<int:journal_id>/entries', views.EntriesView.as_view(), name='view_journal_entries'),
    path('journals/<int:journal_id>/download_journal_pdf', views.DownloadJournalPDF.as_view(), name='download_journal_pdf'),
    path('journals/<int:journal_id>/create_entry', views.CreateEntryView.as_view(), name='create_entry'),
    path('journals/<int:journal_id>/entries/<int:entry_id>/edit', views.EditEntryView.as_view(), name='edit_entry'),
    path('journals/<int:journal_id>/entries/<int:entry_id>/view', views.ViewEntryView.as_view(), name='view_entry'),
    path('journals/<int:journal_id>/entries/<int:entry_id>/download_entry_pdf', views.DownloadEntryPDF.as_view(), name='download_entry_pdf'),
    path('custom_template/', views.CustomTemplateView.as_view(), name='custom_template'),
    path('journals/<int:journal_id>/delete_journal/', views.DeleteJournalView.as_view(), name='delete_journal'),
    path('journals/entries/<int:entry_id>/delete/', views.DeleteEntryView.as_view(), name='delete_entry'),

    path('journals/entries/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Create image directory for profile pictures
 