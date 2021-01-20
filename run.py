import random

from PythonExtensions.Files import *
from PythonExtensions.Images import ImageObject
from PythonExtensions.Json import *
from PythonExtensions.tk import *




# from Tests import RUN_TESTS


if __name__ == '__main__':
    # d = Path.MakeDirectories(Path.Join('.', 'temp'))
    # print(d)
    # print(d.FileName)
    # print(d.extension())
    # file = Path.Join(d, 't.txt')
    # with open(file, 'w') as f: f.write(str(d))
    # print(file)
    # print(file.FileName)
    # print(file.extension())
    #
    # file.Remove()
    # d.Remove()

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
            print('label: ', label.size)
            img = ImageObject(img, label.width, label.height, AutoResize=False)
            box = CropBox.Create(0, 0, img.width / 0.75, img.height / 0.75)
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
