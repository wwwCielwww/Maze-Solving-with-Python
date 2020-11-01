import cv2
import matplotlib.pyplot as plt
import numpy as np

class vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.d = float('inf') 
        self.parent_x = None
        self.parent_y = None
        self.processed = False
        self.index_in_queue = None

def get_neighbors(mat, i, j):

    shape = mat.shape
    neighbors = []

    if i > 0 and not mat[i - 1][j].processed:
        neighbors.append(mat[i - 1][j])
    if i < shape[0] - 1 and not mat[i + 1][j].processed:
        neighbors.append(mat[i + 1][j])
    if j > 0 and not mat[i][j - 1].processed:
        neighbors.append(mat[i][j - 1])
    if j < shape[1] - 1 and not mat[i][j + 1].processed:
        neighbors.append(mat[i][j + 1])

    return neighbors

def bubble_up(queue, index):

    if index <= 0:
        return queue

    p_index = (index-1)//2
    if queue[index].d < queue[p_index].d:
            queue[index], queue[p_index] = queue[p_index], queue[index]
            queue[index].index_in_queue = index
            queue[p_index].index_in_queue = p_index
            queue = bubble_up(queue, p_index)
    return queue

def bubble_down(queue, index):

    length = len(queue)
    lc_index = 2 * index + 1
    rc_index = lc_index + 1

    if lc_index >= length:
        return queue
    if lc_index < length and rc_index >= length: 
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index] = queue[lc_index], queue[index]
            queue[index].index_in_queue = index
            queue[lc_index].index_in_queue = lc_index
            queue = bubble_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index], queue[small] = queue[small], queue[index]
            queue[index].index_in_queue = index
            queue[small].index_in_queue = small
            queue = bubble_down(queue, small)

    return queue

def get_distance(img, u, v):

    return 0.1 + (float(img[v][0]) - float(img[u][0])) ** 2 +\
        (float(img[v][1]) - float(img[u][1])) ** 2 + (float(img[v][2]) - float(img[u][2])) ** 2

def drawPath(img, path, thickness=2):

    x0, y0 = path[0]
    for vert in path[1:]:
        x1, y1 = vert
        cv2.line(img, (x0, y0), (x1, y1), (255, 0, 0), thickness)
        x0, y0 = vert

def find_shortest_path(img, src, dst):

    pq = [] 
    source_x = src[0]
    source_y = src[1]
    dest_x = dst[0]
    dest_y = dst[1]
    rows, cols = img.shape[0], img.shape[1]
    mat = np.full((rows, cols), None) 

    for i in range(rows):
        for j in range(cols):
            mat[i][j] = vertex(j, i)
            mat[i][j].index_in_queue = len(pq)
            pq.append(mat[i][j])

    mat[source_y][source_x].d = 0
    pq = bubble_up(pq, mat[source_y][source_x].index_in_queue)
    
    while len(pq) > 0:
        u = pq[0]
        u.processed = True
        pq[0] = pq[-1]
        pq[0].index_in_queue = 0
        pq.pop()
        pq = bubble_down(pq, 0)
        neighbors = get_neighbors(mat, u.y, u.x)

        for v in neighbors:
            dist = get_distance(img, (u.y, u.x), (v.y, v.x))

            if u.d + dist < v.d:
                v.d = u.d + dist
                v.parent_x = u.x
                v.parent_y = u.y
                idx = v.index_in_queue
                pq = bubble_down(pq, idx)
                pq = bubble_up(pq, idx)
                          
    path=[]
    iter_v = mat[dest_y][dest_x]
    path.append((dest_x, dest_y)) 

    while(iter_v.y != source_y or iter_v.x != source_x):
        path.append((iter_v.x, iter_v.y))
        iter_v = mat[iter_v.parent_y][iter_v.parent_x]

    path.append((source_x,source_y))
    return path