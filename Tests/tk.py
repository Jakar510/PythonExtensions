# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2020.
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------

import queue
import random
from time import sleep
from typing import List, Union

from TkinterExtensions import *




print('TkinterExtensions.version', version)

class MainMenu_Colors: NumPadEntry = None

def _GetPhotoByteData() -> dict:
    """
        PhotoData.keys:
            exit

    :return:
    :rtype: dict
    """

    items = {
            'exit': b'iVBORw0KGgoAAAANSUhEUgAAAEYAAABGCAYAAABxLuKEAAAAAXNSR0IArs4c6QAAAARnQU1BAACx\njwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAAYdEVYdFNvZnR3YXJlAHBhaW50Lm5ldCA0LjEu'
                    b'\n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\nAAAAAElFTkSuQmCC\n',
            }

    return items
PhotoData = _GetPhotoByteData()

q = queue.Queue()

class HTMLViewer(HTMLLabel):
    def __init__(self, master, **kwargs):
        self.master = master
        super().__init__(master=master, **kwargs)

    # def HandlePress(self, event: tkEvent): TkinterEvent.Debug(event)
    # def HandleRelease(self, event: tkEvent): TkinterEvent.Debug(event)
    # def HandleFocusIn(self, event: tkEvent): TkinterEvent.Debug(event)
    # def HandleFocusOut(self, event: tkEvent): TkinterEvent.Debug(event)


d = ItemCollection.Parse([
        {
                "ID":       "G1",
                "Name":     "G Item 1",
                "Children": [
                        {
                                "ID":       "G1.O1",
                                "Name":     "G1.O1 Item 1",
                                "Children": [
                                        {
                                                "ID":   "G1.O1.I1",
                                                "Name": "G1.O1.I1 Item 1",
                                                },
                                        {
                                                "ID":   "G1.O1.I2",
                                                "Name": "G1.O1.I2 Item 2",
                                                },
                                        ],
                                },
                        {
                                "ID":       "G1.O2",
                                "Name":     "G1.O2 Item 2",
                                "Children": [
                                        {
                                                "ID":   "G1.O2.I1",
                                                "Name": "G1.O2.I1 Item 1",
                                                },
                                        {
                                                "ID":   "G1.O2.I2",
                                                "Name": "G1.O2.I2 Item 2",
                                                },
                                        ],
                                },
                        ],
                },
        {
                "ID":       "G2",
                "Name":     "G Item 2",
                "Children": [
                        {
                                "ID":       "G2.O1",
                                "Name":     "G2.O1 Item 1",
                                "Children": [
                                        {
                                                "ID":   "G2.O1.I1",
                                                "Name": "G2.O1.I1 Item 1",
                                                },
                                        {
                                                "ID":   "G2.O1.I2",
                                                "Name": "G2.O1.I2 Item 2",
                                                },
                                        ],
                                },
                        {
                                "ID":       "G2.O2",
                                "Name":     "G2.O2 Item 2",
                                "Children": [
                                        {
                                                "ID":   "G2.O2.I1",
                                                "Name": "G2.O2.I1 Item 1",
                                                },
                                        ],
                                },
                        {
                                "ID":   "G2.O3",
                                "Name": "G2.O3 Item 3",
                                },
                        ],
                },
        ])

class Root(tkRoot):
    # sets up Tkinter and creates the other windows and places them accordingly.
    def __init__(self):
        super().__init__(Screen_Width=800, Screen_Height=480, x=200, y=200)

        self.w: List[tk.Widget] = []
        self.home = HomeWindow(master=self).PlaceFull()

        # self.html = HTMLScrolledText(master=self).PlaceFull()
        # self.html.txt = 'Test'
        # self.html.hide()
        #
        # self.other = Widgets.Label(master=self, text='PlaceHodler').PlaceRelative(relx=0.5, rely=0, relwidth=.5, relheight=1)
        #
        # self.t = HTMLViewer(master=self).PlaceRelative(relx=0, rely=0, relwidth=.5, relheight=1)
        # self.t.txt = 'events'
        # self.Bind(Bindings.Key, self.HandlePress)
        # self.Bind(Bindings.ButtonPress, self.HandlePress)
        # self.Bind(Bindings.ButtonRelease, self.HandlePress)

        self.nb = NotebookThemed(master=self, height=30).PlaceFull()

        self.style.configure('Treeview', rowheight=40, font="-family {Segoe UI Black} -size 12 -slant roman -underline 0 -overstrike 0")
        self.p2 = TreeViewHolderThemed(master=self.nb, backgroundColor='white').PlaceFull()
        self.nb.Add(self.p2, title='page 1')
        self.TreeView = self.p2.TreeView

        self.TreeView.SetItems(d)
        self.TreeView.SetCommand(self.OnClick)
        bold_font = "-family {Segoe UI Black} -size 16 -weight bold -slant roman -underline 0 -overstrike 0"
        self.TreeView.SetTags(sel=dict(foreground='green', font=bold_font))

        self.p1 = Label(master=self.nb, text='page 1').PlaceFull()
        self.nb.Add(self.p1, title='page 2')

        # AutoStartTargetedThread(target=self.__run__)


    # noinspection PyUnusedLocal
    def OnClick(self, event: tk.Event = None):
        self.TreeView.OnSelectRow(event)

    @staticmethod
    def HandlePress(event: tkEvent): TkinterEvent.Debug(event)

    def Run(self): self.mainloop()

    def __run__(self):
        while True:
            cls = random.choice([Window1, Window2, Window3, LabelWindow])
            self.home.Add(cls)
            # DebugWidget(self.home, root=self, Message='__run__')

            sleep(2)
            # self.after(1000, self.__run__)

