import os
from sys import path as sys_path
from shutil import rmtree

sys_path.insert(0, '.') # Import repo's evadb instead of a pip-installed, even though it won't work for Mojo

from evadb import connect
from evadb.mojo import MOJO_BUILTINS_PATH
from evadb.functions.function_bootstrap_queries import Similarity_function_query


if __name__ == "__main__":
    if os.path.exists("evadb_data"):
        rmtree("evadb_data", ignore_errors=True)
    try:
        print("⏳ Establishing evadb connection...")
        cursor = connect().cursor()
        cursor.query(Similarity_function_query).execute()
        cursor.query(f"CREATE OR REPLACE FUNCTION SentenceTransformerFeatureExtractor IMPL '{MOJO_BUILTINS_PATH}'").execute()
        cursor.query(f"CREATE OR REPLACE FUNCTION CustomSentenceTransformerFeatureExtractor1 IMPL './mojo-demo/CustomSourceSTFES'").execute()
        cursor.query(f"CREATE OR REPLACE FUNCTION CustomSentenceTransformerFeatureExtractor2 IMPL './mojo-demo/CustomSourceSTFES'").execute()
        while True:
            print("")
            print("Using BUILTIN: Find similarity distance between two sentences (don't use special characters, including apostrophes)")
            sentence1 = input("Type sentence 1: ")
            sentence2 = input("Type sentence 2: ")
            # Use SentenceTransformerFeatureExtractor from evadb/mojo/funcs.mojo
            result = cursor.query(f"SELECT Similarity(SentenceTransformerFeatureExtractor('{sentence1}').features, SentenceTransformerFeatureExtractor('{sentence2}').features)").df()
            print("The distance is: " + str(result.iat[0,0]))
            print("")
            print("Using CUSTOM SOURCES: Find similarity distance between two sentences (don't use special characters, including apostrophes)")
            sentence1 = input("Type sentence 1: ")
            sentence2 = input("Type sentence 2: ")
            # Use CustomSentenceTransformerFeatureExtractor1 and CustomSentenceTransformerFeatureExtractor2 from ./mojo-demo/CustomSourceSTFES
            result = cursor.query(f"SELECT Similarity(CustomSentenceTransformerFeatureExtractor1('{sentence1}').features, CustomSentenceTransformerFeatureExtractor2('{sentence2}').features)").df()
            print("The distance is: " + str(result.iat[0,0]))
            print("")
            check = input("Do you want to continue? (y/n): ").lower()
            if check != "y" and check != "yes":
                break
        cursor.close()
    except Exception as e:
        print("❗️ Session ended with an error.")
        print(e)
        print("===========================================")
    finally:
        if os.path.exists("evadb_data"):
            rmtree("evadb_data", ignore_errors=True)
