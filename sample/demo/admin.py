from demo.models import DemoModel
from django.contrib import admin

# Register your models here.
from renderer.widgets import MasterImageAdminMixin

@admin.register(DemoModel)
class DemoModelAdmin(MasterImageAdminMixin, admin.ModelAdmin):
    fields = ('master', )