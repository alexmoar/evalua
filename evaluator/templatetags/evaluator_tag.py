from django import template
from evaluator.evaluator_controller import EvaluatorController

register = template.Library()


@register.filter(is_safe=True)
def get_score(project_id: int):
    """Format the numbers decimal separator"""
    score = EvaluatorController.get_score_project(project_id)
    return score.get('score_g')


