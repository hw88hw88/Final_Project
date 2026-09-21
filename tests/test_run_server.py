import unittest
import run_server
import datetime
import json

class TestChatbot(unittest.TestCase):
    # test if the class, variables and functions can be created successfully or not
    def test_class_functions(self):
        self.assertIsNotNone(run_server)
        self.assertIsNotNone(run_server.clear_job_and_background)
        self.assertIsNotNone(run_server.pending_response_generator)
        self.assertIsNotNone(run_server.chatbot_generate_response)
        self.assertIsNotNone(run_server.chatbot_new_job_api)
        self.assertIsNotNone(run_server.about)
        self.assertIsNotNone(run_server.chatbot_get_status)
        self.assertIsNotNone(run_server.app)
        self.assertIsNotNone(run_server.user_background)
        self.assertIsNotNone(run_server.user_background_lock)
        self.assertIsNotNone(run_server.jobs)
        self.assertIsNotNone(run_server.jobs_lock)
        self.assertIsNotNone(run_server.bot)
        self.assertIsNotNone(run_server.bot_lock)

    # test clear_job_and_background()
    def test_clear_job_and_background(self):
        # generating job id for the test
        job_id = str(datetime.datetime.now())
        job_id = job_id.replace(' ', '_')
        job_id = job_id.replace(':', '-')
        job_id = 'job_id' + str(job_id)

        # generating sender for the test
        sender = str(datetime.datetime.now())
        sender = sender.replace(' ', '_')
        sender = sender.replace(':', '-')
        sender = 'sender' + str(sender)

        run_server.jobs[str(job_id)] = {
            'status': 'pending',
            'user_message': 'testing',
            'chatbot_response': 'Working...',
            'sender': sender,
            'creation_time': datetime.datetime(2026, 9, 1)
        }
        run_server.user_background[sender] = {
            'creation_time': datetime.datetime(2026, 9, 1)
        }
        self.assertIsNotNone(run_server.jobs.get(str(job_id)))
        self.assertIsNotNone(run_server.user_background.get(sender))
        run_server.clear_job_and_background()
        self.assertIsNone(run_server.jobs.get(str(job_id)))
        self.assertIsNone(run_server.user_background.get(sender))

        run_server.jobs[str(job_id)] = {
            'status': 'pending',
            'user_message': 'testing',
            'chatbot_response': 'Working...',
            'sender': sender,
            'creation_time': datetime.datetime.now()
        }
        run_server.user_background[sender] = {
            'creation_time': datetime.datetime.now()
        }
        run_server.clear_job_and_background()
        self.assertIsNotNone(run_server.jobs.get(str(job_id)))
        self.assertIsNotNone(run_server.user_background.get(sender))

        # remove the test objects
        run_server.jobs = {}
        run_server.user_background = {}

    # test pending_response_generator()
    def test_pending_response_generator(self):
        response = run_server.pending_response_generator()
        self.assertIsNotNone(response)
        self.assertEqual(str(type(response)), "<class 'str'>")
        self.assertGreater(len(response), 1)

    # test chatbot_generate_response()
    def test_chatbot_generate_response(self):
        # generating job id for the test
        job_id = str(datetime.datetime.now())
        job_id = job_id.replace(' ', '_')
        job_id = job_id.replace(':', '-')
        job_id = 'job_id' + str(job_id)

        # generating sender for the test
        sender = str(datetime.datetime.now())
        sender = sender.replace(' ', '_')
        sender = sender.replace(':', '-')
        sender = 'sender' + str(sender)

        run_server.jobs[str(job_id)] = {
            'status': 'pending',
            'user_message': 'testing',
            'chatbot_response': '',
            'sender': sender,
            'creation_time': datetime.datetime(2026, 9, 1)
        }

        run_server.chatbot_generate_response(
            sender=sender,
            message='hi',
            job_id=job_id
        )

        self.assertIsNotNone(run_server.jobs.get(str(job_id)).get('chatbot_response'))
        # successful generation should return a string with length greater than 0
        self.assertGreater(len(run_server.jobs.get(str(job_id)).get('chatbot_response')), 0)

    # test endpoint chatbot_new_job_api()
    def test_chatbot_new_job_api(self):
        self.client = run_server.app.test_client()

        # test GET method
        response = self.client.get('/')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

        # test POST method
        response = self.client.post('/', json={"sender":"tester", "message":"hi"})
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(type(response.json)), "<class 'dict'>")
        self.assertEqual(str(type(response.json['sender'])), "<class 'str'>")
        self.assertEqual(response.json['sender'], "tester")
        self.assertEqual(str(type(response.json['text'])), "<class 'str'>")
        self.assertGreater(len(response.json['text']), 0)
        self.assertIsNotNone(response.json['job_id'])
        self.assertEqual(str(type(response.json['job_id'])), "<class 'str'>")
        job_id = response.json['job_id']
        sender = response.json['sender']

        # test chatbot_get_status()
        ## keep the unit test running when the LLM is running to avoid error after the test
        while True:
            response = self.client.get('/status?job_id=' + str(job_id))
            self.assertIsNotNone(response)
            self.assertEqual(response.status_code, 200)
            if response.json['status'] == 'completed':
                self.assertEqual(response.json['sender'], sender)
                break

    # test endpoint about()
    def test_about(self):
        self.client = run_server.app.test_client()
        # test GET method
        response = self.client.get('/about')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)

    # test chatbot_get_status()
    def test_chatbot_get_status(self):
        self.client = run_server.app.test_client()
        # test GET method
        response = self.client.get('/status')
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 400)

                # generating job id for the test
        job_id = str(datetime.datetime.now())
        job_id = job_id.replace(' ', '_')
        job_id = job_id.replace(':', '-')
        job_id = 'job_id' + str(job_id)

        # generating sender for the test
        sender = str(datetime.datetime.now())
        sender = sender.replace(' ', '_')
        sender = sender.replace(':', '-')
        sender = 'sender' + str(sender)

        run_server.jobs[str(job_id)] = {
            'status': 'pending',
            'user_message': 'testing',
            'chatbot_response': '',
            'sender': sender,
            'creation_time': datetime.datetime(2026, 9, 1)
        }

        response = self.client.get('/status?job_id=' + str(job_id))
        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['sender'], sender)


