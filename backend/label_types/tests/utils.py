from model_mommy import mommy

from projects.models import ProjectType


def make_label(project, **kwargs):
    if project.project_type.endswith("Classification"):
        return mommy.make("CategoryType", project=project, **kwargs)
    else:
        return mommy.make("SpanType", project=project, **kwargs)
