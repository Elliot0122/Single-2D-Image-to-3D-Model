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
irr = [1]
for r in irr:
    path = f'irregular_desk\\{r}-1'
    mc.run(path)
    mj.run(path)
    ms.run(path)
    mo.run(path)
    #ad.run(path)