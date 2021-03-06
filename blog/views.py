from django.contrib.auth.models import User, Group
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from blog.serializers import (
    UserSerializer,
    GroupSerializer,
    ImageSerializer,
    PostSerializer,
)
from blog.models import Image, Post
from blog.permissions import IsOwnerOrReadOnly


def index(request):
    return HttpResponse("This is my blog.")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None):
        if request.user and pk == "me":
            return Response(
                self.serializer_class(request.user, context={"request": request}).data
            )
        else:
            return super(UserViewSet, self).retrieve(request, pk)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows images to be viewed or edited.
    """

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Image.objects.all()
        username = self.request.query_params.get("username", None)
        if username is None:
            return None
        else:
            queryset = queryset.filter(owner__username=username)
        search = self.request.query_params.get("search", None)
        if search is not None:
            queryset = queryset.filter(
                things__name__icontains=search
            ) | queryset.filter(location__icontains=search)
        return queryset.distinct()

    def create(self, request):
        image = ImageSerializer(data=request.data)
        if image.is_valid():
            if "post" in request.data:
                print(request.data["post"])
                image.save(
                    owner=request.user, post=Post.objects.get(pk=request.data["post"])
                )
            else:
                image.save(owner=request.user)
            return Response(image.data, status=status.HTTP_201_CREATED)
        return Response(image.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        username = self.request.query_params.get("username", None)
        if username is None:
            return None
        else:
            queryset = queryset.filter(owner__username=username)

        return queryset


def media_types(request):
    return JsonResponse(
        {
            "data": {
                "images": [
                    "image/png",
                    "image/jpg",
                    "image/jpeg",
                ]
            }
        }
    )
