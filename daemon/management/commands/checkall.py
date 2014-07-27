from django.core.management import BaseCommand

from daemon.main import BeatmapDaemon


class Command(BaseCommand):
    help = "Check and create missing Download record in handlers"

    def handle(self, *args, **options):
        daemon = BeatmapDaemon()
        daemon.check_all()