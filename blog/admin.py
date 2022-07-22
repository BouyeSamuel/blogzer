from django.contrib import admin

from .models import Article, Category

class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "body")
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = Category.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)