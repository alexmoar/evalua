from django.urls import path

from writer import views

app_name = 'writer'
urlpatterns = [
    path('', views.ProjectsDashboardView.as_view(), name='projects'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('projects/edit/<int:id>', views.ProjectsEditView.as_view(), name='edit_project'),
    path('projects/add/', views.AddProjectView.as_view(), name='add_project'),
]
