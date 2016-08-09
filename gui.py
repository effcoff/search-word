from MainWindow import MainWindow
from kivy.app import App

class MainApp(App):
    title = 'Search Word'

    def __init__(self):
        super().__init__()

    def build(self):
        return MainWindow()

if __name__ in ('__main__'):
    MainApp().run()
