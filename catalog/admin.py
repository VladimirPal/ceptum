from django.contrib import admin
from catalog.models import Product, ProductPhoto, Category, Section, File, CategoryProduct, CameraProduct
from cart.models import Client

class PhotoInline(admin.StackedInline):
    model = ProductPhoto

class FilesInline(admin.StackedInline):
    model = File

admin.site.register(ProductPhoto)

class CategoryProductinline(admin.TabularInline):
    model = CategoryProduct
    sortable_field_name = "position"

class CategoryProductinline2(admin.TabularInline):
    model = CategoryProduct

class ProductsAdmin(admin.ModelAdmin):
    def queryset(self, request):
        qs = Product.objects.exclude(category__slug__in=['outdoor', 'indoor'])
        return qs

    inlines = [PhotoInline, FilesInline, CategoryProductinline2]
    list_display = ('name', 'price', 'quantity', 'created_at', 'updated_at')
    list_per_page = 50
    ordering = ['name']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug' : ('name',)}

    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

class CameraProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, FilesInline, CategoryProductinline2]
    ordering = ['category']

    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]


admin.site.register(Product, ProductsAdmin)
admin.site.register(CameraProduct, CameraProductAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    inlines = [CategoryProductinline]
    list_display = ('name', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description',]
    prepopulated_fields = {'slug' : ('name',)}

    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

admin.site.register(Category, CategoriesAdmin)

class CategoryInline(admin.TabularInline):
    fields = ('name', 'position',)
    model = Category
    sortable_field_name = "position"

class SectionsAdmin(admin.ModelAdmin):
        inlines = [CategoryInline]
        prepopulated_fields = {'slug' : ('name',)}

        class Media:
            js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

admin.site.register(Section, SectionsAdmin)

class ClientsAdmin(admin.ModelAdmin):
    ordering = ['ordered_at']
    list_display = ('ordered_at', 'name')

admin.site.register(Client, ClientsAdmin)
