# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from models import Thing
from django.views.decorators.csrf import csrf_exempt
from serializers import ThingSerializer
from rest_framework.parsers import JSONParser

#主页查询出所有的task
def index(request):
    data = Thing.objects.all()
    return render(request, 'list/index.html', {'data': data})

# Create your views here.


def get_msg(request):
    if request.method == 'GET':
        question = Thing.objects.all()
        serializer = ThingSerializer(question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)
    return HttpResponse(status=404)


@csrf_exempt
def add_msg(request):
    if request.method == 'POST':
        msg = JSONParser().parse(request)
        serializer = ThingSerializer(data=msg)
        print serializer.is_valid()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=201)
    return HttpResponse(status=400)


def del_msg(request, pk):
    if request.method == 'GET':
        Thing.objects.filter(id=pk).delete()
        return JsonResponse({'complete': True}, safe=False)
    return HttpResponse(status=404)


@csrf_exempt
def edit_msg(request, pk):
    if request.method == 'POST':
        msg = JSONParser().parse(request)
        item = Thing.objects.filter(id=pk)
        item.update(
            task=msg.get('task', item[0].task),
            complete=msg.get('complete', item[0].complete),
            # task=msg['task'],
            # complete=msg['complete'],
        )
        return JsonResponse(msg, safe=False)
    return HttpResponse(status=404)
# 排序
def get_msg_order(request):
    if request.method == 'GET':
        #按照优先级排序，从大到小
        question = Thing.objects.all().order_by('-priority')
        serializer = ThingSerializer(question, many=True)
        return JsonResponse(serializer.data, safe=False, status=201)
    return HttpResponse(status=404)

