from evadb import connect
from evadb.mojo import MOJO_BUILTINS_PATH


if __name__ == "__main__":
    try:
        print("Find similarity between two sentences")
        sentence1 = input("Type sentence 1: ")
        sentence2 = input("Type sentence 2: ")
        # establish evadb api cursor
        print("⏳ Establishing evadb connection...")
        cursor = connect().cursor()
        cursor.create_function("SentenceTransformerFeatureExtractor", True, MOJO_BUILTINS_PATH).execute()
        result = cursor.query(f"SELECT Similarity(SentenceTransformerFeatureExtractor('{sentence1}').features, SentenceTransformerFeatureExtractor('{sentence2}').features);").df()
        print("The distance is: " + str(result.iloc[0]["similarity.distance"]))
        cursor.close()
    except Exception as e:
        print("❗️ Session ended with an error.")
        print(e)
        print("===========================================")
