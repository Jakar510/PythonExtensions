# --------------------------------------------------------------------------------------------------
#  Created by Tyler Stegmaier.
#  Property of TrueLogic Company.
#  Copyright (c) 2021.
# --------------------------------------------------------------------------------------------------

import json
import pickle
from typing import *

from cryptography.fernet import Fernet




__all__ = ['Encryptor']

# key = Fernet.generate_key()

class Encryptor(object):
    __slots__ = ['_path', '_encoding', '_private_key', '_encrypter']
    # _KEY_FILE_ = paths.PASS_KEY_FILE_NAME
    def __init__(self, path: str, *, private_key: bytes, encoding: str = "utf-8"):
        self._path = path
        self._encoding = encoding
        self._private_key = private_key
        self._encrypter = Fernet(self._private_key)


    def encode(self, s: str) -> bytes: return s.encode(self._encoding)
    def decode(self, s: bytes) -> str: return s.decode(self._encoding)


    @staticmethod
    def _from_json(s: Union[str, bytes, bytearray], **kwargs) -> Dict:
        try: return json.loads(s, **kwargs)
        except Exception:
            print('_____from__json_____', type(s), s, sep='\n\n', end='\n\n\n')
            raise
    @staticmethod
    def _to_json(s: Dict, **kwargs) -> str: return json.dumps(s, **kwargs)


    @staticmethod
    def _from_pickle(s: bytes) -> Dict: return pickle.loads(s)
    @staticmethod
    def _to_pickle(s: Dict) -> bytes: return pickle.dumps(s, protocol=pickle.HIGHEST_PROTOCOL)


    def _ReadFile(self) -> bytes:
        with open(self._path, 'rb') as f:
            return f.read()
    def _WriteFile(self, value: bytes):
        with open(self._path, 'wb') as f:
            return f.write(value)


    def DecryptFile(self) -> bytes: return self.Decode(self._ReadFile())
    def EncryptFile(self, value: bytes): return self._WriteFile(self.Encrypt(value))


    def ReadJson(self, **kwargs) -> Dict: return self._from_json(self._ReadFile(), **kwargs)
    def WriteJson(self, value: Dict, **kwargs): return self._WriteFile(self._to_json(value, **kwargs).encode())


    def ReadPickle(self) -> Dict: return self._from_pickle(self.DecryptFile())
    def WritePickle(self, value: Dict): return self.EncryptFile(self._to_pickle(value))



    def Encrypt(self, value: bytes) -> bytes: return self._encrypter.encrypt(value)
    def Decode(self, value: bytes = None) -> bytes: return self._encrypter.decrypt(value)



