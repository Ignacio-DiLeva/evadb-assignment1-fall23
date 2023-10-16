
from typing import TypeVar

from subprocess import PIPE, Popen, STDOUT
from find_libpython import find_libpython
import atexit
import os
import pandas as pd
import pickle
import tempfile
import shutil

from .mojo_function import MojoFunction

MojoController = TypeVar("MojoController")

class MojoController:

    instances = {}

    @staticmethod
    def get_mojo_controller(processName: str) -> MojoController:
        controller = MojoController.instances.get(processName, None)
        if controller is None:
            controller = MojoController(processName)
            atexit.register(lambda: controller.finish())
            MojoController.instances[processName] = controller
        return controller

    def __init__(self, processName: str) -> None:
        self.ready = False
        self.closed = False
        self.processName = processName
        self.folder = None
        self.process = None
        self.funcManifests = {}
        self.funcs = {}

    def ensureReady(self) -> None:
        self.checkOpen()
        if not self.ready:
            try:
                self.folder = tempfile.mkdtemp()
                os.mkdir(self.folder + "/manifests")
                mojoEnv = os.environ.copy()
                mojoEnv["MOJO_PYTHON_LIBRARY"] = find_libpython()
                self.process = Popen([self.processName, self.folder], env=mojoEnv, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
                response = self.process.stdout.readline().decode('utf-8').strip()
                if response != "Ready":
                    raise Exception(f"Unexpected response from Mojo process during MojoController startup: {response}")
                for fname in os.listdir(self.folder + "/manifests"):
                    with open(self.folder + "/manifests/" + fname, "rb") as f:
                        self.funcManifests[fname] = pickle.load(f)
                self.ready = True
            finally:
                if not self.ready:
                    if self.folder is not None:
                        shutil.rmtree(self.folder, ignore_errors=True)
                        self.folder = None
                    if self.process is not None:
                        self.process.kill()
                        self.process = None
    
    def setup(self, funcName: str) -> None:
        self.ensureReady()
        self.process.stdin.write(f"setup:{funcName}\n".encode('utf-8'))
        self.process.stdin.flush()
        response = self.process.stdout.readline().decode('utf-8').strip()
        if response != "Done":
            raise Exception(f"Unexpected response from Mojo process during setup for {funcName}: {response}")

    def forward(self, funcName: str, v: pd.DataFrame) -> pd.DataFrame:
        self.ensureReady()
        with open(self.folder + "/infile", "wb") as f:
            pickle.dump(v, f)
        self.process.stdin.write(f"forward:{funcName}\n".encode('utf-8'))
        self.process.stdin.flush()
        response = self.process.stdout.readline().decode('utf-8').strip()
        if response != "Done":
            raise Exception(f"Unexpected response from Mojo process during forward for {funcName}: {response}")
        result = None
        with open(self.folder + "/outfile", "rb") as f:
            result = pickle.load(f)
        return result

    def finish(self) -> None:
        if self.ready:
            self.ready = False
            try:
                self.process.communicate(input=b"\n", timeout=3)
            except:
                self.process.kill()
            shutil.rmtree(self.folder, ignore_errors=True)
        self.closed = True
        self.ready = False

    def getFunction(self, funcName: str) -> MojoFunction:
        self.ensureReady()
        if funcName not in self.funcManifests:
            raise Exception(f"Function {funcName} not found in MojoController")
        func = self.funcs.get(funcName, None)
        if func is None:
            func = MojoFunction(funcName, self.funcManifests[funcName], self)
            self.funcs[funcName] = func
        return func

    def checkOpen(self) -> None:
        if self.closed:
            raise Exception("MojoController has been closed")

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, MojoController):
            return False
        return self.processName == o.processName

    def __hash__(self) -> int:
        return hash(self.processName)
