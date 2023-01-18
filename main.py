from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatter import Scatter
from kivy.utils import get_color_from_hex

from kivy.config import Config

from math import pow


class myApp(App):
    def build(self):
        self.OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
                          '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y), '^': (3, lambda x, y: pow(x, y)), }

        s = Scatter()
        self.main_grid = GridLayout(size=(360, 800), cols=1)
        s.add_widget(self.main_grid)

        self.lb = TextInput(multiline=False, readonly=True,
                            halign="right", font_size=32)
        self.main_grid.add_widget(self.lb)

        self.buttons_grid = GridLayout(
            size=(360, 360), cols=4, spacing=3, padding=3)
        self.main_grid.add_widget(self.buttons_grid)

        green_color = '#0a8c06'
        blue_color = '#051580'
        gray_color = '#44454a'

        self.gen_button(green_color, 'AC')
        self.gen_button(blue_color, '( )')
        self.gen_button(blue_color, '^')
        self.gen_button(blue_color, '/')

        self.gen_button(gray_color, '8')
        self.gen_button(gray_color, '7')
        self.gen_button(gray_color, '9')
        self.gen_button(blue_color, '*')

        self.gen_button(gray_color, '4')
        self.gen_button(gray_color, '5')
        self.gen_button(gray_color, '6')
        self.gen_button(blue_color, '-')

        self.gen_button(gray_color, '1')
        self.gen_button(gray_color, '2')
        self.gen_button(gray_color, '3')
        self.gen_button(blue_color, '+')

        self.gen_button(gray_color, '0')
        self.gen_button(gray_color, '.')
        self.gen_button(gray_color, '<=')
        self.gen_button(blue_color, '=')

        return s

    def gen_button(self, color_hex, text):
        btn = Button(
            background_color=get_color_from_hex(color_hex),
            text=text,
            background_normal='',
        )
        btn.fbind('on_press', self.btn_press, text)
        self.buttons_grid.add_widget(btn)

    def btn_press(self, text: str, instance):
        if text.isdigit():
            if self.lb.text == '0':
                self.lb.text = text
            else:
                self.lb.text += text
        elif text in self.OPERATORS.keys():
            if len(self.lb.text) > 0 and self.lb.text[-1] not in self.OPERATORS.keys():
                self.lb.text += text
        elif text == 'AC':
            self.lb.text = ''
        elif text == '<=':
            self.lb.text = self.lb.text[:-1]
        elif text == '.':
            comma_count = 0
            for s in self.lb.text[::-1]:
                if s == '.':
                    comma_count += 1
                elif not s.isdigit():
                    break
            if comma_count == 0:
                self.lb.text += text

        elif text == '( )':
            if self.lb.text[-1] in self.OPERATORS.keys():
                self.lb.text += '('
            else:
                c_break = 0
                for s in self.lb.text:
                    if s == '(':
                        c_break += 1
                    if s == ')':
                        c_break -= 1
                if c_break == 0:
                    self.lb.text += '('
                else:
                    self.lb.text += ')'
        elif text == '=':
            res = self.calc(
                self.shunting_yard(self.parse(self.lb.text)))
            if res % 10 == 0:
                res = int(res)
            self.lb.text = str(res)

    def parse(self, formula_string):
        number = ''
        for s in formula_string:
            if s.isdigit() or s == '.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in self.OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(self, parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in self.OPERATORS.keys():
                while stack and stack[-1] != "(" and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(self, polish):
        stack = []
        for token in polish:
            if token in self.OPERATORS.keys():
                y, x = stack.pop(), stack.pop()
                stack.append(self.OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]


if __name__ == "__main__":
    Config.set('graphics', 'resizable', '0')
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '800')
    Config.write()
    myApp().run()
