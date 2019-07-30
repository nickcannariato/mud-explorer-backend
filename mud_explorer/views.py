from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

from user_profiles.models import Profile

BASE_URL = 'https://lambda-treasure-hunt.herokuapp.com/api/adv/init/'


@api_view(['GET'])
def init_pass(request):
    user = Profile.objects.filter(user__username=request.user)[0]
    headers = {
        'Authorization': f'Token {user.game_token}'
    }
    response = requests.get(BASE_URL, headers=headers)

    return Response(response.json())
