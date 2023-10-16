import pickle

def handle_df_apply_axis_1(df, applied):
    return df.apply(applied, axis=1)

def pickle_load(fname):
    data = None
    with open(fname, 'rb') as f:
        data = pickle.load(f)
    return data

def pickle_store(fname, obj):
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)

def mlist(*args):
    return list(args)
