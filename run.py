import random

from PythonExtensions.Files import *
from PythonExtensions.Images import ImageObject
from PythonExtensions.Json import *
from PythonExtensions.tk import *




from Tests import RUN_TESTS
def CheckPaths():
    d = Path.MakeDirectories(Path.Join('.', 'temp'))
    print(d)
    print(d.FileName)
    print(d.extension())
    file = Path.Join(d, 't.txt')
    with open(file, 'w') as f: f.write(str(d))
    print(file)
    print(file.FileName)
    print(file.extension())

    file.Remove()
    d.Remove()
def checkImage():
    root = tkRoot()
    frame = Frame(root).PlaceFull()
    label = Canvas(frame).PlaceFull()
    root.update()
    root.update_idletasks()

    # init = (1335, 1080)
    # RUN_TESTS()
    paths = Path.ListDir(r'D:\WorkSpace\SmartPhotoFrame\client\src\.images')
    path = random.choice(paths)
    with open(path, 'rb') as f:
        with ImageObject.open(f) as img:
            print('init: ', img.size)
            print('label: ', label.img_size)
            img = ImageObject(img, label.width, label.height, AutoResize=False)
            box = CropBox.Create(0, 0, label.width, label.height)
            img.CropZoom(box, size=(img.width, img.height))
            # img.Resize(box=box, check_metadata=False)
            # img.Resize(size=(2960 * 1.2, 1440 * 1.2), box=box, check_metadata=False)
            # img.Resize(check_metadata=False)

            x = int((label.width - img.Raw.width) / 2)
            y = int((label.height - img.Raw.height) / 2)
            print(dict(x=x, y=y))
            items = label.CreateImage(img.Raw, x, y)
            print(items)
    root.mainloop()
def run():
    RUN_TESTS()

if __name__ == '__main__':
    run()
    # screen = Size.Create(1920, 1080)
    # screen = Size.Create(1366, 768)
    screen = Size.Create(3820, 2160)

    # img_size = Size.Create(1920, 1080)
    # start = Point.Create(0, 0)

    window = Size.Create(1920, 1080)

    for w in (2560,):  # 1024, 1366,  1920, 3820
        for h in (1600,):  # 768, 864, 1080, 2160
            for x in range(-1500, 500, 50):
                for y in range(-750, 500, 50):
                    start = PlacePosition.Create(x, y)
                    img_size = Size.Create(w, h)

                    box = CropBox.FromPointSize(start, window)
                    box.Update(start, img=img_size, view=window)
                    # if box.IsAllVisible(start, img_size):
                    #     print('_______UPDATE______', w, h, window)

                    # box = CropBox.BoxSize(start, window, start, img_size)
                    if not box.IsAllVisible(start, img_size):
                        print('_______BOX______', start.ToTuple(), img_size.ToTuple(), box)
                        print()

                    # result = box.Scale(screen)
                    # print('__Scale__', result <= screen)

    # for x in range(-100, 100, 25):
    #     for y in range(-100, 100, 25):
    #         point = Point.Create(x, y)
    #
    #         print()
    #         box = CropBox.FromPointSize(start, window)
    #         box.Update(point, img=img_size, view=window)
    #         print('_______UPDATE______', x, y, box.IsAllVisible(point, img_size))
    #
    #
    #         box = CropBox.BoxSize(start, window, point, img_size)
    #         print('_______BOX______', x, y, box.IsAllVisible(point, img_size))
    #
    #         result = box.Scale(screen).ToTuple()
    #         print('__Scale__', result, result > screen)
    #         print()
