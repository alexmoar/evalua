from django.urls import path

from administrator import views

app_name = 'administrator'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]
