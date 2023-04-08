from Pointer_Dict import PointerDict
import unittest
import copy

class PointerDict_Test(unittest.TestCase):
    # Each test always checks, whether original has been changed or not

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
    
    # Add value on empty dictionary
    def test_emptyAdd(self):
        tmp = PointerDict()
        tmp['first'] = 10
        self.assertDictEqual(dict(tmp), { 'first': 10 })
        self.assertDictEqual(tmp.origin, {})
    
    # Add value to existing not nested dictionary
    def test_Add(self):
        orig = { 'foo': 'bar', 'foobar': 1 }
        tmp = PointerDict(orig)
        
        tmp['first']=10
        dummy = copy.deepcopy(orig)
        dummy['first'] = 10
        self.assertDictEqual(dict(tmp), dummy)
        self.assertDictEqual(tmp.origin, orig)

    # Add value to existing nested dictionary
    def test_AddNested(self):
        orig = { 'foo': 'bar', 'foobar': { 'bar': 'foo' } }
        tmp = PointerDict(orig)
        
        tmp['foobar']['barfoo'] = 10
        dummy = copy.deepcopy(orig)
        dummy['foobar']['barfoo'] = 10
        for key in dummy.keys():
            if isinstance(dummy[key], dict):
                self.assertEqual(dict(tmp[key]), dummy[key])
            else:
                self.assertEqual(tmp[key], dummy[key])
        self.assertDictEqual(tmp.origin, orig)

    # Change value in existing not nested dictionary
    def test_Change(self):
        orig = { 'foo': 'bar', 'foobar': 1 }
        tmp = PointerDict(orig)
        
        tmp['foobar']=10
        dummy = copy.deepcopy(orig)
        dummy['foobar']=10
        self.assertDictEqual(dict(tmp), dummy)
        self.assertDictEqual(tmp.origin, orig)

    # Change value in existing nested dictionary
    def test_ChangeNested(self):
        orig = { 'foo': 'bar', 'foobar': { 'bar': 'foo' } }
        tmp = PointerDict(orig)
        
        tmp['foobar']['bar'] = 10
        dummy = copy.deepcopy(orig)
        dummy['foobar']['bar'] = 10
        self.assertDictEqual(dict(tmp), dummy)
        self.assertDictEqual(tmp.origin, orig)

    # Change value in existing not nested dictionary into directory
    def test_ChangeDirect(self):
        orig = { 'foo': 'bar', 'foobar': 1 }
        tmp = PointerDict(orig)
        
        tmp['foobar'] = { 'barbara': '', 'foofa': 1 }
        dummy = copy.deepcopy(orig)
        dummy['foobar'] = { 'barbara': '', 'foofa': 1 }
        for key in dummy.keys():
            if isinstance(dummy[key], dict):
                self.assertEqual(dict(tmp[key]), dummy[key])
            else:
                self.assertEqual(tmp[key], dummy[key])
        self.assertDictEqual(tmp.origin, orig)

    # Change value in existing nested dictionary into directory
    def test_ChangeNestedDirect(self):
        orig = { 'foo': 'bar', 'foobar': { 'bar': 'foo' } }
        tmp = PointerDict(orig)
        
        tmp['foobar']['bar'] = { 'barbara': '', 'foofa': 1 }
        dummy = copy.deepcopy(orig)
        dummy['foobar']['bar'] = { 'barbara': '', 'foofa': 1 }
        # It has to be checked so complicately, because each nested dictionary from PointerDict is also from type PointerDict
        # That means, casting dict() on anested dict() and checking for equality is useless
        # Due to an inner entry still being of type PointerDict, and not dict()
        # Has to check for equal values!
        for key in dummy.keys():
            if isinstance(dummy[key], dict):
                for key2, item in dummy[key].items():
                    if isinstance(item, dict):
                        self.assertEqual(dict(tmp[key][key2]), item)
                    else:
                        self.assertEqual(tmp[key][key2], item)
            else:
                self.assertEqual(tmp[key], dummy[key])
        self.assertDictEqual(tmp.origin, orig)

    # Gets the same value in non-nested directory
    def test_GetValue(self):
        orig = { 'foo': 'bar', 'foobar': 10 , 'bar': 'foo' }
        tmp = PointerDict(orig)
        for key in orig.keys():
            self.assertEqual(tmp[key], orig[key])

    # Gets the same value in nested directory
    def test_GetValueNested(self):
        orig = { 'foo': 'bar', 'foobar': { 'bar': 'foo' } }
        tmp = PointerDict(orig)

        self.assertEqual(tmp['foobar']['bar'], orig['foobar']['bar'])

    # Get value in changed nested directory
    def test_GetValueChangedDict(self):
        orig = { 'foo': 'bar', 'foobar': 1 }
        tmp = PointerDict(orig)
        
        tmp['foobar'] = { 'barbara': '', 'foofa': 1 }
        dummy = copy.deepcopy(orig)
        dummy['foobar'] = { 'barbara': '', 'foofa': 1 }
        self.assertDictEqual(dict(tmp['foobar']), dummy['foobar'])
        self.assertEqual(tmp.origin['foobar'], orig['foobar'])

    # Change value in existing nested dictionary into directory
    def test_GetValueChangedDictNested(self):
        orig = { 'foo': 'bar', 'foobar': { 'bar': 'foo' } }
        tmp = PointerDict(orig)
        
        tmp['foobar']['bar'] = { 'barbara': '', 'foofa': 1 }
        dummy = copy.deepcopy(orig)
        dummy['foobar']['bar'] = { 'barbara': '', 'foofa': 1 }
        # Simple nested dictionaries do not need the complicated way of testing like above, one time casting is enough
        # Casting and checking depends on depth of the nested dictionary
        for key in dummy['foobar'].keys():
            if isinstance(dummy['foobar'][key], dict):
                self.assertEqual(dict(tmp['foobar'][key]), dummy['foobar'][key])
            else:
                self.assertEqual(tmp['foobar'][key], dummy['foobar'][key])
        self.assertDictEqual(tmp.origin['foobar'], orig['foobar'])

if __name__ == '__main__':
    unittest.main()