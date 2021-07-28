import rhinoscriptsyntax as rs
rs.AddBox([[-8, -60, -5], [-8, -60, 5], [-8, 60, 5], [-8, 60, -5], [8, -60, -5], [8, -60, 5], [8, 60, 5], [8, 60, -5]])
rs.AddCylinder([0, 0, 0], 6, 6, True)
