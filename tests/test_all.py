# pylint: disable=redefined-outer-name
'''All unit tests'''
import importlib

import pytest

import objectmapper

@pytest.fixture
def objectmapper_module():
    '''Returns a like-new instance of the objectmapper module.'''
    import objectmapper as objmap # pylint: disable=reimported, import-outside-toplevel
    importlib.reload(objmap)
    return objmap

@pytest.fixture
def empty_mapper():
    '''Returns a new ObjectMapper.'''
    return objectmapper.ObjectMapper()

@pytest.fixture
def int_to_str():
    '''Returns a function that converts an integer to a string.'''
    def int_to_str(i: int) -> str:
        return str(i)
    return int_to_str

@pytest.fixture
def int_to_str_mapper(empty_mapper, int_to_str):
    '''Returns an ObjectMapper with an imperative mapping from int to
    str.
    '''
    empty_mapper.create_map(int, str, int_to_str)
    return empty_mapper

@pytest.fixture
def int_to_str_mapper_decorated(empty_mapper, int_to_str):
    '''Returns an ObjectMapper with a decorated mapping from int to
    str.
    '''
    empty_mapper.create_map(int, str)(int_to_str)
    return empty_mapper

@pytest.fixture
def int_to_str_module(objectmapper_module, int_to_str):
    '''Returns an instance of the objectmapper module with an imperative
    mapping from int to str.
    '''
    objectmapper_module.create_map(int, str, int_to_str)
    return objectmapper_module

@pytest.fixture
def int_to_str_module_decorated(objectmapper_module, int_to_str):
    '''Returns an instance of the objectmapper module with a decorated
    mapping from int to str.
    '''
    objectmapper_module.create_map(int, str)(int_to_str)
    return objectmapper_module

def test_mapper_output(int_to_str_mapper, int_to_str):
    '''Test imperative object mapping matches raw function output.'''
    integer = 42
    assert int_to_str_mapper.map(integer, str) == int_to_str(integer)

def test_mapper_decorated_output(int_to_str_mapper_decorated, int_to_str):
    '''Test decorated object mapping matches raw function output.'''
    integer = 42
    assert int_to_str_mapper_decorated.map(integer, str) == int_to_str(integer)

def test_module_output(int_to_str_module, int_to_str):
    '''Test imperative module mapping matches raw function output.'''
    integer = 42
    assert int_to_str_module.map(integer, str) == int_to_str(integer)

def test_module_decorated_output(int_to_str_module_decorated, int_to_str):
    '''Test decorated module mapping matches raw funtion output.'''
    integer = 42
    assert int_to_str_module_decorated.map(integer, str) == int_to_str(integer)

def test_duplicate_mapping_error(int_to_str_mapper, int_to_str):
    '''Test mapping defined twice without overwrite.'''
    with pytest.raises(objectmapper.DuplicateMappingError):
        int_to_str_mapper.create_map(int, str, int_to_str)

def test_force_overwrite(int_to_str_mapper):
    '''Test mapping defined twice with overwrite.'''
    def int_to_str(i: int) -> str:
        return 'odd' if i % 2 else 'even'
    int_to_str_mapper.create_map(int, str, int_to_str, force=True)
    assert int_to_str_mapper.map(42, str) == int_to_str(42)

def test_input_not_type(empty_mapper, int_to_str):
    '''Test invalid input type.'''
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(10, str, int_to_str)

def test_output_not_type(empty_mapper, int_to_str):
    '''Test invalid output type.'''
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(int, 'ten', int_to_str)

def test_not_callable(empty_mapper):
    '''Test invalid map function type.'''
    with pytest.raises(objectmapper.MapFunctionTypeError):
        empty_mapper.create_map(int, str, 42)

def test_map_input_key_error(empty_mapper):
    '''Test missing input type.'''
    with pytest.raises(objectmapper.MapInputKeyError):
        empty_mapper.map(42, str)

def test_map_output_key_error(int_to_str_mapper):
    '''Test missing output type.'''
    with pytest.raises(objectmapper.MapOutputKeyError):
        int_to_str_mapper.map(42, bool)
