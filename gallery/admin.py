from django.contrib import admin
from django.utils.html import format_html

from gallery.models import Comment, Photo


class CommentInline(admin.TabularInline):
    model = Comment
    show_change_link = False
    extra = 0
    readonly_fields = ("content", "created_at")

    def has_add_permission(self, *args, **kwargs):
        return False


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = [
        "thumb",
        "approved",
        "likes",
        "comments",
        "created_at",
        "updated_at",
    ]
    readonly_fields = (
        "image",
        "likes",
        "created_at",
        "updated_at",
    )
    exclude = ("url",)
    list_filter = ("approved", "created_at", "updated_at")
    inlines = [
        CommentInline,
    ]
    actions = ["approve", "unapprove"]

    def approve(self, request, queryset):
        queryset.update(approved=True)

    approve.short_description = "Mark selected photos as approved"

    def unapprove(self, request, queryset):
        queryset.update(approved=False)

    unapprove.short_description = "Mark selected photos as unapproved"

    def get_formsets_with_inlines(self, request, photo=None):
        for inline in self.get_inline_instances(request, photo):
            if photo.comments.count() > 0:
                yield inline.get_formset(request, photo), inline

    def comments(self, photo):
        return photo.comments.count()

    def thumb(self, photo):
        return format_html(f"<img src='{photo.url}' height='40' />")

    thumb.allow_tags = True
    thumb.__name__ = "Thumb"

    def image(self, photo):
        return format_html(f"<img src='{photo.url}' style='max-height: 500px' />")

    image.allow_tags = True
    image.__name__ = "Image"

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
