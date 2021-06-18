from typing import *

from PIL.Image import Image as _Image

from .Base import *
from .Common import *
from .Keys import Keys




__all__ = ['Size', 'Ratios', 'Point', 'PlacePosition', 'CropBox']

class Size(BaseDictModel[str, int]):
    __slots__ = []
    @property
    def width(self) -> int: return self[Keys.width]
    @property
    def height(self) -> int: return self[Keys.height]

    def ToTuple(self) -> Tuple[int, int]: return int(self.width), int(self.height)
    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def __eq__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.width == other.width and self.height == other.height

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __ne__(self, other: Union[Tuple[int, int], List[int], 'Size']): return not self.__eq__(other)

    def __gt__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.width > other.width and self.height > other.height

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __lt__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.width < other.width and self.height < other.height

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __ge__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.width >= other.width and self.height >= other.height

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __le__(self, other: Union[Tuple[int, int], List[int], 'Size']):
        if isinstance(other, (tuple, list)):
            other = Size.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.width <= other.width and self.height <= other.height

        raise TypeError(type(other), (self.__class__, tuple, list))


    @staticmethod
    def convert(o: Union['Size', _Image, Tuple[int, int]]) -> Tuple[int, int]:
        if isinstance(o, Size): return o.ToTuple()
        elif isinstance(o, _Image): return o.size
        elif isinstance(o, tuple): return o
        throw(o, Size, _Image, tuple)

    def Factors(self, widthMax: int, heightMax: int) -> Tuple[float, float]:
        # if widthMax > self.width or heightMax > self.height:
        #     return self.width / widthMax , self.height / heightMax

        return widthMax / self.width, heightMax / self.height

    def MinScalingFactor(self, widthMax: int, heightMax: int) -> float: return min(self.Factors(widthMax, heightMax))
    def MaxScalingFactor(self, widthMax: int, heightMax: int) -> float: return max(self.Factors(widthMax, heightMax))


    @overload
    def Scale(self, size: Union['Size', _Image, Tuple[int, int]], AsSize: bool) -> 'Size': ...
    @overload
    def Scale(self, size: Union['Size', _Image, Tuple[int, int]]) -> Tuple[int, int]: ...

    def Scale(self, size: Union['Size', _Image, Tuple[int, int]], AsSize: bool = False) -> Union['Size', tuple[int, int]]:
        w, h = self.convert(size)
        factor = self.MinScalingFactor(w, h)
        result = Size.Create(self.width * factor, self.height * factor)
        if AsSize: return result

        return result.ToTuple()

    @staticmethod
    def FromTuple(v: Tuple[int, int]): return Size.Create(*v)
    @classmethod
    def Create(cls, width: Union[int, float], height: Union[int, float]): return cls({ Keys.width: int(width), Keys.height: int(height) })
    @classmethod
    def Parse(cls, d):
        if d is None: return None
        if isinstance(d, dict):
            AssertKeys(d, Keys.width, Keys.height)
            return cls(d)

        throw(d, dict)
class Ratios(Size):
    @property
    def LANDSCAPE(self) -> float: return self.width / self.height
    @property
    def PORTRAIT(self) -> float: return self.height / self.width



class Point(BaseDictModel[str, int]):
    __slots__ = []
    @property
    def y(self) -> int: return self[Keys.y]
    @property
    def x(self) -> int: return self[Keys.x]

    def Set(self, x: int, y: int):
        self[Keys.x] = x
        self[Keys.y] = y
        return self

    def ToTuple(self) -> Tuple[int, int]: return int(self.x), int(self.y)
    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def __eq__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.x == other.y and self.y == other.y

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __ne__(self, other: Union[Tuple[int, int], List[int], 'Size']): return not self.__eq__(other)

    def __gt__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.x > other.x and self.y > other.y

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __lt__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.x < other.x and self.y < other.y

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __ge__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.x >= other.x and self.y >= other.y

        raise TypeError(type(other), (self.__class__, tuple, list))
    def __le__(self, other: Union[Tuple[int, int], List[int], 'Point']):
        if isinstance(other, (tuple, list)):
            other = Point.FromTuple(other)
        if isinstance(other, self.__class__):
            return self.x <= other.x and self.y <= other.y

        raise TypeError(type(other), (self.__class__, tuple, list))

    @classmethod
    def FromTuple(cls, v: Tuple[int, int]): return cls.Create(*v)
    @classmethod
    def Zero(cls): return cls.Create(0, 0)
    @classmethod
    def Create(cls, x: int, y: int): return cls({ Keys.x: x, Keys.y: y })
    @classmethod
    def Parse(cls, d):
        if d is None: return None
        if isinstance(d, dict):
            AssertKeys(d, Keys.x, Keys.y)
            return cls(d)

        throw(d, dict)
