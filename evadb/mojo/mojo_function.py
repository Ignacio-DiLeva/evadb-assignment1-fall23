from evadb.functions.abstract.abstract_function import AbstractFunction
from evadb.functions.mojo import FunctionManifest

import pandas as pd

class MojoFunction(AbstractFunction):
    def __init__(self, name: str, manifest: FunctionManifest, mojoController) -> None:
        if manifest._name != name:
            raise Exception(f"Function name in manifest({manifest._name}) does not match function name ({name})")
        self.name = name
        self.manifest = manifest
        self.mojoController = mojoController
        super().__init__()

    def setup(self, *args, **kwargs) -> None:
        self.mojoController.setup(self.name)

    def forward(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.mojoController.forward(self.name, df)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MojoFunction):
            return False
        return self.name == o.name and self.manifest == o.manifest and self.mojoController == o.mojoController

    def __hash__(self) -> int:
        return hash((self.name, self.manifest, self.mojoController))

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
