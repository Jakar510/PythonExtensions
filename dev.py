from typing import *

from PythonExtensions.tk import *




class App(BaseAsyncApp):
    main: 'Main'

    def test(self, _event: Optional[tkEvent] = None): print(self)
    def random(self, _event: Optional[tkEvent] = None): print('random', self)


    def _setup(self):
        self.main = Main(self)


    def Handle_KeyPress(self, event: TkinterEvent) -> Optional[bool]: pass
    def Handle_Press(self, event: TkinterEvent) -> Optional[bool]: pass


class Popup(BaseLabelWindow[App]):
    def __init__(self, master, app):
        super().__init__(master, app, text='Popup')
        self.PlaceFull()
        self.rb = Button(self, text='hide').PackFull().SetCommand(self.hide)



class Main(BaseWindow[App]):
    def __init__(self, app: App):
        super().__init__(app, app)
        self.PlaceFull()

        # self.random = Button(self, text='self._app.random').PackHorizontal().SetCommand(self._app.random)
        #
        # self.showPopup = Button(self, text='show label window').PackHorizontal()
        # self.p = Popup(self, app).PlaceFull()
        # self.p.hide()
        # self.showPopup.SetCommand(self.p.show)
        #
        # self.label = Label(self, 'test label').PackHorizontal()
        # self.entry = Entry(self, 'test entry').PackHorizontal()
        # self.check = CheckButton(self, 'test check').PackHorizontal()
        # self.lb = Listbox(self).PackHorizontal().SetList(['one', 'two', 'three'])
        # self.text = Text(self, 'test text').PackHorizontal()
        # self.scrolledText = ScrolledText(self, 'test scrolled text').PackHorizontal()
        # self.scale = Scale(self).PackHorizontal()
        # self.canvas = Canvas(self).PackHorizontal()
        # self.canvas.DownloadImage(r'https://astronomy.com/-/media/Images/News%20and%20Observing/Sky%20this%20Week/STW%202021/June/summerevening.jpg?mw=600', 0, 0)

        self.kb = KeyboardEntry(self, app, PopupOptions(relx=0.3025, rely=0.5, relwidth=0.2995, relheight=0.2),
                                font='-family {Segoe UI Black} -size 20',
                                text='popup keyboard - popup keyboard - popup keyboard')
        self.kb.PlaceRelative(.3, .2, .3, .3)

        self.tkb = TitledKeyboardEntry(self, app, PopupOptions(relx=0.3, rely=0.4, relwidth=0.3, relheight=0.2))
        self.tkb.Title.configure(font='-family {Segoe UI Black} -size 20')
        # noinspection PyArgumentList
        self.tkb.Value.configure(text='popup keyboard - popup keyboard - popup keyboard')
        self.tkb.PlaceRelative(.3, .6, .3, .3)


if __name__ == '__main__':
    _app = App('test app')

    # _app.root.after(3000, _app.Close)

    _app.start_gui()

pass

#
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
