# pyre-strict
"""
WDL values instantiated at runtime

Each value is represented by an instance of a Python class inheriting from
``WDL.Value.Base``.
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar
import WDL.Type as T
import json

BaseT = TypeVar('BaseT', bound='Base')
class Base(ABC):
    """The abstract base class for WDL values"""

    type : T.Base
    """WDL Type of this value"""

    value : Any # pyre-ignore
    """The "raw" Python value"""

    def __init__(self, type : T.Base, value : Any) -> None:
        assert isinstance(type, T.Base)
        self.type = type
        self.value = value

    def __eq__(self, other) -> bool:
        return (self.type == other.type and self.value == other.value)

    def __str__(self) -> str:
        return str(self.value)

    def coerce(self, desired_type : Optional[T.Base] = None) -> BaseT:
        """
        Coerce the value to the desired type and return it

        The result is undefined if the coercion is not valid. Types should be
        checked statically on ``WDL.Expr`` prior to evaluation.
        """
        assert desired_type is None or self.type == desired_type
        return self
    def expect(self, desired_type : Optional[T.Base] = None) -> BaseT:
        """Same as coerce"""
        return self.coerce(desired_type)

class Boolean(Base):
    """``value`` has Python type ``bool``"""
    def __init__(self, value : bool) -> None:
        super().__init__(T.Boolean(), value)
    def __str__(self) -> str:
        return str(self.value).lower()

class Float(Base):
    """``value`` has Python type ``float``"""
    def __init__(self, value : float) -> None:
        super().__init__(T.Float(), value)

class Int(Base):
    """``value`` has Python type ``int``"""
    def __init__(self, value : int) -> None:
        super().__init__(T.Int(), value)
    def coerce(self, desired_type : Optional[T.Base] = None) -> Base:
        if desired_type is not None and isinstance(desired_type, T.Float):
            return Float(float(self.value)) # pyre-ignore
        return super().coerce(desired_type)

class String(Base):
    """``value`` has Python type ``str``"""
    def __init__(self, value : str) -> None:
        super().__init__(T.String(), value)
    def __str__(self) -> str:
        return json.dumps(self.value)

class Array(Base):
    """``value`` is a Python ``list`` of other ``WDL.Value`` instances"""
    value : List[Any] = []
    def __init__(self, type : T.Array, value : List[Any]) -> None:
        super().__init__(type, value)
    def __str__(self) -> str:
        return "[" + ", ".join([str(item) for item in self.value]) + "]"
