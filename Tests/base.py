from PythonExtensions.Json import *



def Test_base():
    start = Point.Create(0, 0)
    end = Point.Create(150, 150)
    pic_pos = PlacePosition.Create(10, 10)
    img_size = Size.Create(200, 200)

    print(CropBox.Box(start=start, end=end, pic=pic_pos, img=img_size))



if __name__ == '__main__':
    Test_base()
