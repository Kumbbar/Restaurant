from rest_framework.exceptions import ValidationError
from apps.food.models import ClientBlackList


def check_user_is_blocked(request):
        is_blocked = ClientBlackList.objects.filter(client_id=request.data.get('client'))
        if is_blocked:
            raise ValidationError(
                {
                    'black list': 'current user is blocked',
                }
            )
