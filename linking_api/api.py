from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User, Link
from .serializers import (
    UserSerializer,
   LinkSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView


# USER API
class UserCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        root_param = self.request.query_params.get("root")

        # Verificar si se proporcionó el parámetro 'root' con el valor '1234'
        if root_param == "planfitRootAdmin232":
            # Si es así, mostrar la lista de usuarios
            return User.objects.all()

        # Si no se proporciona el parámetro o no tiene el valor esperado, retornar una lista vacía
        return User.objects.none()

    def perform_create(self, serializer):
        # La creación de usuarios es libre, no hay condiciones
        serializer.save()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Serializar los usuarios
        serializer = self.serializer_class(queryset, many=True)

        # Devolver la respuesta
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def perform_destroy(self, instance):
        # Eliminar también los links asociados al usuario
        Link.objects.filter(usuario=instance).delete()

        # Finalmente, eliminar el link
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Personalizo la clase TokenObtainPairView para que devuelva el id del usuario
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Si las credenciales son válidas y se generó el token de acceso,
        # agrega el ID del usuario a la respuesta
        if response.status_code == status.HTTP_200_OK:
            user = User.objects.get(username=request.data.get("username"))
            user_id = user.id
            response.data["user_id"] = user_id

        return response


# LINK API
class LinkListCreateView(generics.ListCreateAPIView):
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(usuario=user)

class LinkRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = (IsAuthenticated,)

