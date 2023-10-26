from django.urls import include, path
from .views import SearchHownetKeyWord

urlpatterns = [

    path(route="hownet", view=SearchHownetKeyWord.as_view(), name="search_hownet_key_word"),
]
