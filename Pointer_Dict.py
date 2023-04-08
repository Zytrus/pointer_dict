from typing import Union, Any
from collections import UserDict, KeysView

class PointerDict(UserDict):

    def __init__(self, /, mapping: dict = None):
        super().__init__()
        # Contains the original data which will not be modified
        self.origin: dict = mapping or {}
        # Tracks the deleted keys since the original data won't be modified
        self.deleted: set = set()

    def __getitem__(self, key: Union[str, int]) -> Any:
        # Since original data won't be modified, we neeed to check if the key is deleted first
        if key in self.deleted:
            raise KeyError(key)
        elif key in self.data:
            return self.data[key]
        else:
            # Key is maybe in original data
            item = self.origin[key]
            if isinstance(item, dict):
                item = PointerDict(item)
                self[key] = item
            return item

    def __setitem__(self, key: Union[str, int], value: Any):
        if isinstance(value, dict):
            value = PointerDict(value)
        self.data[key] = value
        self.deleted.discard(key)

    def __delitem__(self, key: Union[str, int]):
        if key in self.data:
            del self.data[key]
            self.deleted.add(key)
        elif key in self.origin:
            self.deleted.add(key)
        else:
            raise KeyError(key)
        
    def keys(self) -> KeysView[Union[str, int]]:
        all_keys = set()
        for m_key in super().keys():
            all_keys.add(m_key)
        for o_key in self.origin.keys():
            all_keys.add(o_key)
        for d_key in self.deleted:
            all_keys.discard(d_key)

        return all_keys

    def __contains__(self, key: Union[str, int]) -> bool:
        return key not in self.deleted and (key in self.data.keys() or key in self.origin.keys())
    
    def __repr__(self) -> str:
        pointer = {}
        for key in self.keys():
            pointer[key] = self.__getitem__(key)
        return str(pointer)
    