from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user', 'is_delete')  # Fields to display in the list view
    search_fields = ('title', 'description')  # Fields to search
    list_filter = ('user', 'is_delete')  # Filter options in the sidebar

    def get_queryset(self, request):
        return Task.admin_objects.all()

admin.site.register(Task, TaskAdmin)
