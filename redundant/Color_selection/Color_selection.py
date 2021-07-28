import numpy as np
import statistics as s
import queue as q

# This program allow users to get color that are not so similar

_similarity = 0.6
quantity = 30


def similation(color, box):
    # print("Similation start.")
    for x in range(len(color)):
        # print("box: ", box)
        # print("color: ", color)
        col = ([i / j for i, j in zip(box, color[x])])
        sim = s.harmonic_mean(col)/s.mean(col)
        # print(sim)
        if sim > _similarity:
            return False
    return True


# color = [[1, 1, 1], [1, 1, 7], [1, 1, 45], [1, 7, 1], [1, 7, 7], [1, 7, 45], [1, 45, 1], [1, 45, 7], [1, 45, 45], [
#     7, 1, 1], [7, 1, 7], [7, 1, 45], [7, 7, 1], [7, 45, 1], [45, 1, 1], [45, 1, 7], [45, 1, 45], [45, 7, 1], [45, 45, 1]]
color = []

multiple = []

for x in color:
    z = 1
    while (z*x[0] <= 255 and z*x[1] <= 255 and z*x[2] <= 255):
        multiple.append(z*x)
        z += 1


for b in range(1, 256):
    for g in range(1, 256):
        for r in range(1, 256):
            if len(color) == quantity:
                break
            elif [b, g, r] in multiple:
                # print("same!")
                break
            elif len(color) == 0:
                color.append([b, g, r])
            else:
                if similation(color, [b, g, r]) == True:
                    color.append([b, g, r])
                    z = 1
                    while (z*b <= 255 and z*g <= 255 and z*r <= 255):
                        multiple.append(z*[b, g, r])
                        z += 1
                else:
                    continue

print("Exporting results...")
mat = np.matrix(color)
with open('./color.txt', 'wb') as f:
    for line in mat:
        np.savetxt(f, line, fmt='%.2f')
