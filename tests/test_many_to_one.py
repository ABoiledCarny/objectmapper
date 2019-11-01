# pylint: disable=redefined-outer-name
'''Many-to-one mapping tests'''
import pytest

import objectmapper
from fixtures import empty_module, empty_mapper  # pylint: disable=unused-import


@pytest.fixture
def int_float_to_str():
    '''Returns a function that converts an integer to a string.'''
    def int_float_to_str(integer: int, floater: float) -> str:
        return str(integer + floater)
    return int_float_to_str


@pytest.fixture
def int_float_to_str_mapper(empty_mapper, int_float_to_str):
    '''Returns an ObjectMapper with an imperative mapping from int to
    str.
    '''
    empty_mapper.create_map((int, float), str, int_float_to_str)
    return empty_mapper


@pytest.fixture
def int_float_to_str_mapper_decorated(empty_mapper, int_float_to_str):
    '''Returns an ObjectMapper with a decorated mapping from int to
    str.
    '''
    empty_mapper.create_map((int, float), str)(int_float_to_str)
    return empty_mapper


@pytest.fixture
def int_float_to_str_module(empty_module, int_float_to_str):
    '''Returns an instance of the objectmapper module with an imperative
    mapping from int to str.
    '''
    empty_module.create_map((int, float), str, int_float_to_str)
    return empty_module


@pytest.fixture
def int_float_to_str_module_decorated(empty_module, int_float_to_str):
    '''Returns an instance of the objectmapper module with a decorated
    mapping from int to str.
    '''
    empty_module.create_map((int, float), str)(int_float_to_str)
    return empty_module


def test_mapper_create_map_output(empty_mapper, int_float_to_str):
    '''Test that the objectmapper's create_map returns nothing when not
    used as a decorator.
    '''
    assert empty_mapper.create_map((int, float), str, int_float_to_str) is None


def test_mapper_create_map_decorator_output(empty_mapper, int_float_to_str):
    '''Test that the objectmapper's create_map returns the map function
    when used as a decorator.
    '''
    assert empty_mapper.create_map(int, str)(int_float_to_str) is int_float_to_str


def test_module_create_map_output(empty_module, int_float_to_str):
    '''Test that the module's create_map returns nothing when not used as
    a decorator.
    '''
    assert empty_module.create_map(int, str, int_float_to_str) is None


def test_module_create_map_decorator_output(empty_module, int_float_to_str):
    '''Test that the module's create_map returns the map function when
    used as a decorator.
    '''
    assert empty_module.create_map(int, str)(int_float_to_str) is int_float_to_str


def test_mapper_map_output(int_float_to_str_mapper, int_float_to_str):
    '''Test imperative object mapping matches raw function output.'''
    integer = 42
    floater = 42.5
    assert int_float_to_str_mapper.map((integer, floater), str) == int_float_to_str(integer, floater)


def test_mapper_map_decorated_output(int_float_to_str_mapper_decorated, int_float_to_str):
    '''Test decorated object mapping matches raw function output.'''
    integer = 42
    floater = 42.5
    assert int_float_to_str_mapper_decorated.map((integer, floater), str) == int_float_to_str(integer, floater)


def test_module_output(int_float_to_str_module, int_float_to_str):
    '''Test imperative module mapping matches raw function output.'''
    integer = 42
    floater = 42.5
    assert int_float_to_str_module.map((integer, floater), str) == int_float_to_str(integer, floater)


def test_module_decorated_output(int_float_to_str_module_decorated, int_float_to_str):
    '''Test decorated module mapping matches raw funtion output.'''
    integer = 42
    floater = 42.5
    assert int_float_to_str_module_decorated.map((integer, floater), str) == int_float_to_str(integer, floater)


def test_duplicate_mapping_error(int_float_to_str_mapper, int_float_to_str):
    '''Test mapping defined twice without overwrite.'''
    with pytest.raises(objectmapper.DuplicateMappingError):
        int_float_to_str_mapper.create_map((int, float), str, int_float_to_str)


def test_force_overwrite(int_float_to_str_mapper):
    '''Test mapping defined twice with overwrite.'''
    def int_float_to_str(integer: int, floater: float) -> str:
        return str(integer - floater)
    int_float_to_str_mapper.create_map((int, float), str, int_float_to_str, force=True)
    integer = 42
    floater = 42.5
    assert int_float_to_str_mapper.map((integer, floater), str) == int_float_to_str(integer, floater)


def test_input_not_type(empty_mapper, int_float_to_str):
    '''Test invalid input type.'''
    bad_input = (10, float)
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(bad_input, str, int_float_to_str)


def test_output_not_type(empty_mapper, int_float_to_str):
    '''Test invalid output type.'''
    bad_output = 'sum of args'
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map((int, float), bad_output, int_float_to_str)


def test_not_callable(empty_mapper):
    '''Test invalid map function type.'''
    bad_function = 42
    with pytest.raises(objectmapper.MapFunctionTypeError):
        empty_mapper.create_map((int, float), str, bad_function)


def test_map_input_key_error(empty_mapper):
    '''Test missing input type.'''
    missing_input = (42, 42.5)
    with pytest.raises(objectmapper.MapInputKeyError):
        empty_mapper.map(missing_input, str)


def test_map_output_key_error(int_float_to_str_mapper):
    '''Test missing output type.'''
    missing_output = bool
    with pytest.raises(objectmapper.MapOutputKeyError):
        int_float_to_str_mapper.map((42, 42.5), missing_output)
