import makeContour as mc
import makeJson as mj
import makeRhinoScript as ms
import makeobj as mo

# for r in range(100):
#     path = f'irregular_desk\\{r+1}-1'
#     mc.run(path)
#     mj.run(path)
#     ms.run(path)
#     mo.run(path)
irr = [2,4,5]
for r in irr:
    path = f'chairs\\{r}-1'
    mc.run(path)
    mj.run(path)
    ms.run(path)
    mo.run(path)
    #ad.run(path)