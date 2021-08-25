import rhinoscriptsyntax as rs

points = [[0, 0, 0], [0, 2, 0], [2, 3,0], [4, 2, 0], [4, 0, 0], [0, 0, 0]]

srf = rs.AddPlanarSrf(rs.AddCurve(points))

guide = rs.AddLine([0, 0, 0], [0, 0, -2])

extru = rs.ExtrudeSurface(srf, guide, True)