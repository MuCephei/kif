import unittest
from util.regular_expressions import *

# Are regular expression normally a good idea?
# No
# Are they fun?
# Yes
# Fun wins

class TwoWords(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(two_words.match('enable fun'))
        self.assertFalse(two_words.match('enabl'))
        self.assertFalse(two_words.match('enable'))
        self.assertTrue(two_words.match('enabe fun'))
        self.assertFalse(two_words.match('enable '))
        self.assertFalse(two_words.match('enable fun a'))
        self.assertFalse(two_words.match('enable f-un'))

    def test_get_command(self):
        self.assertEqual(two_words.match('enable fun').group('first'), 'enable')

    def test_get_name(self):
        self.assertEqual(two_words.match('enable fun').group('second'), 'fun')

class CallResponse(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(call_response.match('Call:helloworld Response:dlrowolleh'))
        self.assertTrue(call_response.match('Call:hell0world Response:dlrow0lleh'))
        self.assertTrue(call_response.match('Call:H Response:D'))
        self.assertTrue(call_response.match('Call:H" " Response:D{}'))
        self.assertTrue(call_response.match('Call:H Response:Q Response:D'))
        self.assertTrue(call_response.match('Call:H Response:Q Call:s Response:D'))
        self.assertTrue(call_response.match('Call:H Call:H Response:D Response:D'))

    def test_non_match_case(self):
        self.assertFalse(call_response.match('Cal:helloworld Response:dlrowolleh'))
        self.assertFalse(call_response.match('Callhell0world Response:dlrow0lleh'))
        self.assertFalse(call_response.match('sCall:H Response:D'))
        self.assertFalse(call_response.match('Call:H" " Resonse:D{}'))
        self.assertFalse(call_response.match('Call:H Rsponse:Q ResponseD'))

class RemoveResponse(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(remove_response.match('Remove:helloworld Response:dlrowolleh'))
        self.assertTrue(remove_response.match('Remove:hell0world Response:dlrow0lleh'))
        self.assertTrue(remove_response.match('Remove:H Response:D'))
        self.assertTrue(remove_response.match('Remove:H" " Response:D{}'))
        self.assertTrue(remove_response.match('Remove:H Response:Q Response:D'))
        self.assertTrue(remove_response.match('Remove:H Response:Q Call:s Response:D'))
        self.assertTrue(remove_response.match('Remove:H Call:H Response:D Response:D'))

    def test_non_match_case(self):
        self.assertFalse(remove_response.match('Remov:helloworld Response:dlrowolleh'))
        self.assertFalse(remove_response.match('Removehell0world Response:dlrow0lleh'))
        self.assertFalse(remove_response.match('sRemove:H Response:D'))
        self.assertFalse(remove_response.match('Remove:H" " Resonse:D{}'))
        self.assertFalse(remove_response.match('Remove:H Rsponse:Q ResponseD'))

if __name__ == '__main__':
    unittest.main()
