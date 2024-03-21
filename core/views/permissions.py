from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser


class PublicApiView:
    authentication_classes = ()
    permission_classes = (AllowAny, )


class AdminApiView:
    permission_classes = (IsAuthenticated, IsAdminUser)


class LoginRequiredApiView:
    permission_classes = (IsAuthenticated,)
