from django import template
from django.db.models import Q

from projects.models import Project

register = template.Library()


@register.filter(is_safe=True)
def format_color(status):
    """Format the numbers decimal separator"""
    return {
        Project.CREATED: "#5797fc",
        Project.DRAFT: "#5797fc",
        Project.SEND: "#5797fc",
        Project.FOR_CORRECTION: "#DC3225FF",
        Project.IN_CORRECTION: "#FFCC29FF",
        Project.QUALIFIED: "#4ecc48",
    }.get(status)


@register.filter(is_safe=True)
def count(q):
    return len(q)


@register.simple_tag
def get_projects(request, status):
    if status == 'draft':
        return Project.objects.filter(
            Q(status=Project.CREATED) | Q(status=Project.DRAFT),
            author=request.user
        ).only('id', 'title')

    if status == 'send':
        return Project.objects.filter(
            status=Project.SEND,
            author=request.user
        ).only('id', 'title')

    if status == 'for_correction':
        return Project.objects.filter(
            Q(status=Project.FOR_CORRECTION) | Q(status=Project.IN_CORRECTION),
            author=request.user
        ).only('id', 'title')

    if status == 'qualified':
        return Project.objects.filter(
            status=Project.QUALIFIED,
            author=request.user
        ).only('id', 'title')
