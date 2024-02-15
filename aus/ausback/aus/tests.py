from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json
import os
from django.conf import settings
from .models import *
# for setup
from django.core.files.uploadedfile import SimpleUploadedFile
# for test uploading files
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
# for database set up for urls testing
from django.test import TestCase, Client
from django.urls import reverse
from django.core.management import call_command
# for testing delete list content view 
from urllib.parse import quote

# *** All test methods must start with the word 'test' ***

# 1 
# Test cases for views.py:
class ViewsTestCase(TestCase):
    # (1) For setup before each test case
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Copy the actual test files to a temporary directory
        cls.audio_content = b"Some binary audio content"
        cls.audio_file_path = "media/audio/test_audio.mp3"
        with open(cls.audio_file_path, 'wb') as audio_file:
            audio_file.write(cls.audio_content)
        # Use SimpleUploadedFile to create a dummy file object for testing upload
        cls.audio_file = SimpleUploadedFile(
            "test_audio.mp3",
            cls.audio_content,
            content_type="audio/mp3"
        )
    # (3) For clean up after each test case
    @classmethod
    def tearDownClass(cls):
        # Delete temporary files at the end of the test
        try:
            os.remove(cls.audio_file_path)
        except FileNotFoundError:
            pass
        # Call super() to complete the tear down
        super().tearDownClass()

    def setUp(self):
        super().setUpClass()
        # Call 'initialDb' for initial database
        call_command('initialDb') 
        # Hint: When you need to deal with data in database, use this above line to initial database
        # # Set up test data
        # self.audio = audio.objects.create(
        #     audio_id=1,  # Assign a valid audio_id
        #     audio_name='TestAudio',
        #     audio_type='Heartbeat',
        #     audio_link='test_audio.mp3',
        # )
        # # create test data for list and listContent
        # self.list = audioList.objects.create(list_name='TestList')
        # self.list_content = listContent.objects.create(
        #     list_name=self.list,
        #     audio_name=self.audio,
        # )
        # # create a temporary audio file for testing
        # audio_content = b"Some binary audio content"
        # self.audio_file = SimpleUploadedFile(
        #     "test_audio.mp3",
        #     audio_content,
        #     content_type="audio/mp3"
        # )
        # Create a client for testing
        self.client = Client()

    # (2) Test cases for views.py:
    def test_home_view(self):
        print(" Method: test_home_view......")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Our Website')

    def test_play_random_heartbeat_view(self):
        print(" Method: test_play_random_heartbeat_view......")
        response = self.client.get(reverse('playRandomHeartBeat'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('audio_name', data)
        self.assertIn('audio_link', data)

    def test_play_random_abnormal_view(self):
        print(" Method: test_play_random_abnormal_view......")
        response = self.client.get(reverse('playRandomAbnormal'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        if 'error' in data:
            # Check if the response indicates no audio found
            self.assertEqual(data['error'], 'No audio found')
        else:
            # Check if the response contains the expected fields
            self.assertIn('audio_name', data)
            self.assertIn('audio_type', data)
            self.assertIn('audio_link', data)

    def test_play_random_view(self):
        print(" Method: test_play_random_view......")
        response = self.client.get(reverse('playRandom'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        if 'error' in data:
            # Check if the response indicates no audio found
            self.assertEqual(data['error'], 'No audio found')
        else:
            # Check if the response contains the expected fields
            self.assertIn('audio_name', data)
            self.assertIn('audio_type', data)
            self.assertIn('audio_link', data)

    def test_get_all_audio_view(self):
        print(" Method: test_get_all_audio_view......")
        response = self.client.get(reverse('getAllAudio'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Check if the response is a list of dictionaries
        self.assertIsInstance(data, list)
        for audio_data in data:
            # Check if each dictionary has the expected keys
            self.assertIn('audio_name', audio_data)
            self.assertIn('audio_id', audio_data)
            self.assertIn('audio_type', audio_data)
            self.assertIn('audio_description', audio_data)
            self.assertIn('audio_level', audio_data)
            self.assertIn('audio_link', audio_data)

    def test_get_all_list_view(self):
        print(" Method: test_get_all_list_view......")
        response = self.client.get(reverse('getAllList'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Check if the response is a list of dictionaries
        self.assertIsInstance(data, list)
        for list_data in data:
            # Check if each dictionary has the expected keys
            self.assertIn('list_name', list_data)
            self.assertIn('list_id', list_data)

    def test_get_all_content_view(self):
        print(" Method: test_get_all_content_view......")
        response = self.client.get(reverse('getAllContent'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        # Check if the response is a list of dictionaries
        self.assertIsInstance(data, list)
        for content_data in data:
            # Check if each dictionary has the expected keys
            self.assertIn('list_id', content_data)
            self.assertIn('audio_id', content_data)

    def test_delete_list_content_view(self):
        print(" Method: test_delete_list_content_view......")
        # Assuming you have existing list content to delete
        list_name = 'TestList'
        audio_name = 'TestAudio'
        
        # Encode URL parameters
        encoded_list_name = quote(list_name)
        encoded_audio_name = quote(audio_name)

        # Make a DELETE request to the view
        response = self.client.delete(reverse('deleteListContent', args=[encoded_list_name, encoded_audio_name]))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Delete successfully')

    def test_delete_related_list_content_view(self):
        print(" Method: test_delete_related_list_content_view......")
        # Assuming you have an existing audio with associated list content to delete
        audio_id = 1  # replace with the actual audio_id

        # Encode URL parameter
        encoded_audio_id = quote(str(audio_id))

        # Make a DELETE request to the view
        response = self.client.delete(reverse('deleteRelatedListContent', args=[encoded_audio_id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Delete successfully')

    def test_update_active_heart_audio_view(self):
        print(" Method: test_update_active_heart_audio_view......")
        # Assuming you have an existing audio and list for the update
        audio_id = 17  # replace with the actual audio_id
        list_id = 1  # replace with the actual list_id
        
        # Encode URL parameters
        encoded_audio_id = quote(str(audio_id).encode('utf-8'))
        encoded_list_id = quote(str(list_id).encode('utf-8'))

        # Make a PUT request to the view
        response = self.client.put(reverse('updateActiveHeartAudio', args=[encoded_audio_id, encoded_list_id]))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Update successfully')

    def test_update_active_lung_audio_view(self):
        print(" Method: test_update_active_lung_audio_view......")
        # Assuming you have an existing audio and list for the update
        audio_id = 18  # replace with the actual audio_id
        list_id = 2 # replace with the actual list_id
        
        # Encode URL parameters
        encoded_audio_id = quote(str(audio_id).encode('utf-8'))
        encoded_list_id = quote(str(list_id).encode('utf-8'))

        # Make a PUT request to the view
        response = self.client.put(reverse('updateActiveLungAudio', args=[encoded_audio_id, encoded_list_id]))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Update successfully')

    def test_update_list_content_view(self):
        print(" Method: test_update_list_content_view......")
        # Assuming you have an existing list for the update
        list_name_before = 'TestListBefore'  # replace with the actual list_name_before
        list_name_after = 'TestListAfter'  # replace with the actual list_name_after
        
        # Encode URL parameters
        encoded_list_name_before = quote(list_name_before)
        encoded_list_name_after = quote(list_name_after)

        # Make a PUT request to the view
        response = self.client.put(reverse('updateListContent', args=[encoded_list_name_before, encoded_list_name_after]))
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Update successfully')

    def test_upload_audio_view(self):
        print(" Method: test_upload_audio_view......")
        # Create a temporary audio file for testing
        file_content = b"Some binary audio content"
        audio_file = SimpleUploadedFile("test_audio.mp3", file_content, content_type="audio/mp3")

        # Make a POST request to the view
        response = self.client.post(reverse('uploadAudio'), {'file': audio_file})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertIn('filename', data)

        # Clean up: delete the temporary file
        file_path = os.path.join(settings.MEDIA_ROOT, 'audio', audio_file.name)
        os.remove(file_path)

    def test_delete_audio_file_view(self):
        print(" Method: test_delete_audio_file_view......")
        # Assuming you have an existing audio file in the media folder
        file_content = b"Some binary audio content"
        audio_file = InMemoryUploadedFile(
            BytesIO(file_content),
            'file',
            'test_audio.mp3',
            'audio/mp3',
            len(file_content),
            None
        )
        audio_file.seek(0)
        # Make a POST request to the view
        response = self.client.delete(reverse('delete_audio_file', args=[audio_file.name]))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Audio file deleted successfully.')

    def test_get_active_heart_audio_view(self):
        print(" Method: test_get_active_heart_audio_view......")
        # Assuming you have an existing list for the query
        list_id = 1  # replace with the actual list_id
        

        # Make a GET request to the view
        response = self.client.get(reverse('getActiveHeartAudio', args=[list_id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        if 'error' in data:
            # Check if the response indicates no audio found
            self.assertEqual(data['error'], 'No audio found for the given list ID')
        else:
            # Check if the response contains the expected key
            self.assertIn('audio_id', data)

    def test_get_active_lung_audio_view(self):
        print(" Method: test_get_active_lung_audio_view......")
        # Assuming you have an existing list for the query
        list_id = 1  # replace with the actual list_id
        

        # Make a GET request to the view
        response = self.client.get(reverse('getActiveLungAudio', args=[list_id]))

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        if 'error' in data:
            # Check if the response indicates no audio found
            self.assertEqual(data['error'], 'No audio found for the given list ID')
        else:
            # Check if the response contains the expected key
            self.assertIn('audio_id', data)
    # ...
# 2
# Test cases for models.py:
class TestModels(TestCase):
    # (1) For setup before each test case
    def setUp(self):
        # Set up test data
        self.audio = audio.objects.create(
            audio_id=1,  # Assign a valid audio_id
            audio_name='TestAudio',
            audio_type='Heartbeat',
            audio_link='test_audio.mp3',
        )
        self.user = user.objects.create(
            user_id = 114,
            user_name = "TianSuo",
            user_password = "1919810",
            user_log_state = True,
        )
        self.question = question.objects.create(
            question_id = 1,
        )
        # create test data for list and listContent
        self.list = audioList.objects.create(list_name='TestList')
        self.list_content = listContent.objects.create(
            list_name=self.list,
            audio_name=self.audio,
        )
        self.active_heart_audio = activeHeartAudio.objects.create(
            heart_audio_id=1,
            heart_audio_name='TestAudio',
            heart_audio_type='Heartbeat',
            heart_audio_description='TestAudio',
            heart_audio_level='Primary',
            heart_audio_link='test_audio.mp3',
            heart_audio_list=1,
        )
        self.active_lung_audio = activeLungAudio.objects.create(
            lung_audio_id = 0,
            lung_audio_name = "LungTestAudio",
            lung_audio_type = "LungAudio",
            lung_audio_description = "TestAudioLung",
            lung_audio_level = 'Primary',
            lung_audio_link = "test_lung.wav",
            lung_audio_list = 0,
        )

    # (2) Test cases for models.py:
    def test_audio_model(self):
        print(" Method: test_audio_model......")
        self.assertEqual(self.audio.audio_id, 1)
        self.assertEqual(self.audio.audio_name, 'TestAudio')
        self.assertEqual(self.audio.audio_type, 'Heartbeat')
        self.assertEqual(self.audio.audio_link, 'test_audio.mp3')

    def test_active_heart_audio_model(self):
        print(" Method: test_active_heart_audio_model......")
        self.assertEqual(self.active_heart_audio.heart_audio_id, 1)
        self.assertEqual(self.active_heart_audio.heart_audio_name, 'TestAudio')
        self.assertEqual(self.active_heart_audio.heart_audio_type, 'Heartbeat')
        self.assertEqual(self.active_heart_audio.heart_audio_description, 'TestAudio')
        self.assertEqual(self.active_heart_audio.heart_audio_level, 'Primary')
        self.assertEqual(self.active_heart_audio.heart_audio_link, 'test_audio.mp3')
        self.assertEqual(self.active_heart_audio.heart_audio_list, 1)

    def test_active_lung_audio(self):
        print("Method: test_active_lung_audio......")
        self.assertEqual(self.active_lung_audio.lung_audio_id,0)
        self.assertEqual(self.active_lung_audio.lung_audio_name,"LungTestAudio")
        self.assertEqual(self.active_lung_audio.lung_audio_type,"LungAudio")
        self.assertEqual(self.active_lung_audio.lung_audio_description,"TestAudioLung")
        self.assertEqual(self.active_lung_audio.lung_audio_level,"Primary")
        self.assertEqual(self.active_lung_audio.lung_audio_link,"test_lung.wav")
        self.assertEqual(self.active_lung_audio.lung_audio_list,0)

    def test_user(self):
        self.assertEqual(self.user.user_id,114)
        self.assertEqual(self.user.user_name,"TianSuo")
        self.assertEqual(self.user.user_password,"1919810")
        self.assertEqual(self.user.user_log_state,True)

    def test_question(self):
        self.assertEqual(self.question.question_id,1)

    def test_list_model(self):
        print(" Method: test_list_model......")
        self.assertEqual(self.list.list_name, 'TestList')

    def test_list_content_model(self):
        print(" Method: test_list_content_model......")
        self.assertEqual(self.list_content.list_name, self.list)
        self.assertEqual(self.list_content.audio_name, self.audio)

    # Add more test cases for other models.py...
    # ...

    # (3) For clean up 
    def tearDown(self):
        # Clean up test data
        self.audio.delete()
        self.list.delete()
        self.list_content.delete()
        
# 3
# Test cases for urls.py:        
class TestUrls(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Call 'initialDb' for initial database
        call_command('initialDb') 
        # Hint: When you need to deal with data in database, use this above line to initial database
        
    def test_home_url(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_play_random_heartbeat_url(self):
        response = self.client.get(reverse('playRandomHeartBeat'))
        self.assertEqual(response.status_code, 200)

    def test_play_random_abnormal_url(self):
        response = self.client.get(reverse('playRandomAbnormal'))
        self.assertEqual(response.status_code, 200)

    def test_play_random_url(self):
        response = self.client.get(reverse('playRandom'))
        self.assertEqual(response.status_code, 200)

    def test_get_all_audio_url(self):
        response = self.client.get(reverse('getAllAudio'))
        self.assertEqual(response.status_code, 200)

    def test_get_all_list_url(self):
        response = self.client.get(reverse('getAllList'))
        self.assertEqual(response.status_code, 200)

    def test_get_all_content_url(self):
        response = self.client.get(reverse('getAllContent'))
        self.assertEqual(response.status_code, 200)

    def test_delete_list_content_url(self):
        list_name = 1
        audio_name = 1
        response = self.client.delete(reverse('deleteListContent', args=[list_name, audio_name]))
        self.assertEqual(response.status_code, 200)

    def test_delete_related_list_content_url(self):
        audio_id = 1
        response = self.client.delete(reverse('deleteRelatedListContent', args=[audio_id]))
        self.assertEqual(response.status_code, 200)

    def test_update_list_content_url(self):
        list_name_before = 1
        list_name_after = 1
        response = self.client.post(reverse('updateListContent', args=[list_name_before, list_name_after]))
        self.assertEqual(response.status_code, 200)
    
    def test_update_active_heart_audio_url(self):
        audio_id = 1
        list_id = 1
        response = self.client.post(reverse('updateActiveHeartAudio', args=[audio_id, list_id]))
        self.assertEqual(response.status_code, 200)

    def test_update_active_lung_audio_url(self):
        audio_id = 1
        list_id = 1
        response = self.client.post(reverse('updateActiveLungAudio', args=[audio_id, list_id]))
        self.assertEqual(response.status_code, 200)

    def test_get_add_audio_url(self):
        response = self.client.get(reverse('addAudio'))
        self.assertEqual(response.status_code, 200)

    def test_audio_file_url(self):
        filename = '001.wav'
        encode_link = quote (filename)
        response = self.client.get(reverse('audio-file', args=[encode_link])) 
        self.assertEqual(response.status_code, 200)

    def test_upload_audio_url(self):
        response = self.client.post(reverse('uploadAudio'))
        self.assertEqual(response.status_code, 200)

    def test_delete_audio_file_url(self):
        link = '000.wav'
        encode_link = quote (link)
        response = self.client.delete(reverse('delete_audio_file', args=[encode_link])) 
        self.assertEqual(response.status_code, 404)

    def test_get_active_heart_audio_url(self):
        list_id = 1
        response = self.client.get(reverse('getActiveHeartAudio', args=[list_id]))
        self.assertEqual(response.status_code, 200)

    def test_get_active_lung_audio_url(self):
        list_id = 1
        response = self.client.get(reverse('getActiveLungAudio', args=[list_id]))
        self.assertEqual(response.status_code, 200)



    # Add more test cases for urls.py...
    # ...