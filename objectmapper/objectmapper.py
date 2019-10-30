'''ObjectMapper Class'''

from typing import Any, Callable, Optional, Type, TypeVar

from . import exceptions


_InputType = TypeVar('_InputType')
_OutputType = TypeVar('_OutputType')


class ObjectMapper:
    '''Class for recording and accessing mappings between object
    types. This will often be a singleton in user code.

    '''
    def __init__(self) -> None:
        self._mappings = dict()

    def create_map(self,  # pylint: disable=invalid-name
                   InputType: Type[_InputType],
                   OutputType: Type[_OutputType],
                   map_function: Optional[Callable[[_InputType], _OutputType]] = None,
                   force: bool = False) \
                   -> Optional[Callable[[Callable[[_InputType], _OutputType]], None]]:
        '''Stores a localized mapping between types. See `create_map`'''
        for map_type in [InputType, OutputType]:
            if not isinstance(map_type, type):
                raise exceptions.MapTypeError(map_type)

        def set_map_function(map_function: Callable[[_InputType], _OutputType]) -> None:
            if not callable(map_function):
                raise exceptions.MapFunctionTypeError(map_function)

            self._mappings.setdefault(InputType, dict())

            if not force:
                mapping = self._mappings[InputType].get(OutputType, None)
                if mapping:
                    raise exceptions.DuplicateMappingError(InputType, OutputType, mapping)
            self._mappings[InputType][OutputType] = map_function

        if map_function is None:
            return set_map_function
        return set_map_function(map_function)

    def map(self, input_instance: Any, OutputType: Type[_OutputType]) -> _OutputType:  # pylint: disable=invalid-name
        '''Converts `input_instance` using a mapping from
        `type(input_instance)` to `OutputType`. See `map`.

        '''
        InputType = type(input_instance)  # pylint: disable=invalid-name
        if InputType not in self._mappings:
            raise exceptions.MapInputKeyError(InputType)

        map_function = self._mappings[InputType].get(OutputType, None)
        if not map_function:
            raise exceptions.MapOutputKeyError(InputType, OutputType)

        return map_function(input_instance)