class PlacePosition(Point):
    """ tkinter uses top boundary as x axis. """
    def Right(self, amount: int):
        self[Keys.x] += amount
        return self
    def Left(self, amount: int):
        self[Keys.x] -= amount
        return self
    def Up(self, amount: int):
        self[Keys.y] -= amount
        return self
    def Down(self, amount: int):
        self[Keys.y] += amount
        return self

    @overload
    def Update(self, img: Size, view: Size) -> 'PlacePosition': ...
    # def Update(self,  img: Size, view: Size, AnyValue: Any) -> 'PlacePosition': ...

    @overload
    def Update(self, img: Size, view: Size, OnlyZero: Any) -> 'PlacePosition': ...

    @overload
    def Update(self, img: Size, view: Size, ZeroOrMore: Any) -> 'PlacePosition': ...

    @overload
    def Update(self, img: Size, view: Size, ZeroOrLess: Any) -> 'PlacePosition': ...

    @overload
    def Update(self, img: Size, view: Size, KeepInView: Any) -> 'PlacePosition': ...


    def Update(self, img: Size, view: Size, **kwargs) -> 'PlacePosition':
        """
            The goal is to force the object to comply within its bounds

            x, y: root left point of the box, in (x, y) format.
            : bottom right point of the box, in (x, y) format.

        :param view: size of the view where the photo/object is displayed
        :param img:  size of the photo, in (Width, Height) format.
        :return: PlacePosition
        """
        def XY(_v: int, _img: int, _edit: int, args: KeysView) -> float:
            if 'OnlyZero' in args: return 0

            if 'ZeroOrMore' in args: return _v if _v >= 0 else 0

            if 'ZeroOrLess' in args: return _v if _v <= 0 else 0

            if 'KeepInView' in args:
                if _img < _edit: return (_edit - _img) / 2

                if _v + _img < _edit: return - abs(_edit - _img)

                if _v > 0: return 0

                return _v

            return _v

        self[Keys.x] = int(XY(self.x, img.width, view.width, kwargs.keys()))
        self[Keys.y] = int(XY(self.y, img.height, view.height, kwargs.keys()))

        return self



