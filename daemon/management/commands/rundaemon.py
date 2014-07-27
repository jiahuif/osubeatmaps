from django.core.management import BaseCommand

from daemon.main import BeatmapDaemon


class Command(BaseCommand):
    help = "Run the beatmap daemon."

    def handle(self, *args, **options):
        daemon = BeatmapDaemon()
        daemon.run_daemon()