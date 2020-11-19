import pickle
import gzip


def save(objList,dir):
    with gzip.open(dir,"wb") as fw:
        pickle.dump(objList, fw)

def load(dir):
    with gzip.open(dir,"rb") as fr:
        return pickle.load(fr)