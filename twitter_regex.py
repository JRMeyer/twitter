'''
This regex comes from Christopher Potts @ Stanford
'''

import re

### 
##  Define all the regexes!
#

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                                                                    # eyes
      [\-o\*\']?                                                                # optional nose
      [\)\]\(\[dDpP/\:\}\{@\|\\]*                                                # mouth
      |                                                                         #### reverse, reverse
      [\)\]\(\[dDpP/\:\}\{@\|\\]*                                                # mouth
      [\-o\*\']?                                                                # optional nose
      [:;=8]                                                                    # eyes
      [<>]?
    )"""

regex_strings = (
    r"""                                                                        # Phone numbers regex
    (?:
      (?:                                                                       # (international)
        \+?[01]
        [\-\s.]*
      )?            
      (?:                                                                       # (area code)
        [\(]?
        \d{3}
        [\-\s.\)]*
      )?           
      \d{3}                                                                     # exchange
      [\-\s.]*   
      \d{4}                                                                     # base
    )"""
    ,
    r"""https?://[\S]+"""                                                     # URL regex
    ,
    emoticon_string                                                             # Emoticons
    ,
    r"""<[^>]+>"""                                                              # HTML tags
    ,
    r"""(?:@[\w_]+)"""                                                          # Twitter username
    ,
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""                                        # Twitter hashtags
    ,
    r"""                                                                        # Remaining word types
    (?:[a-z][a-z'\-_]+[a-z])                                                    # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)                                               # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                                                                  # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})                                                         # Ellipsis dots. 
    |
    (?:\S)                                                                      # Everything else that isn't whitespace.
    """
    )

#
##
###



### 
##  Compile all the regexes!
#

word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), 
                     re.VERBOSE | re.I | re.UNICODE)                            # core tokenizing regex

emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)      # emoticons own regex to preserve case if needed

html_entity_digit_re = re.compile(r"&#\d+;")                                    # These are for regularizing
html_entity_alpha_re = re.compile(r"&\w+;")                                     # HTML entities to Unicode:
amp = "&amp;"                                                                   #

#
##
###
