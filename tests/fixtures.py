'''Fixtures that are shared among tests'''
import importlib

import pytest

import objectmapper

@pytest.fixture
def empty_module():
    '''Returns a like-new instance of the objectmapper module.'''
    import objectmapper as objmap # pylint: disable=reimported, import-outside-toplevel
    importlib.reload(objmap)
    return objmap

@pytest.fixture
def empty_mapper():
    '''Returns a new ObjectMapper.'''
    return objectmapper.ObjectMapper()
