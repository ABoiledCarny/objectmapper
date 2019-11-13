# pylint: disable=redefined-outer-name
'''One-to-one mapping tests'''
import pytest

import objectmapper
from fixtures import empty_module, empty_mapper  # pylint: disable=unused-import


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
def int_to_str_module(empty_module, int_to_str):
    '''Returns an instance of the objectmapper module with an imperative
    mapping from int to str.
    '''
    empty_module.create_map(int, str, int_to_str)
    return empty_module


@pytest.fixture
def int_to_str_module_decorated(empty_module, int_to_str):
    '''Returns an instance of the objectmapper module with a decorated
    mapping from int to str.
    '''
    empty_module.create_map(int, str)(int_to_str)
    return empty_module


def test_mapper_create_map_output(empty_mapper, int_to_str):
    '''Test that the objectmapper's create_map returns nothing when not
    used as a decorator.
    '''
    assert empty_mapper.create_map(int, str, int_to_str) is None


def test_mapper_create_map_decorator_output(empty_mapper, int_to_str):
    '''Test that the objectmapper's create_map returns the map function
    when used as a decorator.
    '''
    assert empty_mapper.create_map(int, str)(int_to_str) is int_to_str


def test_module_create_map_output(empty_module, int_to_str):
    '''Test that the module's create_map returns nothing when not used as
    a decorator.
    '''
    assert empty_module.create_map(int, str, int_to_str) is None


def test_module_create_map_decorator_output(empty_module, int_to_str):
    '''Test that the module's create_map returns the map function when
    used as a decorator.
    '''
    assert empty_module.create_map(int, str)(int_to_str) is int_to_str


def test_mapper_map_output(int_to_str_mapper, int_to_str):
    '''Test imperative object mapping matches raw function output.'''
    integer = 42
    assert int_to_str_mapper.map(integer, str) == int_to_str(integer)


def test_mapper_map_decorated_output(int_to_str_mapper_decorated, int_to_str):
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
    integer = 42
    assert int_to_str_mapper.map(integer, str) == int_to_str(integer)


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
