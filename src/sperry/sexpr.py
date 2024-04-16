""" Serialisation and Deserialisation of S-Expressions """

import re
from typing import Any

match_whitespace = re.compile(r'\s+').match
match_string = re.compile(r'"(?:\\.|[^"\\])*"').match
match_number = re.compile(r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?', (re.DOTALL)).match
match_symbol = re.compile(r'[^\s)"]+').match

WHITESPACE_STR = ' \t\n\r'

class Symbol:
    def __init__(self, value: str):
        self.value = value
    
    def __repr__(self):
        return f'{self.value}'


class Expression:
    def __init__(self, elements: list):
        self.elements = elements

    def __repr__(self):
        return f'{self.__class__.__name__}({self.elements})'
    

def _parse(sexpr: str, index: int = 0) -> tuple[Any, int]:
    length = len(sexpr)
    elements = []

    while index < length:
        if sexpr[index] in WHITESPACE_STR:
            index += len(match_whitespace(sexpr, index)[0])

        if sexpr[index] == '(':
            element, index = _parse(sexpr, index + 1)
        elif sexpr[index] == ')':
            return Expression(elements), index + 1
        elif sexpr[index] == '"':
            match = match_string(sexpr, index)
    
            if not match:
                raise ValueError(f'Invalid string at {index}: {sexpr[index:index+12]}...')
    
            element = match[0][1:-1]
            index = match.end()
        else:
            # taken from simplejson
            m = match_number(sexpr, index)
            if m and sexpr[m.end()] in WHITESPACE_STR + ')':
                integer, frac, exp = m.groups()
                if frac or exp:
                    element = float(integer + (frac or '') + (exp or ''))
                else:
                    element = int(integer)
                index = m.end()
            else:
                m = match_symbol(sexpr, index)
                if m:
                    element = Symbol(m[0])
                    index = m.end()
                else:
                    raise ValueError(f'Invalid expression at {index}: {sexpr[index:index+12]}...')

        elements.append(element)
    
    if index != 0:
        raise ValueError('Invalid expression: unterminated')

    return elements[0], index

def parse(sexpr: str) -> Any:
    assert sexpr[0] == '('
    return _parse(sexpr, 1)[0]

def dump(obj: Any) -> str:
    if isinstance(obj, Symbol):
        return obj.value
    elif isinstance(obj, Expression):
        return '(' + ' '.join(dump(e) for e in obj.elements) + ')\n'
    elif isinstance(obj, str):
        return f'"{obj}"'
    else:
        return str(obj)
                   
if __name__ == '__main__':
    with open('/home/guenther/law/projects/labstack/pcb/pcb/labstack.kicad_pcb') as f:
        sexpr = f.read()
    
    obj = parse(sexpr)
    sexpr = dump(obj)

    with open('dump.kicad_pcb', 'w') as f:
        f.write(sexpr)
    