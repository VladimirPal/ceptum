from django.contrib import admin
from blog.models import Entry, Category

class EntrysAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ('title', 'date',)

class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    
admin.site.register(Entry, EntrysAdmin)
admin.site.register(Category, CategoriesAdmin)

