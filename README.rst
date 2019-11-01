objectmapper
============

A small module for mapping between object types.

* `Documentation <https://objectmapper.readthedocs.io/en/latest/>`_
* `Source <https://github.com/ABoiledCarny/objectmapper>`_
* `PyPi Package <https://pypi.org/project/objectmapper/>`_

Installation
------------
``objectmapper`` requires ``Python >= 3.6`` because it relies on modern type annotations.
::

   pip install objectmapper

Example
-------

>>> import objectmapper
>>> mapper = objectmapper.ObjectMapper()
>>> # One-to-one mappings
>>> def int_to_str(i: int) -> str:
...     return str(i)
>>> mapper.create_map(int, str, int_to_str)
>>> mapper.map(42, str)
'42'
>>> # Many-to-one mappings
>>> def int_float_to_str(i: int, f: float) -> str:
...     return str(i + f)
>>> mapper.create_map((int, float), str, int_float_to_str)
>>> mapper.map((42, 42.5), str)
'84.5'
