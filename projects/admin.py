from django.contrib import admin
from . import models

class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('owner', 'vote_total') # fields used for filtering
    readonly_fields = ('vote_total',)
    list_display = ('title', 'owner', 'vote_total') # fields which will be shown in the list view of Project


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Review)