"""
Django command to create domain groups and permissions
"""
import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from profiles.models import Profesor


class Command(BaseCommand):
    """Django command to create domain groups and permissions."""

    def handle(self, *args, **options): 
        professors, created = Group.objects.get_or_create(name='professors')
        students, created = Group.objects.get_or_create(name='students')
        administrators, created = Group.objects.get_or_create(name='administrators')
        
        #ct = ContentType.objects.get_for_model(Profesor)
        
        #permission = Permission.objects.create(codename='can_add_project',
        
        #                           name='Can add project',
        #                           content_type=ct)
        #professors.permissions.add(permission)
