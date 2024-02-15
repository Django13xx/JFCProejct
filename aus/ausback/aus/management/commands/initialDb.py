import csv
from django.core.management.base import BaseCommand
from aus.models import * # import the model

class Command(BaseCommand):
    help = 'Load audio data from CSV file'

    def handle(self, *args, **options):

        # initial audio database----------------------------------------------------------------
        csv_file_path = 'static/audio.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        audio.objects.all().delete()

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                id, name, type, description, level, link = row
                # create or update the record
                audio.objects.create(
                    audio_id=id,
                    audio_name=name,
                    audio_type=type,
                    audio_description=description,
                    audio_level=level,
                    audio_link=link,
                )

        self.stdout.write(self.style.SUCCESS('Audio data loaded successfully'))
        
        
        # initial active heart audio database----------------------------------------------------------------
        csv_file_path = 'static/activeHeartAudio.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        activeHeartAudio.objects.all().delete()

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                id, name, type, description, level, link, list_id = row
                # create or update the record
                activeHeartAudio.objects.create(
                    heart_audio_id=id,
                    heart_audio_name=name,
                    heart_audio_type=type,
                    heart_audio_description=description,
                    heart_audio_level=level,
                    heart_audio_link=link,
                    heart_audio_list=list_id,
                )

        self.stdout.write(self.style.SUCCESS('Heart Audio data loaded successfully'))


        # initial active lung audio database----------------------------------------------------------------
        csv_file_path = 'static/activeLungAudio.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        activeLungAudio.objects.all().delete()

        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                id, name, type, description, level, link, list_id = row
                # create or update the record
                activeLungAudio.objects.create(
                    lung_audio_id=id,
                    lung_audio_name=name,
                    lung_audio_type=type,
                    lung_audio_description=description,
                    lung_audio_level=level,
                    lung_audio_link=link,
                    lung_audio_list=list_id,
                )

        self.stdout.write(self.style.SUCCESS('Lung Audio data loaded successfully'))


        # # initial user database----------------------------------------------------------------
        # csv_file_path_user = 'static/CustomUser.csv'  # csv file path relative to manage.py

        # # delete all the records existed in the model
        # CustomUser.objects.all().delete()

        # with open(csv_file_path_user, 'r') as file:
        #     reader = csv.reader(file)
        #     next(reader)  # skip header row
        #     for row in reader:
        #         id, name, password, state = row
        #         # create or update the record
        #         CustomUser.objects.create(
        #             user_id = id,
        #             user_name = name,
        #             user_password = password,
        #             user_log_state = state,
        #         )

        # self.stdout.write(self.style.SUCCESS('CustomUser data loaded successfully'))


        # initial question database----------------------------------------------------------------
        csv_file_path_question = 'static/question.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        question.objects.all().delete()

        with open(csv_file_path_question, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                id = row
                # create or update the record
                question.objects.create(
                    question_id = id,
                )

        self.stdout.write(self.style.SUCCESS('Question data loaded successfully'))

        # initial audioList database----------------------------------------------------------------
        csv_file_path_audiolist = 'static/audiolist.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        audioList.objects.all().delete()

        with open(csv_file_path_audiolist, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                id, name = row
                # create or update the record
                audioList.objects.create(
                    list_id = id,
                    list_name = name,
                )

        self.stdout.write(self.style.SUCCESS('audio list data loaded successfully'))

        # initial audioList database----------------------------------------------------------------
        csv_file_path_listcontent = 'static/listContent.csv'  # csv file path relative to manage.py

        # delete all the records existed in the model
        listContent.objects.all().delete()

        with open(csv_file_path_listcontent, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header row
            for row in reader:
                content_id, list_id, list_name, audio_id, audio_name = row
                # create or update the record
                listContent.objects.create(
                    content_id = content_id,
                    list_id = list_id,
                    list_name = list_name,
                    audio_id = audio_id,
                    audio_name = audio_name,
                )

        self.stdout.write(self.style.SUCCESS('audio content data loaded successfully'))