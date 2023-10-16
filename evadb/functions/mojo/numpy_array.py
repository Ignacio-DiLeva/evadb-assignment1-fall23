from typing import Tuple, TypeVar

from evadb.catalog.catalog_type import NdArrayType
from evadb.functions.decorators.io_descriptors.data_types import NumpyArray as RealNumpyArray

NumpyArray = TypeVar("NumpyArray")

class NumpyArray:
    def __init__(self):
        self._name: str = ""
        self._is_nullable: bool = False
        self._array_type: NdArrayType = None
        self._dimensions = Tuple[int] = None
    
    def name(self, v: str) -> NumpyArray:
        self._name = v
        return self

    def is_nullable(self, v: bool) -> NumpyArray:
        self._is_nullable = v
        return self
    
    def type(self, v: NdArrayType) -> NumpyArray:
        self._array_type = v
        return self

    def dimensions(self, v: Tuple[int]) -> NumpyArray:
        self._dimensions = v
        return self

    def realize(self) -> RealNumpyArray:
        return RealNumpyArray(self._name, is_nullable=self._is_nullable, type=self._array_type, dimensions=self._dimensions)

    def __str__(self) -> str:
        return f"NumpyArray(name={self._name}, is_nullable={self._is_nullable}, type={self._array_type}, dimensions={self._dimensions})"
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, NumpyArray):
            return False
        return self._name == o._name and self._is_nullable == o._is_nullable and self.__type == o._array_type and self._dimensions == o._dimensions

    def __hash__(self) -> int:
        return hash((self._name, self._is_nullable, self._array_type, self._dimensions))
