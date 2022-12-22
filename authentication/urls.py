from django.contrib.auth.views import LogoutView
from django.urls import path, include

from authentication import views
from authentication.api.router import router
from sgp import settings

app_name = 'authentication'
urlpatterns = [
    path('', views.SignInView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('redirect-session', views.redirect_session, name='redirect_session'),
]
