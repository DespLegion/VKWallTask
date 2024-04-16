from django.core.management.base import BaseCommand

from apps.vk_bot.bot_core import start_listen


class Command(BaseCommand):
    help = "Run VK bot"

    def handle(self, *args, **options):
        start_listen()
