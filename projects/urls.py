from django.urls import path, include

from projects import views

app_name = 'projects'
urlpatterns = [
    path('file/<int:id>', views.GetFileView.as_view(), name='get_file'),
    path('upload-file/', views.UploadFileView.as_view(), name='upload_files'),
]
