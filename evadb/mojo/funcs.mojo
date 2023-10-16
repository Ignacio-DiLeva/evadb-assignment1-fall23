from python import Python
from sys import argv
from utils.vector import DynamicVector

var FILES_FOLDER: String = ""

var mojoh: PythonObject = None
var mlist: PythonObject = None

var pd: PythonObject = None
var SentenceTransformer: PythonObject = None
var FunctionManifest: PythonObject = None
var NumpyArray: PythonObject = None
var PyTorchTensor: PythonObject = None
var PandasDataframe: PythonObject = None
var Dimension: PythonObject = None
var NdArrayType: PythonObject = None
var input: PythonObject = None

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
        self.model = None

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
    Python.add_to_path("evadb")

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

fn do_exec(cmd: String) raises:
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
        if len(args) < 2:
            print("Error")
            return
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
            let cmd: String = func.to_string()
            if cmd == "":
                return
            do_exec(cmd)
            print("Done")
        except e:
            print("Error")
