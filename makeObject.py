import makeContour as mc
import makeJson as mj
import makeRhinoScript as ms
import makeobj as mo
import addPoint as ad
import os

folder = "chairs"

for path in os.listdir(folder):
    prefix = path.split('.')[0]
    if 'png' in path:
        print(f"{prefix} starts!")
        mc.run(os.path.join(folder, prefix))
        mj.run(os.path.join(folder, prefix))
        ms.run(os.path.join(folder, prefix))
        mo.run(os.path.join(folder, prefix))
        ad.run(os.path.join(folder, prefix))
        print(f"{prefix} is done!")