from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from gallery.models import Photo
from gallery.serializers import CommentSerializer, PhotoSerializer


class PhotoViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    """
    API endpoint that allows photos to be listed, created or liked.
    """

    queryset = Photo.approved_photos()
    serializer_class = PhotoSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        photos = request.data.get("photos")
        serializer = self.get_serializer(data=photos, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(methods=["post"], detail=True)
    def like(self, request, pk=None):
        try:
            photo = self.queryset.get(id=pk)
        except Photo.DoesNotExist:
            return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)

        photo.like()
        photo.save()
        return Response(None, status=status.HTTP_202_ACCEPTED)

    @action(methods=["get", "post"], detail=True)
    def comments(self, request, pk=None):
        try:
            photo = self.queryset.get(id=pk)
        except Photo.DoesNotExist:
            return Response("Photo not found", status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":
            return self._list_comments(photo)

        elif request.method == "POST":
            return self._post_comment(request, pk)

    def _list_comments(self, photo):
        serializer = CommentSerializer(photo.comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _post_comment(self, request, photo_id):
        data = {**request.data, "photo": photo_id}
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
