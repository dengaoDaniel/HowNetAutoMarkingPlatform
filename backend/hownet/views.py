from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from projects.permissions import IsProjectAdmin, IsHowNetRoleDesigner
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from projects.models import Project
from projects.serializers import ProjectSerializer
from django.conf import settings
import requests
import json

class SearchHownetKeyWord(views.APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsHowNetRoleDesigner)]

    def get(self, request, *args, **kwargs):
        word = request.query_params.get('word')
        if not word:
            return Response(
                {'result': 'error',
                 'errorMessage': 'word parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST,
            )        
        """
        #hownet查词api在配置文件中统一修改
        hownet_search_api = settings.HOWNET_WORD_SEARCH_URL
        hownet_word_response = requests.get(hownet_search_api, 
                                            params={'word': word})
        
        if hownet_word_response.status_code != 200:
            return Response(
                {'result': 'error',
                 'errorMessage': hownet_word_response.json()['errorMessage']}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        """
        #由于hownet侧没有解决问题，联调需要返回写死结果
        #hownet_word_data = hownet_word_response.json()
        hownet_word_data = {
                "data": [
                    {
                        "NO": "000000026417", 
                        "W_C": "不惜",        
                        "G_C": "verb",          
                        "S_C": "PlusFeeling|正面情感",  
                        "E_C": "~牺牲业余时间，~付出全部精力，~出卖自己的灵魂",  
                        "W_E": "do not hesitate to",   
                        "G_E": "verb",      
                        "S_E": "PlusFeeling|正面情感",  
                        "E_E": "",                     
                        "DEF": "{willing|愿意}",      
                        "RMK": ""
                    },
                    {
                        "NO": "000000026418", 
                        "W_C": "苹果",        
                        "G_C": "noun",          
                        "S_C": "PlusFeeling|正面情感",  
                        "E_C": "~水果，~公司名称",  
                        "W_E": "apple",   
                        "G_E": "noun",      
                        "S_E": "PlusFeeling|正面情感",  
                        "E_E": "",                     
                        "DEF": "{apple|苹果}",      
                        "RMK": ""
                    },
                ]

            }
        """
        hownet_word_data = {
            "result": "error",
            "errorMessage": "hownet查词错误",       
            "message": "该关键词不存在"     
        }
        """
        return Response(hownet_word_data)
    
    
class HownetFileUpload(views.APIView):
    permission_classes = [IsAuthenticated & (IsProjectAdmin | IsHowNetRoleDesigner)]

    #返回上传hownet文件的服务url
    def get(self, request, *args, **kwargs):
        hownet_file_upload_api = settings.HOWNET_FILE_UPLOAD_URL
        result = {
            "url": hownet_file_upload_api
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
                {   "result":"error",
                    "errorMessage": "project_id and project_state parameters are required."}, 
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
            """
            #调用hownet发布/撤回接口，通知hownet规则和词典生效
            hownet_commit_rollback_api = settings.HOWNET_COMMIT_ROLLBACK_URL
            headers = {'content-type':'application/json'}
            data = {
                'project_id': project_id,
                'project_name': project.name,
                'project_state': new_state
            }
            hownet_response = requests.post(url=hownet_commit_rollback_api, data=json.dumps(data), headers=headers)
        
            if hownet_response.status_code != 200:
                return Response(
                    {   'result': 'error',
                        'errorMessage': hownet_response.json()['errorMessage']}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            """
            serializer.save()
            return Response(
                {"result": "successful",
                 "message": "Hownet service updated successfully"}, 
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

