from django.urls import include, path
from .views import SearchHownetKeyWord, HownetFileUpload, HownetCommitAndRollBack

urlpatterns = [

    path(route="hownet/keyword", view=SearchHownetKeyWord.as_view(), name="search_hownet_key_word"),
    path(route="hownet/upload", view=HownetFileUpload.as_view(), name="upload_hownet_file"),
    path(route="hownet/commit-rollback", view=HownetCommitAndRollBack.as_view(), name="hownet_commit_rollback"),

]