class HomeWindow(Frame):
    def __init__(self, master: Root):
        self.root = master
        super().__init__(master)
        self.w: List[Widgets.Button] = []

    def Add(self, cls: Union[Frame, LabelFrame]):
        assert (callable(cls))
        w = cls(master=self.root).PlaceFull()
        b = Widgets.Button(master=self, text=f'{w.__class__.__name__} [ {len(self.root.w)} ]')
        b.SetCommand(lambda: self.closeWindow(w))
        i = len(self.root.w)
        self.Grid_RowConfigure(i, weight=1)
        self.Grid_ColumnConfigure(0, weight=1)
        b.Grid(column=0, row=i)
        w.hide()
        self.root.w.append(w)

    def closeWindow(self, w: Union[Frame, LabelFrame]):
        w.show()
        self.root.home.hide()



class BaseWindow(Frame):
    button: Widgets.Button
    CreateWidgets: callable
    def __init__(self, master: Root):
        self.master = master
        super().__init__(master)
        self.CreateWidgets()

    def exit(self):
        self.hide()
        self.master.home.show()

    def OnAppearing(self):
        self.button.SetPhoto(PhotoData['exit'])

class Window1(BaseWindow):
    def CreateWidgets(self):
        self.button = Widgets.Button(master=self, text="button 1").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)



class Window2(BaseWindow):
    def CreateWidgets(self):
        self.button = Widgets.Button(master=self, text="button 2").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


class Window3(BaseWindow):
    nested: Window2
    def CreateWidgets(self):
        self.button = Widgets.Button(master=self, text="button 3").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.5)
        self.nested = LabelWindow(master=self).Place(relx=0.5, rely=0.0, relheight=1.0, relwidth=0.5)


class LabelWindow(LabelFrame):
    button: Widgets.Button
    CreateWidgets: callable
    def __init__(self, master: Root or BaseWindow):
        self.master = master
        super().__init__(master, text=str(self.__class__.__name__))
        self.button = Widgets.Button(master=self, text="button 4").SetCommand(self.exit).Place(relx=0.0, rely=0.0, relheight=1.0, relwidth=0.5)

    def exit(self):
        self.hide()
        self.master.home.show()



def test():
    """ https://stackoverflow.com/questions/7878730/ttk-treeview-alternate-row-colors """
    from random import choice




    colors = ["red", "green", "black", "blue", "white", "yellow", "orange", "pink", "grey", "purple", "brown"]
    def recolor():
        for child in tree.TreeView.get_children():
            picked = choice(colors)
            tree.TreeView.item(child, tags=(picked,), values=(picked,))
        for color in colors:
            tree.TreeView.tag_configure(color, background=color)
        tree.TreeView.tag_configure("red", background="red")


    root = tkRoot(800, 480, 200, 200)
    print('tkinter.info.patchlevel', root.tk.call('info', 'patchlevel'))

    style = Style(root)
    style.configure("Treeview", foreground="yellow", background="black", fieldbackground="green")

    frame = Frame(root).PlaceFull().SetID(1234)
    print(frame.__name__)
    print(str(frame))
    print(repr(frame))
    tree = TreeViewHolderThemed(frame, backgroundColor='white')

    tree.TreeView["columns"] = ("one", "two", "three")
    tree.TreeView.column("#0", width=100, minwidth=30, stretch=Bools.NO)
    tree.TreeView.column("one", width=120, minwidth=30, stretch=Bools.NO)

    tree.TreeView.heading("#0", text="0", anchor=AnchorAndSticky.West)
    tree.TreeView.heading("one", text="1", anchor=AnchorAndSticky.West)

    for i in range(30): tree.TreeView.insert("", i, text=f"Elem {i} ", values="none")

    tree.Pack(side=Side.top, fill=Fill.both, expand=True)

    Button(frame, text="Change").SetCommand(recolor).Pack(fill=tk.X)

    root.mainloop()

def test1():
    Root().Run()


def run_all():
    # from TkinterExtensions.Widgets.KeyBoard import KeyBaordTestFrame
    # KeyBaordTestFrame.test()
    # test()
    # test1()
    pass

if __name__ == '__main__':
    run_all()
