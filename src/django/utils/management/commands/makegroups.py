"""
Django command to create domain groups and permissions
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    """Django command to create domain groups and permissions."""

    def handle(self, *args, **options):
        professors, created = Group.objects.get_or_create(name="professors")
        students, created = Group.objects.get_or_create(name="students")
        administrators, created = Group.objects.get_or_create(name="administrators")
        principals, created = Group.objects.get_or_create(name="principals")

        # ct = ContentType.objects.get_for_model(Profesor)

        # permission = Permission.objects.create(codename='can_add_project',

        #                           name='Can add project',
        #                           content_type=ct)
        # professors.permissions.add(permission)
