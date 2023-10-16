from typing import List, TypeVar

from evadb.catalog.catalog_type import Dimension, NdArrayType
from evadb.functions.decorators.io_descriptors.data_types import PandasDataframe as RealPandasDataframe

PandasDataframe = TypeVar("PandasDataframe")

class PandasDataframe:
    def __init__(self):
        self._columns: List[str] = None
        self._column_types: List[NdArrayType] = []
        self._column_shapes: List[Dimension] = []
    
    def columns(self, v: List[str]) -> PandasDataframe:
        self._columns = v
        return self

    def column_types(self, v: List[NdArrayType]) -> PandasDataframe:
        self._column_types = v
        return self
    
    def column_shapes(self, v: List[Dimension]) -> PandasDataframe:
        self._column_shapes = v
        return self

    def realize(self) -> RealPandasDataframe:
        return RealPandasDataframe(self._columns, self._column_types, self._column_shapes)

    def __str__(self) -> str:
        return f"PandasDataframe(columns={self._columns}, column_types={self._column_types}, column_shapes={self._column_shapes})"
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, PandasDataframe):
            return False
        return self._columns == o._columns and self._column_types == o._column_types and self._column_shapes == o._column_shapes

    def __hash__(self) -> int:
        return len(self._columns)
