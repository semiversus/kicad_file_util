""" Serialisation and Deserialisation of S-Expressions """

import re
from typing import Any

match_whitespace = re.compile(r'\s+').match
match_string = re.compile(r'"(?:\\.|[^"\\])*"').match
match_symbol = re.compile(r'[^\s)"]+').match

WHITESPACE_STR = ' \t\n\r'


class Expression:
    def __init__(self, elements: list):
        self.elements = elements

    def __str__(self):
        return '(' + ' '.join(str(e) for e in self.elements) + ')\n'


def _parse(sexpr: str, index: int = 0) -> tuple[Any, int]:
    length = len(sexpr)
    elements = []

    while index < length:
        character = sexpr[index]
        if sexpr[index] in WHITESPACE_STR:
            index = match_whitespace(sexpr, index).end()
            character = sexpr[index]

        if character == '(':
            element, index = _parse(sexpr, index + 1)
        elif character == ')':
            return Expression(elements), index + 1
        elif character == '"':
            match = match_string(sexpr, index)

            if not match:
                raise ValueError(f'Invalid string at {index}: {sexpr[index:index+12]}...')

            element = match[0]
            index = match.end()
        else:
            match = match_symbol(sexpr, index)
            if not match:
                raise ValueError(f'Invalid string at {index}: {sexpr[index:index+12]}...')

            element = match[0]
            index = match.end()

        elements.append(element)

        if sexpr[index] != ')':
            index += 1

    if index != 0:
        raise ValueError('Invalid expression: unterminated')

    return elements[0], index


def parse(sexpr: str) -> Any:
    assert sexpr[0] == '('
    return _parse(sexpr, 1)[0]


if __name__ == '__main__':
    with open('/home/guenther/law/projects/labstack/pcb/pcb/labstack.kicad_pcb') as f:
        sexpr = f.read()

    obj = parse(sexpr)
    sexpr = str(obj)

    with open('dump.kicad_pcb', 'w') as f:
        f.write(sexpr)
