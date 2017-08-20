import unittest
from util.regular_expressions import *

# Are regular expression normally a good idea?
# No
# Are they fun?
# Yes
# Fun wins

class TwoWords(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(words[2].match('enable fun'))
        self.assertFalse(words[2].match('enabl'))
        self.assertFalse(words[2].match('enable'))
        self.assertTrue(words[2].match('enabe fun'))
        self.assertFalse(words[2].match('enable '))
        self.assertFalse(words[2].match('enable fun a'))
        self.assertTrue(words[2].match('enable f-un'))

    def test_get_first(self):
        self.assertEqual(words[2].match('enable fun').group('word0'), 'enable')

    def test_get_second(self):
        self.assertEqual(words[2].match('enable fun').group('word1'), 'fun')

class ThreeWords(unittest.TestCase):
    def test_match_case(self):
        self.assertFalse(words[3].match('enable fun'))
        self.assertTrue(words[3].match('enable fun centaur'))

    def test_get_first(self):
        self.assertEqual(words[3].match('enable fun centaur').group('word0'), 'enable')

    def test_get_second(self):
        self.assertEqual(words[3].match('enable fun centaur').group('word1'), 'fun')

    def test_get_third(self):
        self.assertEqual(words[3].match('enable fun centaur').group('word2'), 'centaur')

class CallResponse(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(call_response.match('helloworld&gt;&gt;&gt;Response'))
        self.assertTrue(call_response.match(' helloworld&gt;&gt;&gt;dlrowolleh'))
        self.assertTrue(call_response.match('hell0world &gt;&gt;&gt;dlrow0lleh'))
        self.assertTrue(call_response.match('H&gt;&gt;&gt; D'))
        self.assertTrue(call_response.match('H" " &gt;&gt;&gt; D{}'))

    def test_non_match_case(self):
        self.assertFalse(call_response.match(''))
        self.assertFalse(call_response.match('Call:hell0world Response:dlrow0lleh'))
        self.assertFalse(call_response.match('a&gt;&gt;b'))
        self.assertFalse(call_response.match('a&lt;&lt;&lt;b'))

    def test_call(self):
        self.assertEqual(call_response.match('a&gt;&gt;&gt;b').group('call'),
                         'a')
        self.assertEqual(call_response.match(' a&gt;&gt;&gt;b').group('call'),
                         'a')
        self.assertEqual(call_response.match(' a &gt;&gt;&gt;b').group('call'),
                         'a ')
        self.assertEqual(call_response.match('aa&gt;&gt;a&gt;&gt;&gt;b').group('call'),
                         'aa&gt;&gt;a')

    def test_response(self):
        self.assertEqual(call_response.match('a&gt;&gt;&gt;b').group('response'),
                         'b')
        self.assertEqual(call_response.match('a&gt;&gt;&gt; b').group('response'),
                         ' b')
        self.assertEqual(call_response.match('a&gt;&gt;&gt; b ').group('response'),
                         ' b ')
        self.assertEqual(call_response.match('a&gt;&gt;&gt;b ').group('response'),
                         'b ')

class RemoveResponse(unittest.TestCase):
    def test_match_case(self):
        self.assertTrue(remove_response.match('helloworld&lt;&lt;&lt;Response'))
        self.assertTrue(remove_response.match(' helloworld&lt;&lt;&lt;dlrowolleh'))
        self.assertTrue(remove_response.match('hell0world &lt;&lt;&lt;dlrow0lleh'))
        self.assertTrue(remove_response.match('H&lt;&lt;&lt; D'))
        self.assertTrue(remove_response.match('H" " &lt;&lt;&lt; D{}'))

    def test_non_match_case(self):
        self.assertFalse(remove_response.match(''))
        self.assertFalse(remove_response.match('Call:hell0world Response:dlrow0lleh'))
        self.assertFalse(remove_response.match('a&lt;&lt;b'))
        self.assertFalse(remove_response.match('a&gt;&gt;&gt;b'))

    def test_call(self):
        self.assertEqual(remove_response.match('a&lt;&lt;&lt;b').group('call'),
                         'a')
        self.assertEqual(remove_response.match(' a&lt;&lt;&lt;b').group('call'),
                         'a')
        self.assertEqual(remove_response.match(' a &lt;&lt;&lt;b').group('call'),
                         'a ')
        self.assertEqual(remove_response.match('aa&lt;&lt;a&lt;&lt;&lt;b').group('call'),
                         'aa&lt;&lt;a')

    def test_response(self):
        self.assertEqual(remove_response.match('a&lt;&lt;&lt;b').group('response'),
                         'b')
        self.assertEqual(remove_response.match('a&lt;&lt;&lt; b').group('response'),
                         ' b')
        self.assertEqual(remove_response.match('a&lt;&lt;&lt; b ').group('response'),
                         ' b ')
        self.assertEqual(remove_response.match('a&lt;&lt;&lt;b ').group('response'),
                         'b ')

class Dice(unittest.TestCase):
    def test_easy(self):
        self.assertTrue(dice.match('1d6'))
        self.assertTrue(dice.match(' 1d6 '))
        self.assertTrue(dice.match(' 1d6 + 7'))
        self.assertTrue(dice.match('1d6+7'))

    def test_non_match_case(self):
        self.assertFalse(dice.match('16'))
        self.assertFalse(dice.match('d6 + 7'))

    def test_n(self):
        self.assertEqual(dice.match('1d6+7').group('n'), '1')
        self.assertEqual(dice.match('10d6+7').group('n'), '10')
        self.assertEqual(dice.match('01d6+7').group('n'), '01')
        self.assertEqual(dice.match('7d6').group('n'), '7')

    def test_m(self):
        self.assertEqual(dice.match('1d6+7').group('m'), '6')
        self.assertEqual(dice.match('10d060+7').group('m'), '060')

    def test_sign(self):
        self.assertEqual(dice.match('1d6+7').group('sign'), '+')
        self.assertEqual(dice.match('10d060-7').group('sign'), '-')

    def test_q(self):
        self.assertEqual(dice.match('1d6+7').group('q'), '7')
        self.assertEqual(dice.match('10d060-7').group('q'), '7')

    def test_multiple(self):
        self.assertEqual(dice.findall('1d6 + 4 2d3'), [('1', '6', '+ 4', '+', '4'), ('2', '3', '', '', '')])
        self.assertEqual(dice.findall('1d6 + 4 + 2d3 - 7'), [('1', '6', '+ 4', '+', '4'), ('2', '3', '- 7', '-', '7')])


class Arg(unittest.TestCase):
    def test_no_agrs(self):
        self.assertFalse(args_regex.search('kif'))
        self.assertFalse(args_regex.search('Wow what a nice day outside.'))

    def test_arg(self):
        self.assertEqual(args_regex.search('dice --show').group('arg'), 'show')

    def test_named_args(self):
        self.assertEqual(args_regex.findall('dice --show'), [('show', '', '')])
        self.assertEqual(args_regex.findall('dice --show --a'), [('show', '', ''), ('a', '', '')])

    def test_valued_args(self):
        self.assertEqual(args_regex.findall('dice --show true'), [('show', ' true', 'true')])
        self.assertEqual(args_regex.findall('dice --show yes --a no'), [('show', ' yes ', 'yes'), ('a', ' no', 'no')])

    def test_value(self):
        self.assertEqual(args_regex.search('dice --show true').group('value'), 'true')

if __name__ == '__main__':
    unittest.main()
