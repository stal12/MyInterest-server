from json import JSONDecodeError

from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.utils import jwt_get_username_from_payload_handler
from server import models
from rest_framework_jwt.settings import api_settings
import requests
import jwt
import json
import time
from multiprocessing import Process

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


# Create your views here.

def funzione(name):
    print('hello', name)


def fetch_user_obj(email):
    if not models.MyUser.objects.filter(email=email).exists():
        return None
    else:
        user = models.MyUser.objects.get(email=email)
        person = models.Person.objects.get(user=user)
        categories = []
        for category in person.categories.all():
            categories.append(category.name)
        friends_id = []
        for friend in person.friends.all():
            friends_id.append(friend.id)
        pending_friends_id = []
        for pending_friend in person.pending_friends.all():
            pending_friends_id.append(pending_friend.id)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        json_res = {
            'token': token,
            'id': user.id,
            'email': user.email,
            'name': person.name,
            'categories': categories,
            'friends': friends_id,
            'pending_friends': pending_friends_id,
            'image': person.image
        }
        return json_res


@csrf_exempt
def prova(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return HttpResponseForbidden()
    else:
        r = requests.post('http://192.168.1.111:8000/api-token-verify/', {"token": request.META['HTTP_AUTHORIZATION']})
        if r.status_code != 200:
            return HttpResponseForbidden()
        else:
            response = HttpResponse('ciao')
            return response


@csrf_exempt
def my_obtain_jwt_token(request):
    response = obtain_jwt_token(request)
    return response


@csrf_exempt
def login(request):
    try:
        credentials = json.loads(request.body)
    except JSONDecodeError:
        return HttpResponseForbidden()
    r = requests.post('http://localhost:8000/api-token-auth/', credentials)
    if r.status_code != 200:
        return HttpResponseForbidden()
    else:
        user = models.MyUser.objects.get(email=credentials['email'])
        person = models.Person.objects.get(user=user)
        categories = []
        for category in person.categories.all():
            categories.append(category.name)
        friends_id = []
        for friend in person.friends.all():
            friends_id.append(friend.id)
        pending_friends_id = []
        for pending_friend in person.pending_friends.all():
            pending_friends_id.append(pending_friend.id)
        json_res = {
            'token': json.loads(r.content)['token'],
            'id': user.id,
            'email': user.email,
            'name': person.name,
            'categories': categories,
            'friends': friends_id,
            'pending_friends': pending_friends_id,
            'image': person.image
        }
        return HttpResponse(json.dumps(json_res))


# @csrf_exempt
# def personal(request):
#     if 'HTTP_AUTHORIZATION' not in request.META:
#         return HttpResponseForbidden()
#     else:
#         token = request.META['HTTP_AUTHORIZATION']
#         r = requests.post('http://192.168.1.111:8000/api-token-verify/', {"token": token})
#         if r.status_code != 200:
#             return HttpResponseForbidden()
#         else:
#             payload = jwt.decode(token, verify=False)
#             username = jwt_get_username_from_payload_handler(payload)
#             if not User.objects.filter(username=username).exists():
#                 return HttpResponseForbidden()
#             else:
#                 user = User.objects.get(username=username)
#                 response = HttpResponse('{\n  "username": "' + user.username + '",\n  "email": "' + user.email + '" \n}')
#                 return response


@csrf_exempt
def facebook_login(request):
    client_obj = json.loads(request.body)
    print(client_obj)
    if ('token' not in client_obj) or ('email' not in client_obj):
        return HttpResponseForbidden()
    else:
        r = requests.get('https://graph.facebook.com/me?access_token=' + client_obj['token'])
        facebook_obj = json.loads(r.content)
        print(facebook_obj)
        if ('name' not in facebook_obj) or ('id' not in facebook_obj):
            return HttpResponseForbidden()
        else:
            if not models.MyUser.objects.filter(email=client_obj['email']).exists():
                return HttpResponseForbidden()
            else:
                user_obj = fetch_user_obj(client_obj['email'])
                return HttpResponse(json.dumps(user_obj))

@csrf_exempt
def facebook_register(request):
    client_obj = json.loads(request.body)
    print(client_obj)
    if ('token' not in client_obj) or ('email' not in client_obj) or ('name' not in client_obj) or ('image' not in client_obj):
        return HttpResponseForbidden()
    else:
        r = requests.get('https://graph.facebook.com/me?access_token=' + client_obj['token'])
        facebook_obj = json.loads(r.content)
        print(facebook_obj)
        if ('name' not in facebook_obj) or ('id' not in facebook_obj):
            return HttpResponseForbidden()
        else:
            if models.MyUser.objects.filter(email=client_obj['email']).exists():
                user_obj = fetch_user_obj(client_obj['email'])
                user_obj['created'] = False
                return HttpResponse(json.dumps(user_obj))
            else:
                user = models.MyUser.objects.create_user(client_obj['email']) # forse lasciare la password vuota non è l'idea migliore
                user.save()
                person = models.Person(user=user, name=client_obj['name'], image=client_obj['image'])
                person.save()
                user_obj = fetch_user_obj(client_obj['email'])
                user_obj['created'] = True
                return HttpResponse(json.dumps(user_obj))


@csrf_exempt
def fetch_user(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return HttpResponseForbidden()
    else:
        token = request.META['HTTP_AUTHORIZATION']
        r = requests.post('http://192.168.1.111:8000/api-token-verify/', {"token": token})
        if r.status_code != 200:
            return HttpResponseForbidden()
        else:
            payload = jwt.decode(token, verify=False)
            email = jwt_get_username_from_payload_handler(payload)
            if not models.MyUser.objects.filter(email=email).exists():
                return HttpResponseForbidden()
            else:
                user = models.MyUser.objects.get(email=email)
                response = HttpResponse('{\n  "email": "' + user.email + '",\n  "email": "' + user.email + '" \n}')
                return response


@csrf_exempt
def register_user(request):
    user_data = json.loads(request.body)
    if ('firstName' not in user_data) or ('lastName' not in user_data) or ('email' not in user_data) or \
            ('password' not in user_data) or ('confirmPassword' not in user_data):
        print('manca qualcosa')
        return HttpResponseForbidden()
    else:
        if user_data['password'] != user_data['confirmPassword']:
            print('password diverse')
            return HttpResponseForbidden()
        else:
            if MyUser.objects.filter(email=user_data['email']).exists():
                print('esiste già')
                return HttpResponse('{\n  "error": "user already exists"\n}')
            else:
                user = MyUser.objects.create_user(email=user_data['email'], password=user_data['password'])
                Person(user=user, first_name=user_data['firstName'], last_name=user_data['lastName']).save()
                r = requests.post('http://192.168.1.111:8000/api-token-auth/',
                                  {"email": user_data['email'], "password": user_data['password']})
                print(r.content)
                return HttpResponse(r)


@csrf_exempt
def register_categories(request):
    body = json.loads(request.body)
    if 'categories' not in body:
        return HttpResponseForbidden
    else:
        if 'HTTP_AUTHORIZATION' not in request.META:
            return HttpResponseForbidden()
        else:
            token = request.META['HTTP_AUTHORIZATION']
            r = requests.post('http://localhost:8000/api-token-verify/', {"token": token})
            if r.status_code != 200:
                return HttpResponseForbidden()
            else:
                payload = jwt.decode(token, verify=False)
                email = jwt_get_username_from_payload_handler(payload)
                if not models.MyUser.objects.filter(email=email).exists():
                    return HttpResponseForbidden()
                else:
                    user = models.MyUser.objects.get(email=email)
                    person = models.Person.objects.get(user=user)
                    person.categories.clear()
                    for category in body['categories']:
                        person.categories.add(models.Category.objects.get(name=category))
                    response = HttpResponse('')
                    return response
