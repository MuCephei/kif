import regex

# I don't want crazy regular expressions mucking up the normal code
# Also makes it easier to test

two_words = regex.compile('\A(?P<first>[a-z]+)\s(?P<second>[a-z]+)\Z')
call_response = regex.compile('\ACall:(?P<call>.+)\sResponse:(?P<response>.+)\Z')
remove_response = regex.compile('\ARemove:(?P<remove>.+)\sResponse:(?P<response>.+)\Z')
