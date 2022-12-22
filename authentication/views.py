from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from authentication.models import UserInformation
from evaluator.models import Evaluator


def redirect_session(request):
    if request.user.is_authenticated:
        user = UserInformation.objects.get(user_id=request.user.id)
        if user.role == UserInformation.ADMIN:
            return redirect(reverse_lazy('administrator:dashboard'))
        elif user.role == UserInformation.EVALUATOR:
            return redirect(reverse_lazy('evaluator:dashboard'))
        elif user.role == UserInformation.WRITER:
            return redirect(reverse_lazy('writer:projects'))
        else:
            messages.warning(request, 'Usuario sin rol para el sistema')
            return redirect(reverse_lazy('authentication:logout'))

    return redirect(reverse_lazy('authentication:login'))


class SignInView(View):
    template_name = "authentication/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('authentication:redirect_session'))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if User.objects.filter(username__exact=username).exists():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('authentication:redirect_session'))

        messages.warning(request, 'Usuario o contraseña incorrecto. Por favor intentalo de nuevo')
        return redirect(reverse_lazy('authentication:login'))


class SignUpView(View):
    template_name = "authentication/register.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        role = request.POST.get('role', None)
        password = request.POST.get('password', None)
        repeat_password = request.POST.get('repeat_password', None)
        user_exist = User.objects.filter(Q(username__exact=username) | Q(username__exact=email)).exists()
        message = None

        if user_exist:
            message = "Este usuario ya se encuentra registrado."
        elif not username or not first_name or not last_name or not email or not role:
            message = "Todos los campos son requeridos."
        elif not password or not repeat_password or password != repeat_password:
            message = "Las contraseñas no coinciden."

        if not message:
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()

            user_information = UserInformation(
                user=user,
                role=role
            )
            user_information.save()
            user = authenticate(request, username=username, password=password)

            if user_information.role == UserInformation.EVALUATOR:
                Evaluator.objects.create(user=user)

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('authentication:redirect_session'))
        else:
            messages.error(request, message)

        return redirect(reverse_lazy('authentication:register'))

