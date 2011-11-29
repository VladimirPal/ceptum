from django.contrib import admin
from blog.models import Entry, Category

class EntrysAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ('title', 'date',)
    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Entry, EntrysAdmin)
admin.site.register(Category, CategoriesAdmin)

