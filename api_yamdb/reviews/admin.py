from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'title', 'score', 'pub_date')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'review', 'pub_date')
    search_fields = ('review', 'author')
    list_filter = ('author',)


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
