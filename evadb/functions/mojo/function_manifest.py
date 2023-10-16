from abc import ABC
from typing import List, TypeVar, Union

from evadb.catalog.models.function_io_catalog import FunctionIOCatalogEntry

from .numpy_array import NumpyArray
from .pandas_dataframe import PandasDataframe
from .pytorch_tensor import PyTorchTensor

FunctionManifest = TypeVar("FunctionManifest")

class FunctionManifest(ABC):
    def __init__(self) -> None:
        self._name: str = ""
        self._cacheable: bool = False
        self._function_type: str = ""
        self._batchable: bool = True
        self._input_signatures: List[Union[NumpyArray,PandasDataframe,PyTorchTensor]] = None
        self._output_signatures: List[Union[NumpyArray,PandasDataframe,PyTorchTensor]] = None

    def name(self, v: str) -> FunctionManifest:
        self._name = v
        return self

    def cacheable(self, v: bool) -> FunctionManifest:
        self._cacheable = v
        return self
    
    def function_type(self, v: str) -> FunctionManifest:
        self._function_type = v
        return self

    def batchable(self, v: bool) -> FunctionManifest:
        self._batchable = v
        return self

    def input_signatures(self, v: List[Union[NumpyArray,PandasDataframe,PyTorchTensor]]) -> FunctionManifest:
        self._input_signatures = v
        return self

    def output_signatures(self, v: List[Union[NumpyArray,PandasDataframe,PyTorchTensor]]) -> FunctionManifest:
        self._output_signatures = v
        return self

    def get_input_io_list(self) -> List[FunctionIOCatalogEntry]:
        io_list = []
        if self._input_signatures is not None:
            for i in self._input_signatures:
                io_list.extend(i.realize().generate_catalog_entries(is_input=True))
        return io_list

    def get_output_io_list(self) -> List[FunctionIOCatalogEntry]:
        io_list = []
        if self._output_signatures is not None:
            for o in self._output_signatures:
                io_list.extend(o.realize().generate_catalog_entries(is_input=False))
        return io_list

    def __str__(self) -> str:
        return f"FunctionManifest(name={self._name}, cacheable={self._cacheable}, function_type={self._function_type}, batchable={self._batchable}, input_signatures={self._input_signatures}, output_signatures={self._output_signatures})"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, o: object) -> bool:
        if not isinstance(o, FunctionManifest):
            return False
        return self._cacheable == o._cacheable and self._function_type == o._function_type and self._batchable == o._batchable and self._input_signatures == o._input_signatures and self._output_signatures == o._output_signatures

    def __hash__(self) -> int:
        return hash((self._name, self._cacheable, self._function_type, self._batchable))
