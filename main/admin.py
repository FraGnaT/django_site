# -*- coding:UTF-8 -*-

from django.contrib import admin
from tst.main.models import content, site_setting, tags, Category, Comment


class NewsAdmin(admin.ModelAdmin):
    fieldsets = (
    ('Контент',{'fields': ('title', 'preview', 'text')}),
    ('Теги',{'fields': ('tags', 'description', 'category', 'published')}),)
    list_display = ('id', 'title', 'description', 'date', 'category', 'published')
    list_filter = ('id', 'date', 'category', 'tags')
    class Media:
        js = ('/media/admin/js/tiny_mce/tiny_mce.js',
              '/media/admin/js/tiny_mce/textareas.js',)
        
admin.site.register(content, NewsAdmin)

class setting(admin.ModelAdmin):
    fieldsets = (
    ('Настройки', {'fields': ('title', 'description', 'url')}),)
    list_display = ('title', 'description', 'url')
admin.site.register(site_setting, setting)

class category(admin.ModelAdmin):
    fieldsets = (
    ( 'none', {'fields': ('name', 'url', 'OnTop')}),)
    list_display = ('name', 'url', 'OnTop')
admin.site.register(Category, category)

class comment(admin.ModelAdmin):
    fieldsets = (
    ('none', {'fields': ('user', 'text')}),)
    list_display = ('user', 'text', 'date')
admin.site.register(Comment, comment)

class Tags(admin.ModelAdmin):
    fields = ('tag',)
admin.site.register(tags, Tags)
