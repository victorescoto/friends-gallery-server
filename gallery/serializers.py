from rest_framework import serializers

from gallery.models import Comment, Photo


class PhotosSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        photos = [Photo(**photo) for photo in validated_data]
        return Photo.objects.bulk_create(photos)


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "url", "likes"]
        read_only_fields = ["id", "likes"]
        list_serializer_class = PhotosSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "photo", "created_at"]
        read_only_fields = ["id", "created_at"]
