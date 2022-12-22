import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from projects.models import FilesApp, Project


class ProjectView(LoginRequiredMixin, View):
    template_name = "administrator/add_project.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        pass


class GetFileView(View):
    def get(self, request, *args, **kwargs):
        files = FilesApp.objects.filter(
            project_id=kwargs.get('id')
        )
        data = [{'id': f.id, 'name': f.name, 'type_file': f.type_file, 'file': f"/media/{f.file}"} for f in files]
        return JsonResponse(status=200, data={'files': data})

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        query = FilesApp.objects.get(
            id=data.get('id'),
            project__author_id=request.user.id
        )
        query.delete()
        return JsonResponse(status=200, data={'id': query.id, 'message': 'Archivo eliminado'})


@method_decorator(csrf_exempt, name='dispatch')
class UploadFileView(View):

    @staticmethod
    def extension_file(filename):
        ext = filename.split('.')[-1]
        allowed_extensions = [FilesApp.PDF, FilesApp.PNG, FilesApp.JPG, FilesApp.JPEG]
        if not ext in allowed_extensions:
            raise "Extension no válida"

        return ext

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        try:
            id_project = request.POST.get("id_project", None)
            if not id_project:
                raise "Id proyecto no identificado"

            project = Project.objects.get(id=id_project)
            name = request.FILES['file'].name
            FilesApp.objects.create(
                name=name,
                file=request.FILES['file'],
                type_file=self.extension_file(name),
                project=project
            )
            return HttpResponse(status=200)
        except Exception as e:
            return JsonResponse(status=400, data={'message': f"{e}"})
