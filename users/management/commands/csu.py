from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """ Кастомная команда для создания админа """
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.create(
            email='admin2@gmail.com',
            username='Admin2',
        )
        user.set_password('1650')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Успешно созданный пользователь-администратор с электронной почтой '
                                             f'{user.email}'))
