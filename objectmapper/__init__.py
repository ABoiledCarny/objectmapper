# pylint: disable=missing-module-docstring

from typing import Any, Callable, Iterable, Optional, overload, Type, TypeVar

from .objectmapper import ObjectMapper, _InputType, _OutputType
from .exceptions import (
    DuplicateMappingError,
    MapTypeError,
    MapFunctionTypeError,
    MapKeyError,
    MapInputKeyError,
    MapOutputKeyError,
    ObjectMapperError,
)


__all__ = [
    'create_map',
    'DuplicateMappingError',
    'map',
    'MapTypeError',
    'MapFunctionTypeError',
    'MapKeyError',
    'MapInputKeyError',
    'MapOutputKeyError',
    'ObjectMapper',
    'ObjectMapperError',
]


_OBJECT_MAPPER = ObjectMapper()


@overload
def create_map(input_type: Type[_InputType],
               output_type: Type[_OutputType],
               map_function: None,
               force: bool) -> Callable[[Callable[[_InputType], _OutputType]],
                                        Callable[[_InputType], _OutputType]]:  # pragma: no cover
    '''Specialized form of `create_map` for a one-to-one mapping.

    If a map function is not provided, then it behaves as a decorator
    and returns the decorated function
    '''
    ...


@overload
def create_map(input_type: Type[_InputType],
               output_type: Type[_OutputType],
               map_function: Callable[[_InputType], _OutputType],
               force: bool) -> None:  # pragma: no cover
    '''Specialized form of `create_map` for a one-to-one mapping.

    If a map function is provided, then there are only side effects
    and nothing is returned.
    '''
    ...


@overload
def create_map(input_types: Iterable[type],
               output_type: Type[_OutputType],
               map_function: None,
               force: bool) -> Callable[[Callable[..., _OutputType]],
                                        Callable[..., _OutputType]]:  # pragma: no cover
    '''If a map function is provided, then there are only side effects and
    nothing is returned.
    '''
    ...


@overload
def create_map(input_types: Iterable[type],
               output_type: Type[_OutputType],
               map_function: Callable[..., _OutputType],
               force: bool) -> None:  # pragma: no cover
    '''If a map function is provided, then there are only side effects and
    nothing is returned.
    '''
    ...


def create_map(input_types, output_type, map_function=None, force=False):
    '''Stores a mapping (`map_function`) from objects of types
    `input_types` to an object of type `output_type`. If `force` is
    `True`, then any pre-existing mapping from `input_types` to
    `output_type` is overwritten.

    .. testsetup:: create_map_explicit

       import objectmapper

    .. doctest:: create_map_explicit

       >>> # One-to-one
       >>> objectmapper.create_map(int, str, lambda i: str(i))
       >>> objectmapper.map(42, str)
       '42'
       >>> # Many-to-one
       >>> objectmapper.create_map((int, float), str, lambda i, j: str(i + j))
       >>> objectmapper.map((25, 25.1), str)
       '50.1'

    .. testcleanup:: create_map_explicit

       import importlib
       importlib.reload(objectmapper)

    Can also be used as a _decorator_

    .. testsetup:: create_map_decorator

       import objectmapper

    .. doctest:: create_map_decorator

       >>> @objectmapper.create_map((int, float), str)
       ... def int_float_to_str(i: int, j: float) -> str:
       ...     return str(i + j)
       >>> objectmapper.map((25, 25.1), str)
       '50.1'

    .. testcleanup:: create_map_decorator

       import importlib
       importlib.reload(objectmapper)

    `MapTypeError` is raised if and of the `input_types` or
    `output_type` are not types

    `MapFunctionTypeError` is raised if `map_function` is not
    callable.

    `DuplicateMappingError` is raised if there is a pre-existing
    mapping from `input_types` to `output_type` and `force` is
    `False`.
    '''
    return _OBJECT_MAPPER.create_map(input_types, output_type, map_function, force)


@overload
def map(input_instance: Any, output_type: Type[_OutputType]) -> _OutputType:  # pragma: no cover pylint: disable=redefined-builtin
    '''Specialized form of `map` for retrieving one-to-one mappings.'''
    ...


@overload
def map(input_instances: Iterable[Any], output_type: Type[_OutputType]) -> _OutputType:  # pragma: no cover pylint: disable=redefined-builtin
    '''General form of `map` for retrieving many-to-one mappings.'''
    ...


def map(input_instances, output_type):  # pylint: disable=redefined-builtin
    '''Returns an object of type `output_type` by giving `*input_instances`
    to the mapping from `map(type, input_instances)` to `output_type`.

    .. testsetup:: map

       import objectmapper

    .. doctest:: map

       >>> import objectmapper
       >>> # One-to-one
       >>> @objectmapper.create_map(int, str)
       ... def longform_int_to_str(i: int) -> str:
       ...     digits = (str(x) for x in range(10))
       ...     words = ['zero', 'one', 'two', 'three', 'four',
       ...              'five', 'six', 'seven', 'eight', 'nine']
       ...     digit_to_word = {d: w for d, w in zip(digits, words)}
       ...     return ' '.join(digit_to_word[c] for c in str(i))
       >>> objectmapper.map(451, str)
       'four five one'
       >>> # Many-to-one
       >>> @objectmapper.create_map((int, int), str)
       ... def longform_int_int_to_str(i: int, j: int) -> str:
       ...     return ' '.join(map(longform_int_to_str, [i, j]))
       >>> objectmapper.map((451, 234), str)
       'four five one two three four'


    .. testcleanup:: map

       import importlib
       importlib.reload(objectmapper)


    Raises `MapInputKeyError` if there are no mappings from
    `map(type, input_instances)`.

    Raises `MapOutputKeyError` if there are no mappings from
    `map(type, input_instances)` to `output_type`.
    '''
    return _OBJECT_MAPPER.map(input_instances, output_type)
