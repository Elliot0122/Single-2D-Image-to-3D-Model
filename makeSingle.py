import makeContour as mc
import makeJson as mj
import makeRhinoScript as ms

path = 'chairs\\16-1'

mc.run(path)
mj.run(path)
ms.run(path)