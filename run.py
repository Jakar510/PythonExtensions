from Tests import *




def TestApps():
    from PythonExtensions.tk import BaseApp, BaseWindow, BaseLabelWindow, Button

    class App(BaseApp):
        main: 'Main'
        def test(self): print(self)
        def random(self): print('random', self)

        def start_gui(self):
            self.main = Main.Root(self)
            return super(App, self).start_gui()



    class Popup(BaseLabelWindow[App]):
        def __init__(self, master, app):
            super().__init__(master, app, text='Popup')
            self.PlaceFull()
            self.rb = Button(self, text='hide').PackFull().SetCommand(self.hide)



    class Main(BaseWindow[App]):
        def __init__(self, master, app):
            super().__init__(master, app)
            self.PlaceFull()
            self.rb = Button(self, text='self._app.random').PackFull().SetCommand(self._app.random)

            self.lb = Button(self, text='show label window').PackFull()

            self.l = Popup(self, app).PlaceFull()
            self.l.hide()

            self.lb.SetCommand(self.l.show)



    _app = App(app_name='test app', root_path='.')

    _app.root.after(2000, _app.Close)
    _app.start_gui()



if __name__ == '__main__':
    # TestApps()
    Run()
