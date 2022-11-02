def cross(o,a,b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
def compare(a):
    return (a[0],a[1])
def length2(a,b):
    return(a[0]-b[0])**2+(a[1]-b[1])**2
def far(o,a,b):
    return length2(o,a) > length2(o,b)
def Jarvis_march(points):
    CH = []
    points.sort(key=compare)
    m = 1
    CH.append(points[0])
    current = 0
    while True:
        next = current
        for r in range(len(points)):
            c = cross(CH[m-1],points[r],points[next])
            if c > 0 or c == 0 and far(CH[m-1],points[r],points[next]):
                next = r
        if next == 0:
            break
        CH.append(points[next])
        m+=1
        current = next
    return CH
if __name__ == '__main__':
    points = [[0,0],[0,1],[1,0]]
    print(Jarvis_march(points))