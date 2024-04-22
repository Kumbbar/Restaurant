from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


BASE_CODENAMES = ('admin_permission', 'food_permission', 'client_service_permission', 'cooking_permission')


class Command(BaseCommand):

    @staticmethod
    def is_permission_exists(codename):
        return True if Permission.objects.filter(codename=codename).first() else False

    def create_statuses_by_consts_model(self):
        default_content_type = ContentType.objects.get(model='restaurant')
        for codename in BASE_CODENAMES:
            if self.is_permission_exists(codename):
                self.stdout.write(f'Status {codename} already exists')
                continue
            new_status = Permission(name=codename, content_type=default_content_type, codename=codename)
            new_status.save()
            self.stdout.write(f'Status {codename} created')

    def handle(self, *args, **options):
        self.create_statuses_by_consts_model()
        self.stdout.write(self.style.SUCCESS('Successfully ended'))
