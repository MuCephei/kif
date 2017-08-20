import regex
from util.autovivifier import Autovivifier
import constants as k

# I don't want crazy regular expressions mucking up the normal code
# Also makes it easier to test
# As a side note, these are probably a bad idea, but they are fun

def make_words_regex(n):
    numbers = [str(i) for i in range(n)]
    word = 'word'
    sections = ['(?P<' + word + number + '>[\S]+)' for number in numbers]
    start = '\A'
    middle = '\s+'
    end = '\Z'
    return regex.compile(start + middle.join(sections) + end)

words = Autovivifier(make_words_regex)
call_response = regex.compile('\A\s*(?P<' +k.call + '>.*)&gt;&gt;&gt;(?P<' +k.response + '>.*)\Z')
remove_response = regex.compile('\A\s*(?P<' +k.call + '>.*)&lt;&lt;&lt;(?P<' +k.response + '>.*)\Z')
word_call_response = regex.compile('\A\s*{(?P<' +k.call + '>.*)}&gt;&gt;&gt;(?P<' +k.response + '>.*)\Z')
word_remove_response = regex.compile('\A\s*{(?P<' +k.call + '>.*)}&lt;&lt;&lt;(?P<' +k.response + '>.*)\Z')
alias_call_response = regex.compile('\A\s*\[(?P<' +k.call + '>.*)\]&gt;&gt;&gt;(?P<' +k.response + '>.*)\Z')
alias_remove_response = regex.compile('\A\s*\[(?P<' + k.call + '>.*)\]&lt;&lt;&lt;(?P<' + k.response + '>.*)\Z')


dice = regex.compile('\s*(?P<' + k.number_dice + '>[0-9]+)d(?P<' + k.dice_type +
                     '>[0-9]+)\s*((?P<' + k.dice_sign + '>[\+-])\s*(?P<' + k.dice_modifier + '>[0-9]+))?\s*')

args_regex = regex.compile('--(?P<' + k.arg + '>\S+)(\s+(?P<' + k.value + '>[^-\s]+)\s*)?')