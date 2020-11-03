from django.db import models


class Photo(models.Model):
    url = models.URLField()
    likes = models.IntegerField(default=0)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def like(self):
        self.likes += 1

    @staticmethod
    def approved_photos():
        """
        Returns a list of approved photos
        """
        return Photo.objects.filter(approved=True).order_by("-created_at")


class Comment(models.Model):
    author = models.CharField(max_length=100, null=True)
    content = models.CharField(max_length=255)
    photo = models.ForeignKey(
        "Photo", on_delete=models.CASCADE, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
