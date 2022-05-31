from django.core.management.base import BaseCommand, CommandError
from ...models import Vacancy

class Command(BaseCommand):
    status = "ARCHIVED"

    help = f"Changes vacancy's status to '{status}'"

    def add_arguments(self, parser):
        parser.add_argument('vacancy_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for vacancy_id in options['vacancy_id']:
            try:
                vacancy = Vacancy.objects.get(pk=vacancy_id)
            except Vacancy.DoesNotExist:
                raise CommandError('Vacancy "%s" does not exist' % vacancy_id)

            vacancy.status = self.status
            vacancy.save()

            self.stdout.write(self.style.SUCCESS(f"Successfully changed status to '{self.status}' vacancy #{vacancy_id}"))
