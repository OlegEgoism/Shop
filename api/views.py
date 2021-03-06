import json

from celery import shared_task
from django.conf import settings
import redis
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

# Connect to our Redis instance
redis_instance = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)



@api_view(['GET', 'POST'])
def manage_items(request, *args, **kwargs):
    """
    будет использоваться для получения всех элементов,
    которые в настоящее время установлены в нашем запущенном экземпляре Redis.
    Это представление также позволит нам создавать новые записи в нашем экземпляре Redis,
    передавая объект JSON
    """
    if request.method == 'GET':
        items = {}
        count = 0
        for key in redis_instance.keys("*"):
            items[key.decode("utf-8")] = redis_instance.mget(key)
            count += 1
        response = {
            'count': count,
            'msg': f"Found {count} items.",
            'items': items
        }
        return Response(response, status=200)
    elif request.method == 'POST':
        item = request._data
        # item = json.loads(request.body)
        key = list(item.keys())[0]
        value = item[key]
        redis_instance.set(key, value)
        response = {
            'msg': f"{key} successfully set to {value}"
        }
        return Response(response, 201)


@api_view(['GET', 'PUT', 'DELETE'])
def manage_item(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_instance.get(kwargs['key'])
            if value:
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': 'success'
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_instance.get(kwargs['key'])
            if value:
                redis_instance.set(kwargs['key'], new_value)
                response = {
                    'key': kwargs['key'],
                    'value': value,
                    'msg': f"Successfully updated {kwargs['key']}"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)

    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_instance.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg': f"{kwargs['key']} successfully deleted"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key': kwargs['key'],
                    'value': None,
                    'msg': 'Not found'
                }
                return Response(response, status=404)


# @api_view(['GET', 'POST'])
# def get_state(request, id):
#     status = redis_instance.get('celery-task-meta-'+id)
#     state = json.loads(status)
#     key = redis_instance.keys('*')
#     print(key)
#     print(status, 'state')
#     print(len(id), 'get_state')
#     return Response(state['status'])

@api_view(['GET', 'POST'])
def get_state(request, id):
    status = redis_instance.get('celery-task-meta-' +id)
    status = json.loads(status)
    print(status)
    # if request.method == 'GET':
    #     meta = 'celery-task-meta-'+id
    #     # print(redis_instance.keys('*'), 'r  edis_instance task_id')
    #     state = redis_instance.get(meta)
    #     print(state)
    #     keys = redis_instance.keys('*')
    #     keys = [value.decode('utf-8') for value in keys]
    #     # print(keys)
    #     # print(id, 'eto id taski')
    #     # print(meta in keys)
    #     # response = {
    #         # 'status': instance['status']
    #     # }
    return Response(status['status'])




    # form = HomeForm()
    # if request.method == 'POST':
    #     form = HomeForm(request.POST)
    #     if form.is_valid():
    #         num = form.cleaned_data
    #         # print(num.get('number'))
    #         result = add.delay(num.get('number'))
    #         # print(num.get('number'))
    #
    # context = {'form': form}
    # return render(request, 'orders/order/home.html', context=context)