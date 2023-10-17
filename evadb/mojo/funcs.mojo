from python import Python
from sys import argv
from utils.vector import DynamicVector

let PythonNone = Python.none()

var FILES_FOLDER: PythonObject = PythonNone

var mojoh = PythonNone
var mlist = PythonNone

var pd = PythonNone
var SentenceTransformer = PythonNone
var FunctionManifest = PythonNone
var NumpyArray = PythonNone
var PyTorchTensor = PythonNone
var PandasDataframe = PythonNone
var Dimension = PythonNone
var NdArrayType = PythonNone
var input = PythonNone

struct SentenceTransformerFeatureExtractor:
    var ready: Bool
    var model: PythonObject

    fn manifest(self) raises -> PythonObject:
        return FunctionManifest()
            .name("SentenceTransformerFeatureExtractor")
            .cacheable(False)
            .function_type("mojo/FeatureExtraction")
            .batchable(False)
            .input_signatures(mlist(
                PandasDataframe()
                    .columns(mlist("data"))
                    .column_types(mlist(NdArrayType.STR))
                    .column_shapes(mlist((1,)))
            ))
            .output_signatures(mlist(
                PandasDataframe()
                    .columns(mlist("features"))
                    .column_types(mlist(NdArrayType.FLOAT32))
                    .column_shapes(mlist((1, 384)))
            ))

    fn __init__(inout self):
        self.ready = False
        self.model = PythonNone

    fn setup(inout self) raises:
        if not self.ready:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.ready = True

    fn forward(self, df: PythonObject) raises -> PythonObject:
        let resDf: PythonObject = pd.DataFrame()
        _ = resDf.__setitem__("features", mojoh.handle_df_apply_axis_1(df, self.model.encode))
        return resDf

var stfe = SentenceTransformerFeatureExtractor()

fn do_python_imports() raises:
    Python.add_to_path(".")

    mojoh = Python.import_module("evadb.mojoh")
    mlist = mojoh.mlist

    pd = Python.import_module("pandas")
    SentenceTransformer = Python.import_module("sentence_transformers").SentenceTransformer
    input = Python.import_module("builtins").input
    let evadb_functions_mojo = Python.import_module("evadb.functions.mojo")
    FunctionManifest = evadb_functions_mojo.FunctionManifest
    NumpyArray = evadb_functions_mojo.NumpyArray
    PyTorchTensor = evadb_functions_mojo.PyTorchTensor
    PandasDataframe = evadb_functions_mojo.PandasDataframe
    let evadb_catalog_catalog_type = Python.import_module("evadb.catalog.catalog_type")
    Dimension = evadb_catalog_catalog_type.Dimension
    NdArrayType = evadb_catalog_catalog_type.NdArrayType

fn do_manifests() raises:
    _ = mojoh.pickle_store(FILES_FOLDER + "/manifests/SentenceTransformerFeatureExtractor", stfe.manifest())

fn do_exec(cmd: PythonObject) raises:
    if cmd == "setup:SentenceTransformerFeatureExtractor":
        stfe.setup()
        return
    elif cmd == "forward:SentenceTransformerFeatureExtractor":
        let df = mojoh.pickle_load(FILES_FOLDER + "/infile")
        _ = mojoh.pickle_store(FILES_FOLDER + "/outfile", stfe.forward(df))
    else:
        raise Error("Unknown command")

fn main() raises:
    try:
        let args = argv()
        FILES_FOLDER = args[1]
        do_python_imports()
        do_manifests()
        print("Ready")
    except e:
        print("Error")
        return
    while True:
        try:
            let func: PythonObject = input()
            if not func:
                return
            if func == "":
                return
            do_exec(func)
            print("Done")
        except e:
            print("Error")
