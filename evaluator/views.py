import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from authentication.models import UserInformation
from evaluator.evaluator_controller import EvaluatorController
from evaluator.models import Evaluator
from projects.models import Score, Project


class DashboardView(LoginRequiredMixin, View):
    template_name = "evaluator/dashboard.html"

    def get(self, request, *args, **kwargs):
        to_evaluate = Score.objects.filter(
            evaluator__user=request.user,
            project__status=Project.SEND
        )
        return render(request, self.template_name, {'to_evaluate': to_evaluate})

    def post(self, request, *args, **kwargs):
        pass


class ProjectsQualifiedView(LoginRequiredMixin, View):
    template_name = "evaluator/project_qualified.html"

    def get(self, request, *args, **kwargs):
        id_project = kwargs.get('id_project')
        is_assigned = Score.objects.filter(
            evaluator__user=request.user,
            project__status=Project.SEND,
            project_id=id_project,
        ).exists()
        if not is_assigned:
            return redirect(reverse_lazy('evaluator:dashboard'))

        user = UserInformation.objects.get(user_id=request.user.id)
        project = Project.objects.get(id=kwargs.get('id_project'))
        return render(request, self.template_name, {
            'user': user,
            'project': project,
        })


class ProjectScoresQuestionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            status=200,
            data=EvaluatorController.get_score_project(kwargs.get('id_project'), request)
        )


class ProjectQuestionsView(LoginRequiredMixin, View):

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        score = data.get('score', 0)
        id_project = data.get('id_project', None)
        evaluator = Evaluator.objects.get(user=request.user)
        sc = Score.objects.filter(project_id=id_project, evaluator=evaluator).first()
        if sc:
            sc.score = score
            sc.save()
        else:
            sc = Score.objects.create(
                score=float(score),
                evaluator=evaluator,
                project_id=id_project,
                extra=Score.GENERAL
            )

        return JsonResponse(
            status=200,
            data={
                'item': {'id': sc.id, 'score': sc.score},
                'message': 'Calificación guardada exitosamente',
                'alert': 'success'
            }
        )
