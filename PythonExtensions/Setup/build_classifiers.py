import json
import re

from PythonExtensions.Setup import *
from PythonExtensions.debug import *




def Indent(level: int): return '    ' * level

num_start = re.compile(r'^\d+_')
ver_finder = re.compile(r'^\d+\.\d+$')

_num_words = {
    '0': 'Zero',
    '1': 'One',
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    '10': 'Ten',
    '11': 'Eleven',
    }

def GetClass(name: str, _indent: int = 0): return f'{Indent(_indent)}class {name}(object):'

class Name(object):
    class Name(object):
        class Name(object):
            pass

classes = { }

def Remove(_line: str, *args: str):
    for arg in args:
        _line = _line.replace(arg, '')

    return _line
def Replace(_line: str, kwargs: Dict[str, str]):
    for old, new in kwargs.items():
        _line = _line.replace(old, new)

    return _line

def GetData(_line: str, *, sep=' :: ') -> List[str]:
    results = []
    for l in _line.split(sep):
        # l = l.replace(' - ', '_').replace(' ', '_').replace('\\', '_').replace(r'/', '_')
        # l = l.replace('\n', '').replace('-', '').replace("'", '')
        l = Replace(l, {
            ' - ': '_',
            '\\': '_',
            '/': '_',
            ' ': '_',
            '.': '_',
            '+': '_plus',
            '#': '_sharp',
            '3D': 'ThreeDimension',
            })
        l = Remove(l, '\n', '(', ')', "'", '-', ',')

        l = num_start.sub('', l)
        v = ver_finder.match(l)
        if v is not None:
            l = 'Version_' + v.group(0).replace('.', '_')

        if l in _num_words:
            l = _num_words[l]

        results.append(l)

    return results
def HandleData(_value: str, _end: str, d: Dict, _data: List[str]):
    try:
        if len(_data) == 0:
            d[_end] = _value
            return

        item = _data[0]
        if item not in d:
            d[item] = { }

        d = d[item]

        return HandleData(_value, _end, d, _data[1:])
    except:
        PrettyPrint('', _value=_value, _end=_end, _data=_data)
        raise


# {'min': 2, 'max': 5}
for line in ReadLinesFromFile(os.path.abspath('./classifiers.txt')):
    data = GetData(line)
    # print(data)

    value = data[-1]

    HandleData(line.replace('\n', ''), value, classes, data)

with open(os.path.abspath('./Classifiers.json'), 'w', newline='\n') as f:
    json.dump(classes, f, indent=4)


def WriteData(_f, _key: str, d: Union[Dict, str], _indent: int):
    for _cls, _data in d.items():
        if isinstance(_data, str):
            _data = _data.replace("\n", "")
            _f.write(f'{Indent(_indent)}{_cls} = "{_data}" \n')

        elif len(_data) == 1:
            for k, v in _data.items():
                v = v.replace("\n", "")
                _f.write(f'{Indent(_indent)}{k} = "{v}" \n')

        else:
            _f.write(GetClass(_cls, _indent))
            _f.write('\n')
            WriteData(_f, _cls, _data, _indent + 1)

with open(os.path.abspath('./Classifiers.py'), 'w') as f:
    for cls, data in classes.items():
        indent = 0
        f.write(GetClass(cls, indent))
        f.write('\n')
        WriteData(f, cls, data, _indent=1)
