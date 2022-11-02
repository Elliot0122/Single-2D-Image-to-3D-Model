import separate_parts as sp
import extract_features_to_json as ef
import make_obj_file as mo
import os

folder = ".\\..\\data"

for path in os.listdir(folder):
    prefix = path.split('.')[0]
    if 'png' in path:
        print(f"{prefix} starts!")
        sp.run(os.path.join(folder, prefix))
        ef.run(os.path.join(folder, prefix))
        mo.run(os.path.join(folder, prefix))
        #ad.run(os.path.join(folder, prefix))
        print(f"{prefix} is done!")