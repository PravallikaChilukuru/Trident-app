import datetime
import psutil
from django.core.management.base import BaseCommand
from trident_app.models import SystemSnapshot

class Command(BaseCommand):
    help = 'Saves system health snapshot to DB'

    def handle(self, *args, **kwargs):
        today = datetime.date.today()
        # Check if a snapshot exists for today
        if not SystemSnapshot.objects.filter(timestamp__date=today).exists():
            SystemSnapshot.objects.create(
                uptime="Calculated via Management Command",
                cpu_usage=psutil.cpu_percent(),
                memory_usage=psutil.virtual_memory().percent
            )
            self.stdout.write(self.style.SUCCESS('Successfully saved snapshot'))
        else:
            self.stdout.write(self.style.WARNING('Snapshot already exists for today.'))
