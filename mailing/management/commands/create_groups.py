from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Создает группы для отправки наставнику на проверку.'

    def add_arguments(self, parser):
        parser.add_argument('group_names', nargs='+', type=str, help='Список названий групп, которые нужно создать')

    def handle(self, *args, **kwargs):
        group_names = kwargs['group_names']

        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа {name} была успешно создана.'))
            else:
                self.stdout.write(self.style.WARNING(f'Группа {name} уже существует.'))
