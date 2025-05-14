from django.contrib import admin
from .models import Operation, Category


@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
