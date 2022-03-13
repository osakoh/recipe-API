from django.contrib import admin

from .models import Tag, Ingredient, Recipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user']
    list_display_links = ['name', 'user']
    list_per_page = 25


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    list_filter = ['name', 'user']
    list_display_links = ['name', 'user']
    list_per_page = 25


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'time_minutes', 'price', 'link']
    list_filter = ['user', 'title', 'time_minutes', 'price', 'link']
    list_display_links = ['user', 'title', 'time_minutes', 'price']
    list_per_page = 25

# Register your models here.
