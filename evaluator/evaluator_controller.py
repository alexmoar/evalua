from django.db.models import Sum

from projects.models import FilesApp, Score


class EvaluatorController:
    @staticmethod
    def get_score_project(project_id: int, request=None):
        if request:
            scores = Score.objects.filter(
                project_id=project_id,
                evaluator__user_id=request.user.id
            ).only('score', 'extra')
        else:
            scores = Score.objects.filter(
                project_id=project_id
            ).only('score', 'extra')

        score_g = scores.first()
        score_g = int(score_g.score) if score_g else 0

        return {
            'score_g': score_g,
        }
