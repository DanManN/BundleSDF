import sys
from glob import glob

import cv2
import numpy as np
import trimesh as tm
import transformations as tf


def draw_box(img, vs):
    col1 = (0, 0, 255)
    col2 = (255, 0, 0)

    cls = [
        col1, col1, col1, col1, col2, col2, col1, col1, col1, col1, col1, col2
    ]

    img = cv2.line(img, vs[0], vs[1], cls[0], 2, 8, 0)
    img = cv2.line(img, vs[1], vs[2], cls[1], 2, 8, 0)
    img = cv2.line(img, vs[2], vs[3], cls[2], 2, 8, 0)
    img = cv2.line(img, vs[3], vs[0], cls[3], 2, 8, 0)

    img = cv2.line(img, vs[4], vs[5], cls[4], 2, 8, 0)
    img = cv2.line(img, vs[5], vs[6], cls[5], 2, 8, 0)
    img = cv2.line(img, vs[6], vs[7], cls[6], 2, 8, 0)
    img = cv2.line(img, vs[7], vs[4], cls[7], 2, 8, 0)

    img = cv2.line(img, vs[0], vs[4], cls[8], 2, 8, 0)
    img = cv2.line(img, vs[3], vs[7], cls[9], 2, 8, 0)
    img = cv2.line(img, vs[2], vs[6], cls[10], 2, 8, 0)
    img = cv2.line(img, vs[1], vs[5], cls[11], 2, 8, 0)
    return img


DIR = sys.argv[1]
print("reading from", DIR, "directory...")
camK = np.fromfile(DIR + '/cam_K.txt', sep=' ').reshape((3, 3))
mesh = tm.load_mesh(DIR + '/textured_mesh.obj')
bbox = mesh.bounding_box_oriented
scene = tm.scene.Scene([mesh, bbox])
scene.show()
base_transform, extents = tm.bounds.oriented_bounds(mesh)
print(extents)
bounds = tm.bounds.corners([-extents / 2, extents / 2])
bounds_t = tm.transform_points(bounds, tf.inverse_matrix(base_transform))
for filename in sorted(glob(DIR + '/ob_in_cam/*.txt')):
    transform = np.fromfile(filename, sep=' ').reshape((4, 4))
    print(filename)
    # print(transform, bounds)
    bounds_tt = tm.transform_points(bounds_t, transform)
    print(bounds_tt)
    img_file = DIR + '/color/' + filename.split('/')[-1].split('.')[0] + '.png'
    print(img_file)
    img = cv2.imread(img_file)
    points, _ = cv2.projectPoints(
        bounds_tt,
        (0, 0, 0),
        (0, 0, 0),
        camK,
        None,
    )
    points = [(int(p[0][0]), int(p[0][1])) for p in points]
    print(points)
    img = draw_box(img, points)
    cv2.imshow('test', img)
    cv2.waitKey()
