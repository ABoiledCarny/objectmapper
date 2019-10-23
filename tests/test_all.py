import pytest

import objectmapper

@pytest.fixture
def empty_mapper():
    return objectmapper.ObjectMapper()

@pytest.fixture
def int_to_str():
    def int_to_str(i: int) -> str:
        return str(i)
    return int_to_str

@pytest.fixture
def int_to_str_mapper(empty_mapper, int_to_str):
    empty_mapper.create_map(int, str, int_to_str)
    return empty_mapper

def test_mapping(int_to_str_mapper, int_to_str):
    assert int_to_str_mapper._mappings[int][str] is int_to_str

def test_duplicate_mapping_error(int_to_str_mapper, int_to_str):
    with pytest.raises(objectmapper.DuplicateMappingError):
        int_to_str_mapper.create_map(int, str, int_to_str)

def test_force_overwrite(int_to_str_mapper):
    def int_to_str(i: int) -> str:
        return 'odd' if i % 2 else 'even'
    int_to_str_mapper.create_map(int, str, int_to_str, force=True)
    assert int_to_str_mapper.map(42, str) == int_to_str(42)

def test_input_not_type(empty_mapper, int_to_str):
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(10, str, int_to_str)

def test_output_not_type(empty_mapper, int_to_str):
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(int, 'ten', int_to_str)

def test_not_callable(empty_mapper, int_to_str):
    with pytest.raises(objectmapper.MapTypeError):
        empty_mapper.create_map(int, str, None)

def test_map_input_key_error(empty_mapper):
    with pytest.raises(objectmapper.MapInputKeyError):
        empty_mapper.map(42, str)

def test_map_output_key_error(int_to_str_mapper):
    with pytest.raises(objectmapper.MapOutputKeyError):
        int_to_str_mapper.map(42, bool)
