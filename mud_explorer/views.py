from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import requests
import json
import time

from user_profiles.models import Profile
from .models import Room

BASE_URL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'


@api_view(['GET'])
def get_all_rooms(request):
    start_time = time.time()
    rooms = Room.objects.all().order_by('id')[:100]
    out_dict = dict()

    for room in rooms:
        out_dict[room.id] = [(room.x, room.y), {}]
        out_dict[room.id][1]['n'] = room.n
        out_dict[room.id][1]['s'] = room.s
        out_dict[room.id][1]['e'] = room.e
        out_dict[room.id][1]['w'] = room.w
    print("--- %s seconds ---" % (time.time() - start_time))
    return Response(out_dict)


@api_view(['GET'])
def init_pass(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    response = requests.get(f'{BASE_URL}/init', headers=headers)

    return Response(response.json())


# DONE
@api_view(['POST'])
def init_move(request):
    user = Profile.objects.filter(user__username=request.user)[0]
    headers = {
        'Authorization': f'Token {user.game_token}'
    }

    data = json.dumps(request.data)

    response = requests.post(f'{BASE_URL}/move/', headers=headers, data=data)
    print(data)
    return Response(response.json())

# NOT TESTED
@api_view(['POST'])
def init_take(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }

    data = json.dumps(request.data)
    response = requests.post(f'{BASE_URL}/take/', headers=headers, data=data)

    return Response(response.json())

# NOT TESTED
@api_view(['POST'])
def init_drop(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)

    response = requests.post(f'{BASE_URL}/drop/', headers=headers, data=data)

    return Response(response.json())

# NOT TESTED
@api_view(['POST'])
def init_sell(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)

    response = requests.post(f'{BASE_URL}/sell/', headers=headers, data=data)

    return Response(response.json())

# NOT TESTED
@api_view(['POST'])
def init_confirm_sell(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps({
        'name': request.data.name,
        'confirm': 'yes'
    })
    response = requests.post(f'{BASE_URL}/sell/', headers=headers, data=data)

    return Response(response.json())


@api_view(['POST'])
def init_status(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }

    response = requests.post(f'{BASE_URL}/status/', headers=headers)

    return Response(response.json())


@api_view(['POST'])
def init_examine(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)
    response = requests.post(f'{BASE_URL}/examine/',
                             headers=headers, data=data)

    return Response(response.json())


@api_view(['POST'])
def init_change_name(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)
    response = requests.post(
        f'{BASE_URL}/change_name/', headers=headers, data=data)

    return Response(response.json())


@api_view(['POST'])
def init_pray(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    response = requests.post(f'{BASE_URL}/pray/', headers=headers)

    return Response(response.json())


@api_view(['POST'])
def init_flight(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)

    response = requests.post(f'{BASE_URL}/fly/', headers=headers, data=data)

    return Response(response.json())


@api_view(['POST'])
def init_dash(request):
    user = Profile.objects.filter(user__username=request.user).first()
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    data = json.dumps(request.data)
    response = requests.post(f'{BASE_URL}/dash/', headers=headers, data=data)

    return Response(response.json())
