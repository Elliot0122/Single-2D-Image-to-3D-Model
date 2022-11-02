import separate_parts as sp
import extract_features_to_json as ef
import make_obj_file as mo

path = ".\\..\\data\\1-1"
sp.run(path)
ef.run(path)
mo.run(path)