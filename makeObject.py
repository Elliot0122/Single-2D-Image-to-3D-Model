import makeContour as mc
import makeJson as mj
import makeRhinoScript as ms
import os

folder = "chairs"

for path in os.listdir(folder):
    prefix = path.split('.')[0]
    if 'png' in path:
        print(f"{prefix} starts!")
        mc.run(os.path.join(folder, prefix))
        mj.run(os.path.join(folder, prefix))
        ms.run(os.path.join(folder, prefix))
        print(f"{prefix} is done!")