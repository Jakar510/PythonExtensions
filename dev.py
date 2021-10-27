from PythonExtensions.tk import *




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

        self.random = Button(self, text='self._app.random').PackHorizontal().SetCommand(self._app.random)

        self.showPopup = Button(self, text='show label window').PackHorizontal()
        self.p = Popup(self, app).PlaceFull()
        self.p.hide()
        self.showPopup.SetCommand(self.p.show)

        self.label = Label(self, 'test label').PackHorizontal()
        self.entry = Entry(self, 'test entry').PackHorizontal()
        self.check = CheckButton(self, 'test check').PackHorizontal()
        self.lb = Listbox(self).PackHorizontal().SetList(['one', 'two', 'three'])
        self.text = Text(self, 'test text').PackHorizontal()
        self.scrolledText = ScrolledText(self, 'test scrolled text').PackHorizontal()
        self.scale = Scale(self).PackHorizontal()
        self.canvas = Canvas(self).PackHorizontal()
        self.canvas.DownloadImage(r'https://astronomy.com/-/media/Images/News%20and%20Observing/Sky%20this%20Week/STW%202021/June/summerevening.jpg?mw=600', 0, 0)


if __name__ == '__main__':
    # App.InitAsync()
    _app = App(app_name='test app', root_path='..')

    # _app.root.after(3000, _app.Close)

    _app.start_gui()
    # _app.start_gui_Async()

pass


# import asyncio
# from timeit import timeit
#
# from PythonExtensions.Models import WebApi
#
#
#
#
# url = WebApi('https://google.com')
#
#
# def get(): asyncio.get_event_loop().run_until_complete(getAsync())
# async def getAsync():
#     async with url as session:
#         reply = await session.get()
#         await reply.read()
#
#
# def test(number: int):
#     _globals = globals()
#     print(timeit("get()", number=number, globals=_globals) / number)
#
#
# if __name__ == '__main__':
#     for i in range(1, 100):
#         test(i)
