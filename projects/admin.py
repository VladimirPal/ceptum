from django.contrib import admin
from projects.models import Project, Category

class EntrysAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ('name', 'date',)
    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js', '/static/js/tinymce_setup.js',]

class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Project, EntrysAdmin)
admin.site.register(Category, CategoriesAdmin)
