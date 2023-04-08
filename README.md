A class that subclasses from Userdict. It is supposed to save memory by shallow copying another dictionary, whilst also being able to have its own values.

The dictionary works like this:

```py
original = { 'foo': 1, 'bar': 2, 'foobar': 3 }
pointer_dict = PointerDict(original)

pointer_dict['foo'] = 10

print(original) # Should result in { 'foo': 1, 'bar': 2, 'foobar': 3 }
print(pointer_dict) # Should result in { 'foo': 10, 'bar': 2, 'foobar': 3 }
```

The original values are left untouched, but additional values or changed values are saved in the PointerDict class.
This approach is amde to save memory, when dealing with several variations of the same class.
A shallow copy would change the original values as well, this behaviour is unwanted.
A deepcopy needs to allocate new memory, there the PointerDict is somewhat a mixture of both.
Whilst being able to access the new values in its own class, it points towards the original values, when they were not changed.
(Therefore the name 'PointerDict')