class CropBox(BaseDictModel[str, int]):
    """  Adjusted box (x, y, width, height), ensuring that all dimensions resides within the boundaries. """
    __slots__ = []
    @property
    def y(self) -> int: return self[Keys.y]
    @property
    def x(self) -> int: return self[Keys.x]

    def Set(self, x: int, y: int):
        self[Keys.x] = x
        self[Keys.y] = y
        return self

    @property
    def width(self) -> int: return self[Keys.width]
    @property
    def height(self) -> int: return self[Keys.height]

    def Resize(self, width: int, height: int) -> 'CropBox':
        self[Keys.width] = width
        self[Keys.height] = height
        return self

    def __iter__(self) -> Iterable[int]: return iter(self.ToTuple())

    def IsAllVisible(self, pic: PlacePosition, img: Size) -> bool:
        return (pic.x >= 0 and
                pic.y >= 0 and
                (pic.y + img.height) <= self.height and
                (pic.x + img.width) <= self.width)

    def Update(self, pic: PlacePosition, img: Size, view: Size) -> 'CropBox':
        """
            The goal is to find the area of the object that is visible.

            x, y: root left point of the box, in (x, y) format.
            : bottom right point of the box, in (x, y) format.

        :param view: size of the view where the photo/object is displayed
        :param pic:  where the photo is placed, in (x, y) format. For Example: Canvas placements. This can be any integer
        :param img:  size of the photo, in (Width, Height) format.
        :return: CropBox
        """
        def XY(_v: int, _img: int, _edit: int) -> int:
            if _v > 0:
                if _v + _img < _edit:
                    return 0

                if _v + _img >= _edit:
                    return 0

                return _v

            elif _v < 0:
                if _v + _img <= _edit:
                    return - abs(_img - _edit)

                if _v + _img > _edit:
                    return _v

                return _v

            return 0


        self[Keys.x] = XY(pic.x, img.width, view.width)
        self[Keys.y] = XY(pic.y, img.height, view.height)


        def Width(_v: int, _img: int, _edit: int) -> int:
            if _v == 0:
                if _img < _edit:
                    return _img

                # img_h >= edit_h:
                return _edit

            elif _v > 0:
                if _v + _img >= _edit:
                    return _edit - _v

                if _v + _img < _edit:
                    return _img

                return _img

            else:  # _y < 0
                if _v + _img < _edit:
                    # print('__Width__', _v, _img, _edit)
                    return _img + _v

                # _y + img_h >= edit_h
                return _edit
        self[Keys.width] = Width(self.x, img.width, view.width)


        def Height(_v: int, _img: int, _edit: int) -> int:
            if _v == 0:
                if _img < _edit:
                    return _img

                # img_h >= edit_h:
                return _edit

            elif _v > 0:
                if _v + _img >= _edit:
                    return _edit - _v

                if _v + _img < _edit:
                    return _img

                return _img

            else:  # _y < 0
                if _v + _img < _edit:
                    # print('__Height__', _v, _img, _edit)
                    return _img + _v

                # _y + img_h >= edit_h
                return _edit
        self[Keys.height] = Height(self.y, img.height, view.height)

        return self

    def Scale(self, image_size: Union[Size, _Image, Tuple[int, int]]) -> Size: return self.ToPointSize()[1].Scale(image_size, AsSize=True)
    def EnforceBounds(self, image_size: Union[Size, _Image, Tuple[int, int]]) -> Tuple[int, int, int, int]:
        img_w, img_h = Size.convert(image_size)
        self.Set(int(self.x if self.x >= 0 else 0),
                 int(self.y if self.y >= 0 else 0))
        self.Resize(int(self.width if self.width <= img_w else img_w),
                    int(self.height if self.height <= img_h else img_h))

        return self.ToTuple()





    def ToTuple(self) -> Tuple[int, int, int, int]: return self.x, self.y, self.width, self.height
    def ToPointSize(self) -> Tuple[Point, Size]: return self.TopLeft, self.Size
    def ToPoints(self) -> Tuple[Point, Point]: return self.TopLeft, self.BottomRight
    def BoundaryPoints(self) -> Tuple[Point, Point, Point, Point]: return self.TopLeft, self.TopRight, self.BottomLeft, self.BottomRight

    @property
    def Size(self) -> Size: return Size.Create(self.width, self.height)
    @property
    def TopLeft(self) -> Point: return Point.Create(self.x, self.y)
    @property
    def TopRight(self) -> Point: return Point.Create(self.x + self.width, self.y)
    @property
    def BottomLeft(self) -> Point: return Point.Create(self.x, self.y + self.height)
    @property
    def BottomRight(self) -> Point: return Point.Create(self.x + self.width, self.y + self.height)

    # noinspection PyMethodOverriding
    @classmethod
    def Create(cls, x: int, y: int, width: int, height: int):
        return cls({
            Keys.x:      int(x),
            Keys.y:      int(y),
            Keys.width:  int(width),
            Keys.height: int(height),
            })
    @classmethod
    def Crop(cls, x: int, y: int, width: int, height: int, *, pic: PlacePosition, img: Size, edit: Size):
        o = cls.Create(x, y, width, height)
        o.Update(pic, img, edit)
        return o
    @classmethod
    def FromPoints(cls, start: Point, end: Point):
        x1, y1 = start
        x2, y2 = end
        return cls.Create(x1, y1, x2 - x1, y2 - y1)
    @classmethod
    def FromPointSize(cls, start: Point, size: Size):
        x1, y1 = start
        w, h = size
        return cls.Create(x1, y1, w, h)



    @classmethod
    @overload
    def Box(cls, start: Point, end: Point, pic: PlacePosition, img: Size) -> 'CropBox': ...
    @classmethod
    @overload
    def Box(cls, start: Point, end: Size, pic: PlacePosition, img: Size) -> 'CropBox': ...
    @classmethod
    @overload
    def Box(cls, x: int, y: int, width: int, height: int, pic: PlacePosition, img: Size) -> 'CropBox': ...

    @classmethod
    def Box(cls, **kwargs) -> 'CropBox':
        pic = kwargs['pic']
        img = kwargs['img']
        assert (isinstance(pic, PlacePosition))
        assert (isinstance(img, Size))
        if 'x' in kwargs:
            x, y = kwargs['x'], kwargs['y']
            width, height = kwargs['width'], kwargs['height']
            assert (isinstance(x, int))
            assert (isinstance(y, int))
            assert (isinstance(width, int))
            assert (isinstance(height, int))
            return cls._Box(Point.Create(x, y), Point.Create(x + width, y + height), pic, img)
        else:
            start = kwargs['start']
            end = kwargs['end']
            assert (isinstance(start, Point))
            if isinstance(end, Size):
                return cls._Box(start, Point.Create(start.x + end.width, start.y + end.height), pic, img)

            assert (isinstance(end, Point))
            return cls._Box(start, Point.Create(end.x, end.y), pic, img)
    @classmethod
    def _Box(cls, start: Point, end: Point, pic: PlacePosition, img: Size) -> 'CropBox':
        """
        :param start: root start point of the box, in (x, y) format.
        :param end: root end point of the box, in (x, y) format.
        :param pic:  root left point of the photo, in (x, y) format.
        :param img:  size of the photo, in (width, height) format.
        :return: adjusted box dimensions, ensuring that it resides within the photo.
        """

        x1, y1 = start
        x2, y2 = end

        # going right
        x1 = x1 if x1 > pic.x else pic.x
        y1 = y1 if y1 > pic.y else pic.y

        # going left
        x1 = x1 if x1 < pic.x + img.width else pic.x + img.width
        y1 = y1 if y1 < pic.y + img.height else pic.y + img.height

        # going right
        x2 = x2 if x2 < pic.x + img.width else pic.x + img.width
        y2 = y2 if y2 < pic.y + img.height else pic.y + img.height

        # going left
        x2 = x2 if x2 > pic.x else pic.x
        y2 = y2 if y2 > pic.y else pic.y

        return cls.Create(int(x1), int(y1), int(x2 - x1), int(y2 - y1))



    @classmethod
    def Parse(cls, d):
        if isinstance(d, dict):
            AssertKeys(d, Keys.width, Keys.height, Keys.x, Keys.y)
            for k, v in d.items():
                d[k] = int(v)

            return cls(d)

        throw(d, dict)
