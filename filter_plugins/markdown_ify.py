# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re

def markdown_ify(data):
    '''
    U(url) -> url
    M(module) -> link to ansible module document
    I(text) -> _text_ or *text*
    C(text) -> `text`
    '''
    #paren_re = r'\(((?:\([^)]*\)|[^)])*)\)'
    #data = re.sub(r'U%s' % paren_re, r'\1', data) # U(url) -> url
    #data = re.sub(r'M%s' % paren_re, r'[\1](http://docs.ansible.com/ansible/\1_module.html)', data) # M(module) -> link to module
    #data = re.sub(r'I%s' % paren_re, r'_\1_', data) # I(word) -> _word_
    #data = re.sub(r'C%s' % paren_re, r'`\1`', data) # C(word) -> `word`
    #return data
    pos = 0
    exp = re.compile(r'([UMIC])\(|[()]')
    context = []
    result = []
    while True:
        m = exp.search(data,pos)
        if m is None:
            break
        if m.group(0) == '(':
            context.append('(') 
            result.append(data[pos:m.end()])
        elif m.group(0) == ')':
            if not context:
                result.append(data[pos:m.end()])
            else:
                c = context.pop()
                if c == 'U':
                    result[-1] += data[pos:m.start()]
                elif c == 'M':
                    t = result[-1] + data[pos:m.start()]
                    result[-1] = '[%s](http://docs.ansible.com/ansible/%s_module.html)' % (t,t)
                elif c == 'I':
                    t = result[-1] + data[pos:m.start()]
                    if '_' in t:
                        s = '*'
                    else:
                        s = '_'
                    result[-1] = s+t+s
                elif c == 'C':
                    t = result[-1] + data[pos:m.start()]
                    result[-1] = '`%s`' % t
                else: # context='('
                    result[-1] += data[pos:m.end()]
        else:
            # U()/M()/I()/C()
            result.append(data[pos:m.start()])
            result.append("")
            context.append(m.group(1)) 
        pos = m.end()
    if not result:
        return data
    return "".join(result)
    

class FilterModule(object):
    ''' Evaluate formatting function in ansible doc string as Markdown '''

    def filters(self):
        return {
            'markdown_ify': markdown_ify
        }
