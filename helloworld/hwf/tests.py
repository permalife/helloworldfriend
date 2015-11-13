from django.test import TestCase
from datetime import datetime, timedelta

import requests


class HelloWorldFriendTestCase(TestCase):
    """
    Unit test suite framework for testing HelloWorldFriend app
    """
    def setUp(self):
        self.url = 'http://localhost:8000/greet/'
        self.invalid1 = {'name': 'Joe', 'datetime': '20151111'}

        utcnow = datetime.utcnow()
        self.invalid2 = {
            'name': 'Joe',
            'datetime': datetime.strftime(
                utcnow - timedelta(seconds=60),
                '%Y%m%d%H%M%S'
            ),
        }
        self.valid = {
            'name': 'Joe',
            'datetime': datetime.strftime(
                utcnow + timedelta(seconds=60),
                '%Y%m%d%H%M%S'
            ),
        }

    def testGet(self):
        """
        HTTP/GET is not supported for this app
        """
        res = requests.get(self.url, params=self.valid)
        self.assertEqual(res.status_code, 400)
        self.assertIn('GET is not supported', res.content)

    def testPostNoJson(self):
        """
        Data is not posted as JSON
        """
        res = requests.post(self.url, data=self.valid)
        self.assertEqual(res.status_code, 400)
        self.assertIn('JSON string expected', res.content)

    def testPostInvalidDateTimeString(self):
        """
        Invalid datetime string provided in the request
        """
        res = requests.post(self.url, json=self.invalid1)
        self.assertEqual(res.status_code, 400)
        self.assertIn('Invalid date format', res.content)

    def testPostPastDateTime(self):
        """
        Requested greeting time is in the past
        """
        res = requests.post(self.url, json=self.invalid2)
        self.assertEqual(res.status_code, 400)
        self.assertIn('time is in the past', res.content)

    def testPostValid(self):
        """
        A valid friend greeting request
        """
        res = requests.post(self.url, json=self.valid)
        self.assertEqual(res.status_code, 200)
        self.assertIn('will be greeted', res.content)
