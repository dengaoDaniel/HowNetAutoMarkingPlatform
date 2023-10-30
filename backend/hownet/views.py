from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from projects.permissions import IsProjectAdmin, IsHowNetRoleDesigner
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from projects.models import Project
from projects.serializers import ProjectSerializer
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
      
        #hownet查词api在配置文件中统一修改
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
    
    
class HownetFileUpload(views.APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsHowNetRoleDesigner)]

    #返回上传hownet文件的服务url
    def get(self, request, *args, **kwargs):
        hownet_file_ipload_api = settings.HOWNET_FILE_UPLOAD_URL
        result = {
            "url": hownet_file_ipload_api
        }

        return Response(result)
    

class HownetCommitAndRollBack(views.APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsHowNetRoleDesigner)]

    def post(self, request, *args, **kwargs):
        project_id = request.data.get("project_id")
        new_state = request.data.get("project_state")

        # 确保project_id和project_state都在请求体中
        if not all([project_id, new_state]):
            return Response(
                {"error": "project_id and project_state parameters are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 获取对应的Project对象
        project = get_object_or_404(Project, pk=project_id)        
        # 使用serializer更新项目状态
        serializer_data = {
            "project_state": new_state,
        }
        serializer = ProjectSerializer(instance=project, data=serializer_data, partial=True)

        if serializer.is_valid():
            serializer.save()

            #TODO:调用hownet发布/撤回接口，通知hownet规则和词典生效
            hownet_commit_rollback_api = settings.HOWNET_COMMIT_ROLLBACK_URL
            hownet_response = requests.get(hownet_commit_rollback_api)
        
            if hownet_response.status_code != 200:
                return Response(
                    {'error': 'hownet service error'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response({"result": "Hownet service updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

