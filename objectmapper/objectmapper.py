'''ObjectMapper Class'''

from typing import Any, Callable, Dict, Iterable, overload, Tuple, Type, TypeVar

from . import exceptions


_InputType = TypeVar('_InputType')
_OutputType = TypeVar('_OutputType')


def _make_tuple(non_tuple: Any) -> Tuple[Any, ...]:
    try:
        result = tuple(non_tuple)
    except TypeError:
        result = (non_tuple,)
    return result


class ObjectMapper:
    '''Class for recording and accessing mappings between object
    types. This will often be a singleton in user code.

    '''
    def __init__(self) -> None:
        self._mappings: Dict[Tuple[type, ...], Dict[type, Callable[..., _OutputType]]] = dict()

    @overload
    def create_map(self,  # pylint: disable=no-self-use;
                   input_type: Type[_InputType],
                   output_type: Type[_OutputType],
                   map_function: None,
                   force: bool) -> Callable[[Callable[[_InputType], _OutputType]],
                                            Callable[[_InputType], _OutputType]]:  # pragma: no cover
        '''Stores a localized mapping between types. See `create_map`'''
        ...

    @overload
    def create_map(self,  # pylint: disable=no-self-use
                   input_type: Type[_InputType],
                   output_type: Type[_OutputType],
                   map_function: Callable[[_InputType], _OutputType],
                   force: bool) -> None: # pragma: no cover
        '''Stores a localized mapping between types. See `create_map`'''
        ...

    @overload
    def create_map(self,  # pylint: disable=no-self-use
                   input_types: Iterable[type],
                   output_type: Type[_OutputType],
                   map_function: None,
                   force: bool) -> Callable[[Callable[..., _OutputType]],
                                            Callable[..., _OutputType]]:  # pragma: no cover
        '''Stores a localized mapping between types. See `create_map`'''
        ...

    @overload
    def create_map(self,  # pylint: disable=no-self-use
                   input_types: Iterable[type],
                   output_type: Type[_OutputType],
                   map_function: Callable[..., _OutputType],
                   force: bool) -> None:  # pragma: no cover
        '''Stores a localized mapping between types. See `create_map`'''
        ...

    def create_map(self, input_types, output_type, map_function=None, force=False):
        '''Stores a localized mapping between types. See `create_map`.'''
        input_types = _make_tuple(input_types)

        for map_type in input_types + (output_type,):
            if not isinstance(map_type, type):
                raise exceptions.MapTypeError(map_type)

        def set_map_function(map_function: Callable[..., _OutputType]) -> Callable[..., _OutputType]:
            if not callable(map_function):
                raise exceptions.MapFunctionTypeError(map_function)

            self._mappings.setdefault(input_types, dict())

            if not force:
                mapping = self._mappings[input_types].get(output_type, None)
                if mapping:
                    raise exceptions.DuplicateMappingError(input_types, output_type, mapping)
            self._mappings[input_types][output_type] = map_function
            return map_function

        if map_function is None:
            return set_map_function
        set_map_function(map_function)

    @overload
    def map(self, input_instance: Any, output_type: Type[_OutputType]) -> _OutputType:  # pylint: disable=no-self-use; # pragma: no cover
        '''Specialized form of `map` for retrieving one-to-one mappings.'''
        ...

    @overload
    def map(self, input_instances: Iterable[Any], output_type: Type[_OutputType]) -> _OutputType:  # pylint: disable=no-self-use; # pragma: no cover
        '''General form of `map` for retrieving one-to-one mappings.'''
        ...

    def map(self, input_instances, output_type):
        '''Converts `input_instances` using a mapping from `map(type,
        input_instances)` to `output_type`. See `map`.

        '''
        input_instances = _make_tuple(input_instances)
        input_types = tuple(map(type, input_instances))
        if input_types not in self._mappings:
            raise exceptions.MapInputKeyError(input_types)

        map_function = self._mappings[input_types].get(output_type, None)
        if not map_function:
            raise exceptions.MapOutputKeyError(input_types, output_type)

        return map_function(*input_instances)
