from projects.models import Project


class WriterController:

    @classmethod
    def update_project(cls, id_project: int, data: dict):
        """"""
        title = data.get('title')
        description = data.get('description')
        status = data.get('status')
        project = Project.objects.get(id=id_project)
        is_updated = False
        if project.title != title:
            project.title = title
            is_updated = True
        if project.status != status:
            project.status = status
            is_updated = True
        if project.description != description:
            project.description = description
            is_updated = True

        if is_updated:
            project.save()
            message = 'Proyecto actualizado'
            alert = 'success'
        else:
            message = 'No tenemos información para actualizar'
            alert = 'warning'

        return message, alert, project.id