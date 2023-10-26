from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from projects.permissions import IsProjectAdmin, IsHowNetRoleDesigner
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from projects.models import Project
from django.conf import settings
import requests

class SearchHownetKeyWord(views.APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsHowNetRoleDesigner)]

    def get(self, request, *args, **kwargs):
        word = request.query_params.get('word')
        if not word:
            return Response(
                {'error': 'word parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST,
            )        
      
        #project = get_object_or_404(Project, pk=self.kwargs["project_id"])
        hownet_search_api = settings.HOWNET_WORD_SEARCH_URL
        hownet_word_response = requests.get(hownet_search_api, 
                                            params={'word': word})
        
        if hownet_word_response.status_code != 200:
            return Response(
                {'error': 'hownet service error'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        hownet_word_data = hownet_word_response.json()
        result = {
            "data": hownet_word_data
        }
        
        return Response(result)

