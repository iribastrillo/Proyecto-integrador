from django.contrib import admin

from .models import PrincipalProfile


class PrincipalAdmin (admin.ModelAdmin):
    pass

admin.site.register (PrincipalProfile, PrincipalAdmin)