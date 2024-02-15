from django.core.management.base import BaseCommand
from aus.models import * # import the model

class Command(BaseCommand):
    help = 'Delete all the data from CSV file'
    def handle(self, *args, **options):

        # delete all the records existed in the audio
        audio.objects.all().delete()
        activeHeartAudio.objects.all().delete()
        activeLungAudio.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Audio data deleted successfully'))


        # delete all the records existed in the user
        CustomUser.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('CustomUser data deleted successfully'))


        # delete all the records existed in the question
        question.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Question data deleted successfully'))

        # delete all the records existed in the list
        audioList.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('List data deleted successfully'))

        # delete all the records existed in the list
        audioList.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('List content data deleted successfully'))