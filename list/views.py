# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from models import Thing
from django.views.decorators.csrf import csrf_exempt
from serializers import ThingSerializer
from rest_framework.parsers import JSONParser
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
#主页查询出所有的task
def index(request):
    data = Thing.objects.all()
    return render(request, 'list/index.html', {'data': data})

# Create your views here.
class MsgList(APIView):
    #获取所有的todo，或者创建一个新的todo
    def get(self, request, format=None):
        question = Thing.objects.all()
        serializer = ThingSerializer(question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

    @csrf_exempt
    def post(self, request, format=None):
        msg = JSONParser().parse(request)
        serializer = ThingSerializer(data=msg)
        print serializer.is_valid()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return HttpResponse(status=400)

class MsgDetail(APIView):
    #对todo的修改和删除
    def delete(self, request, pk, format=None):
        Thing.objects.filter(id=pk).delete()
        return JsonResponse({'complete': True}, safe=False)

    @csrf_exempt
    def put(self, request, pk, format=None):
        msg = JSONParser().parse(request)
        item = Thing.objects.filter(id=pk)
        item.update(
            task=msg.get('task', item[0].task),
            complete=msg.get('complete', item[0].complete),
            # task=msg['task'],
            # complete=msg['complete'],
        )
        return JsonResponse(msg, safe=False)
# 排序
def get_msg_order(request):
    if request.method == 'GET':
        #按照优先级排序，从大到小
        question = Thing.objects.all().order_by('-priority')
        serializer = ThingSerializer(question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)
    return HttpResponse(status=404)
#分页
class PageView(APIView):
    def get(self,request,*args,**kwargs):
        # 获取所有数据
        question = Thing.objects.all()
        # 创建分页对象
        pg = PageNumberPagination()
        page_question = pg.paginate_queryset(queryset=question, request=request)
        # 序列化
        serializer = ThingSerializer(instance=page_question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)

