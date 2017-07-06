import regex
from util.autovivifier import Autovivifier

# I don't want crazy regular expressions mucking up the normal code
# Also makes it easier to test

def make_words_regex(n):
    numbers = [str(i) for i in range(n)]
    word = 'word'
    sections = ['(?P<' + word + number + '>[\S]+)' for number in numbers]
    start = '\A'
    middle = '\s+'
    end = '\Z'
    return regex.compile(start + middle.join(sections) + end)

words = Autovivifier(make_words_regex)
call_response = regex.compile('\A\s*(?P<call>.*)&gt;&gt;&gt;(?P<response>.*)\Z')
remove_response = regex.compile('\A\s*(?P<call>.*)&lt;&lt;&lt;(?P<response>.*)\Z')
word_call_response = regex.compile('\A\s*{(?P<call>.*)}&gt;&gt;&gt;(?P<response>.*)\Z')
word_remove_response = regex.compile('\A\s*{(?P<call>.*)}&lt;&lt;&lt;(?P<response>.*)\Z')
