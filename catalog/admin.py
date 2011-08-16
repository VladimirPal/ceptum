from django.contrib import admin

from catalog.models import Product, ProductPhoto, Category, Section, Feature, FeatureName, File
from cart.models import Client

class PhotoInline(admin.StackedInline):
    model = ProductPhoto

class FeaturesInline(admin.StackedInline):
    model = Feature

class FilesInline(admin.StackedInline):
    model = File

admin.site.register(ProductPhoto)

class ProductsAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, FeaturesInline, FilesInline]
    list_display = ('name', 'price', 'quantity', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Product, ProductsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoriesAdmin)

class SectionsAdmin(admin.ModelAdmin):
        prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Section, SectionsAdmin)

admin.site.register(FeatureName)

class ClientsAdmin(admin.ModelAdmin):
    ordering = ['ordered_at']
    list_display = ('ordered_at', 'name')

admin.site.register(Client, ClientsAdmin)
