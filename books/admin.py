from django.contrib import admin

from .models import Book, Comment


@admin.register(Comment)
class CommnetAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'text', 'datetime_created', 'is_active', 'recommend', )


class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'author', )


admin.site.register(Book, BookAdmin)
