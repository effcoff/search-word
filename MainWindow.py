from kivy.app import App
from kivy.config import Config
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.lang import Builder
from kivy.uix.widget import Widget

from WordSearch import WordSerach

Config.set('graphics', 'width', '500')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', 0)

LabelBase.register(DEFAULT_FONT, "font.ttf")

Builder.load_string(
'''
#:kivy 1.9.1

<MainWindow>:
    GridLayout:
        cols: 1
        pos: root.pos
        size: root.size
        padding: 20

        Label:
            text: 'Search Word'
            font_size: 60
            text_size: root.size
            halign: 'center'
            valign: 'middle'
            size_hint_y: None
            height: 100

        GridLayout:
            cols: 3
            size_hint_y: 1
            spacing: 5
            size_hint_y: None
            height: 50
            spacing: 5
            padding: 0,0,0,10

            Label:
                text: '検索:'
                font_size: 20
                size_hint_x: 0.2

            TextInput:
                id: search_word_input
                text: ''
                multiline: False
                font_size: self.height / 1.5

            Button:
                text: '検索'
                font_size: 20
                size_hint_x: 0.3
                on_press: root.search_word(search_word_input.text, result_box)

        Label:
            font_size: 20
            text_size: self.width, None
            size_hint_y: None
            height: self.texture_size[1] + 10
            halign: 'center'
            valign: 'middle'
            text: '----  検索結果  ----'

        ScrollView:
            Label:
                id: result_box
                font_size: 17
                text_size: self.width - 10, None
                size_hint_y: None
                height: self.texture_size[1]
                valign: 'top'
                color: 0,0,0,1

                canvas.before:
                    Color:
                        rgba: 1,1,1,1
                    Rectangle:
                        pos: self.pos
                        size: self.size

''')


class MainWindow(Widget):
    def __init__(self):
        super().__init__()

        self.ws = WordSerach()

    def search_word(self, value, result_box):
        self.ws.insertDB(value)
        mean = self.ws.readWord(value)
        string = '\n'.join(mean)
        result_box.text += string + '\n\n'


if __name__ in ('__main__'):
    class MainApp(App):
        title = 'Search Word'

        def __init__(self):
            super().__init__()

        def build(self):
            return MainWindow()


    MainApp().run()
