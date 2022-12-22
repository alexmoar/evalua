from django.urls import path

from evaluator import views

app_name = 'evaluator'
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('qualified/<int:id_project>', views.ProjectsQualifiedView.as_view(), name='qualified'),
    path('project/scores/<int:id_project>', views.ProjectScoresQuestionView.as_view(), name='get_scores'),
    path('projects/questions/<int:id>', views.ProjectQuestionsView.as_view(), name='get_questions_project'),
]
