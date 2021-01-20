# ------------------------------------------------------------------------------
#  Created by Tyler Stegmaier
#  Copyright (c) 2021.
#
# ------------------------------------------------------------------------------

import base64
import os
import tempfile
from io import BytesIO
from urllib.request import urlopen

from PIL import ImageFile, ImageTk
from PIL.Image import BICUBIC, EXTENSION, Exif, Image, init, new, open as img_open

from .ImageExtensions import *
from ..Exceptions import ArgumentError
from ..Files import *
from ..Json import *
from ..debug import PrettyPrint




__all__ = [
    'ImageObject',
    'ImageTk',
    'ImageExtensions',
    ]

class ImageObject(object):
    __slots__ = ['_img', '_path', '_fp', '_widthMax', '_heightMax', '_name_']
    _path: Path
    _fp: Optional[BytesIO]
    _img: Image
    _widthMax: Optional[int]
    _heightMax: Optional[int]
    def __init__(self, img: Optional[Image], widthMax: Optional[int] = None, heightMax: Optional[int] = None, *, AutoResize: bool = True, LOAD_TRUNCATED_IMAGES: bool = True):
        self._img = img
        self.SetMaxSize(widthMax, heightMax)
        if AutoResize and widthMax and heightMax:
            print('AutoResized')
            self.Resize(check_metadata=True)
        ImageFile.LOAD_TRUNCATEDImageS = LOAD_TRUNCATED_IMAGES

    @property
    def Raw(self) -> Image: return self._img
    @property
    def width(self) -> int: return self._img.width
    @property
    def height(self) -> int: return self._img.height
    @property
    def size(self) -> Size: return Size.Create(self._img.width, self._img.height)

    @staticmethod
    def open(fp, **kwargs) -> Image: return img_open(fp, **kwargs)
    @staticmethod
    def NewImage(size: Tuple[int, int], mode: str = 'RGB', color: Tuple[int, int, int] = (0, 0, 0)) -> Image: return new(mode, size, color=color)


    def __name__(self, extension: ImageExtensions) -> str:
        try:
            return self._name_
        except AttributeError:
            self._name_ = f'{hash(self)}.{extension.value}'
            return self._name_
    def _TempFilePath(self, extension: ImageExtensions) -> Path: return File.TemporaryFile(self.__module__, name=self.__name__(extension), root_dir=tempfile.gettempdir())
    def __enter__(self):
        # noinspection PyTypeChecker
        self._fp = open(self._path, 'wb')
        self._img = img_open(self._fp)
        return self
    def __exit__(self, *args):
        # exc_type, exc_val, exc_tb = args
        if not self._path.IsTemporary and self._fp and all(arg is None for arg in args): self.save()

        if self._fp:
            if hasattr(self, '_temp'): os.remove(self._temp)
            self._img.close()
            self._fp.close()
            self._fp = None
    def __call__(self, path: Path = None, *, extension: ImageExtensions = None):
        if not path and not extension:
            raise ArgumentError('Must Provide either the file path or the image type extension')

        self._path = path or self._TempFilePath(extension)  # ImageExtensions(path.extension({ '.': '' })
        return self
    def save(self, fp: BinaryIO = None): self._img.save(fp or self._fp)

    def SetMaxSize(self, widthMax: Optional[int], heightMax: Optional[int]):
        self._widthMax = widthMax
        self._heightMax = heightMax


    @property
    def _factors(self) -> Tuple[float, float]: return self._widthMax / self._img.width, self._heightMax / self._img.height
    def Maximum_ScalingFactor(self) -> float: return max(self._factors)
    def Minimum_ScalingFactor(self) -> float: return min(self._factors)
    def CalculateNewSize(self) -> Tuple[int, int]:
        scalingFactor = self.Minimum_ScalingFactor()
        return int(scalingFactor * self._img.width), int(scalingFactor * self._img.height)
    def _Scale(self, factor: float) -> Tuple[int, int]: return int(self._img.width * (factor or 1)), int(self._img.height * (factor or 1))


    def Rotate(self, angle: Union[int, RotationAngle] = None, *, expand: bool = True, Offset: Tuple[int, int] = None, fill_color=None, center=None, resample=BICUBIC) -> 'ImageObject':
        """
            CAUTION: Offset will TRIM the image if moved out of bounds of the

        :param fill_color:
        :param center:
        :param resample:
        :param Offset: int in range 0-360 angle to rotate
        :param angle:
        :param expand:
        :return:
        """
        if angle is None: return self
        if isinstance(angle, RotationAngle): angle = angle.value
        self._img = self._img.rotate(angle=angle, expand=expand, translate=Offset, fillcolor=fill_color, center=center, resample=resample)
        return self

    def Crop(self, box: CropBox) -> 'ImageObject':
        self._img = self._img.crop(box.EnforceBounds(self._img.size))
        return self

    def CropZoom(self, box: CropBox, size: Union[Size, Tuple[int, int]], *, reducing_gap: float = 3.0) -> 'ImageObject':
        try:
            if isinstance(size, Size): size = size.ToTuple()
            elif isinstance(size, tuple): size = tuple(map(int, size))
            else: raise TypeError(type(size), (Size, tuple))

            # self._img = self._img.resize(size=size, reducing_gap=reducing_gap)
            self.Resize(size, reducing_gap=reducing_gap, check_metadata=False)
            self.Crop(box)
            self.Resize(reducing_gap=reducing_gap, check_metadata=False)
            return self
        finally:
            PrettyPrint('__CropZoom__kwargs__',
                        box=box,
                        size=size,
                        reducing_gap=reducing_gap,
                        _widthMax=self._widthMax,
                        _heightMax=self._heightMax,
                        result=self.size,
                        _CalculateNewSize=self.CalculateNewSize())


    def Zoom(self, factor: float, *, reducing_gap: float = None) -> 'ImageObject':
        self._img = self._img.resize(size=self._Scale(factor), reducing_gap=reducing_gap)
        return self

    def Resize(self, size: Union[Size, Tuple[int, int]] = None, box: CropBox = None, *, check_metadata: bool, reducing_gap: float = None, resample=BICUBIC) -> 'ImageObject':
        if check_metadata:
            exif: Exif = self._img.getexif()
            if 'Orientation' in exif:  # check if image has exif metadata.
                if exif['Orientation'] == 3:
                    self.Rotate(RotationAngle.upside_down)
                elif exif['Orientation'] == 6:
                    self.Rotate(RotationAngle.left)
                elif exif['Orientation'] == 8:
                    self.Rotate(RotationAngle.right)

        kwargs = dict(resample=resample, reducing_gap=reducing_gap)
        if box: kwargs['box'] = box.EnforceBounds(image_size=self._img.size)

        if isinstance(size, Size): kwargs['size'] = size.ToTuple()
        elif isinstance(size, tuple): kwargs['size'] = tuple(map(int, size))
        elif isinstance(self._widthMax, (int, float)) and isinstance(self._heightMax, (int, float)): kwargs['size'] = self.CalculateNewSize()

        try:
            self._img = self._img.resize(**kwargs)
        except:
            PrettyPrint('__Resize__kwargs__', kwargs=kwargs, _widthMax=self._widthMax, _heightMax=self._heightMax, result=self.size)
            raise

        return self

    def ToPhotoImage(self, master=None, **kwargs) -> ImageTk.PhotoImage: return ImageTk.PhotoImage(master=master, image=self._img, **kwargs)



    @classmethod
    @overload
    def FromFile(cls, path: Union[str, Path], *, width: int = None, height: int = None, AsPhotoImage) -> ImageTk.PhotoImage: ...
    @classmethod
    @overload
    def FromFile(cls, path: Union[str, Path], *, width: int = None, height: int = None) -> Image: ...

    @classmethod
    def FromFile(cls, path: Union[str, Path], *, width: int = None, height: int = None, AsPhotoImage=None):
        Assert(path, str, Path)

        with open(path, 'rb') as f:
            with cls.open(f) as img:
                o = cls(img, width, height)
                if AsPhotoImage is not None: return o.ToPhotoImage(master=AsPhotoImage, width=width, height=height)
                return o.Raw



    @classmethod
    @overload
    def FromBase64(cls, path: Union[str, bytes], *, width: int = None, height: int = None, AsPhotoImage) -> ImageTk.PhotoImage: ...
    @classmethod
    @overload
    def FromBase64(cls, path: Union[str, bytes], *, width: int = None, height: int = None) -> Image: ...

    @classmethod
    def FromBase64(cls, data: Union[str, bytes], width: int = None, height: int = None, AsPhotoImage=None):
        Assert(data, str, bytes)
        return cls.FromBytes(base64.b64decode(data), width=width, height=height, AsPhotoImage=AsPhotoImage)



    @classmethod
    @overload
    def FromURL(cls, path: Union[str, bytes], *, width: int = None, height: int = None, AsPhotoImage) -> ImageTk.PhotoImage: ...
    @classmethod
    @overload
    def FromURL(cls, path: Union[str, bytes], *, width: int = None, height: int = None) -> Image: ...

    @classmethod
    def FromURL(cls, url: str, width: int = None, height: int = None, AsPhotoImage=None):
        Assert(url, str)
        return cls.FromBytes(urlopen(url).read(), width=width, height=height, AsPhotoImage=AsPhotoImage)



    @classmethod
    @overload
    def FromBytes(cls, path: Union[str, bytes], *formats: str, width: int = None, height: int = None, AsPhotoImage) -> ImageTk.PhotoImage: ...
    @classmethod
    @overload
    def FromBytes(cls, path: Union[str, bytes], *formats: str, width: int = None, height: int = None) -> Image: ...

    @classmethod
    def FromBytes(cls, data: bytes, *formats: str, width: int = None, height: int = None, AsPhotoImage=None):
        Assert(data, bytes)
        if formats:
            with BytesIO(data) as buf:
                with cls.open(buf, formats=formats) as img:
                    o = cls(img, width, height)
                    if AsPhotoImage is not None: return o.ToPhotoImage(master=AsPhotoImage, width=width, height=height)
                    return o.Raw

        else:
            with BytesIO(data) as buf:
                with cls.open(buf) as img:
                    o = cls(img, width, height)
                    if AsPhotoImage is not None: return o.ToPhotoImage(master=AsPhotoImage, width=width, height=height)
                    return o.Raw



    @staticmethod
    def Extensions() -> Tuple[str, ...]:
        init()
        return tuple(EXTENSION.keys())

    @staticmethod
    @overload
    def IsImage(path: str, *file_types: str) -> bool: ...
    @staticmethod
    @overload
    def IsImage(path: Path, *file_types: str) -> bool: ...
    @staticmethod
    @overload
    def IsImage(path: bytes, *file_types: str) -> bool: ...

    @staticmethod
    def IsImage(path: Union[str, Path, bytes], *file_types: str) -> bool:
        if isinstance(path, Path): path = path.Value

        if isinstance(path, str):
            if not file_types:
                if not EXTENSION: ImageObject.Extensions()
                file_types = tuple(EXTENSION.keys())

            if path.lower().endswith(file_types):
                try:
                    with open(path, 'rb') as f:
                        with ImageObject.open(f) as img:
                            img.verify()
                            return True
                except (IOError, SyntaxError): return False

        elif isinstance(path, bytes):
            try:
                with BytesIO(path) as buf:
                    with ImageObject.open(buf) as img:
                        img.verify()
                        return True
            except (IOError, SyntaxError): return False

        return False
