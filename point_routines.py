import math

def dummy_path():
    """
    A list of points = simple list of (x, y) coords representing points which can be joined by lines
    by drawing routines. Equivalent to a polyline of distinct line segements.
    LATER may refactor to include other svg path types
    """
    return [(0, 0), (1, 1)]

def dummy_layer():
    """
    A list paths representing a number of line segements all to be on the same layer of the drawing
    Each segement is independent, it will only follow on from a previous segment if linking coords are given
    i.e. end point of one sublist is equal to start point of next sublist
    """
    return [[(0, 0), (0, 1)], [(0, 1), (1, 1), (1, 0), (0, 0)]]

def dummy_layer2():
    return [[(4, 4), (4, 5)], [(4, 5), (5, 5), (5, 4), (4, 4)]]

def dummy_score_layer():
    return [[(0, 0), (1, 1)]]

def dummy_drawing(cl, sl):
    """
    Dictionary collection of layers that make up a drawing keyed by layer name
    For most drawings there will be a cut layer and a score layer
    e.g.. dwg['cut'] = layer_a, dwg['score'] = layer_b etc
    """
    dwg = {}
    dwg['cut'] = cl
    dwg['score'] = sl
    return dwg

def path_xybounds(path):
    minx = min(p[0] for p in path)
    miny = min(p[1] for p in path)
    maxx = max(p[0] for p in path)
    maxy = max(p[1] for p in path)
    return minx, miny, maxx, maxy

def layer_xybounds(layer):
    minx = min(path_xybounds(path)[0] for path in layer)
    miny = min(path_xybounds(path)[1] for path in layer)
    maxx = max(path_xybounds(path)[2] for path in layer)
    maxy = max(path_xybounds(path)[3] for path in layer)
    return (minx, miny, maxx, maxy)

def translate_path(path, v):
    """
    translate each point in a path by the vector v
    """
    _path = []
    for p in path:
        _path.append((p[0] + v[0], p[1] + v[1]))
    return _path

def rotate_path(path, theta):
    """
    rotate each point in a path by the angle theta anticlockwise about origin
    NOTE svg & beam coord systems are +ve y down so this renders as clockwise
    """
    theta = math.radians(theta)
    _path = []
    for p in path:
        _path.append((p[0] * math.cos(theta) - p[1] * math.sin(theta), p[0] * math.sin(theta) + p[1] * math.cos(theta)))
    return _path

def round_path(path, d):
    """
    round coords to d digits
    mainly for printing sensibly, not needed for drawing
    svg seems insensitive to integer vs fp e.g 1 vs 1.0
    """
    _path = []
    for p in path:
        _path.append((round(p[0], d), round(p[1], d)))
    return _path

def translate_layer(layer, v):
    """
    translate each path in layer by the vector v
    """
    _layer = []
    for path in layer:
        _layer.append(translate_path(path, v))
    return _layer

def rotate_layer(layer, theta):
    """
    rotate each sub list of layer by theta
    """
    _layer = []
    for pl in layer:
        _layer.append(rotate_path(pl, theta))
    return _layer

def round_layer(layer, d):
    """
    round coords to d digits in each sub list
    mainly for printing sensibly, not needed for drawing
    """
    _layer = []
    for pl in layer:
        _layer.append(round_path(pl, d))
    return _layer

def translate_drawing(dwg, v):
    """
    translate each layer in drawing by the vector v
    """
    _dwg = {}
    for k, layer in dwg.items():
        _dwg[k] = translate_layer(layer, v)
    return _dwg

def rotate_drawing(dwg, theta):
    """
    translate cut and score sub lpls by the vector v
    should work for any number of sub lpls in list
    """
    _dwg = {}
    for k, layer in dwg.items():
        _dwg[k] = rotate_layer(layer, theta)
    return _dwg

def pair_drawing(dwg, trl):
    """
    helper routing to allow easier tiling of some polygons and struts
    where useful to create a pair by rotate, translate and appending
    :param dwg:
    :param trl: transform list (angle, x, y) tuple
    :return: pair of input dwg with second rotated by angle and translated x,y
    """
    angle, x, y = trl
    _dwg = {}
    for k, layer in dwg.items():
        _dwg[k] = layer + translate_layer(rotate_layer(layer, angle), (x, y))

    return _dwg

def round_drawing(dwg, d):
    """
    round coords to d digits in cut and score sub lpls
    mainly for printing sensibly, not needed for drawing
    """
    _dwg = {}
    for  k, layer in dwg.items():
        _dwg[k] = round_layer(layer, d)
    return _dwg

def merge_drawings(dwg1, dwg2, xoffset, yoffset):
    """
    merge two drawings into one
    dwg1 moved to origin and dwg2 offset relative to right edge by xoffset and bottom by yoffset
    if x or y offsets are 0 then position at left or top edge
    positioning based on cut layers only
    """

    dwg1bounds = layer_xybounds(dwg1['cut'])
    _dwg1 = translate_drawing(dwg1, (-dwg1bounds[0], -dwg1bounds[1]))

    dwg2bounds = layer_xybounds(dwg2['cut'])
    if xoffset == 0: # move to yoffset below dwg1
        _dwg2 = translate_drawing(dwg2, (-dwg2bounds[0], -dwg2bounds[1] - dwg1bounds[1] + dwg1bounds[3] + yoffset))
    elif yoffset == 0: # move to xoffset right of dwg1
        _dwg2 = translate_drawing(dwg2, (-dwg2bounds[0] - dwg1bounds[0] + dwg1bounds[2] + xoffset, -dwg2bounds[1]))
    else: # offset both x and y relative to dwg1 lower right corner
        _dwg2 = translate_drawing(dwg2, (-dwg2bounds[0] - dwg1bounds[0] + dwg1bounds[2] + xoffset, -dwg2bounds[1] - dwg1bounds[1] + dwg1bounds[3] + yoffset))

    #merge
    for k, layer in _dwg1.items():
        _dwg1[k].extend(_dwg2[k])

    return _dwg1

if __name__ == '__main__':
    print("path       : ", dummy_path())
    print("layer   : ", dummy_layer())
    print("dwg : ", dummy_drawing(dummy_layer(), dummy_score_layer()))

    # translate, rotate operations are on point lists
    print("\nTransformations on single path")
    print("Translate path by 1,1 :", translate_path(dummy_path(), (1, 1)))
    print("Rotate path by 90deg (anticlockwise) :", round_path(rotate_path(dummy_path(), 90), 0))

    print("\nTransformations on layers - iterate over path routines")
    print("Translate layer by 1,1 :", translate_layer(dummy_layer(), (1, 1)))
    print("Rotate layer by 90deg :", round_layer(rotate_layer(dummy_layer(), 90), 0))

    print("\nTransformations on dwg - iterate over layers dictionary")
    print("Translate cs line point list by 1,1 :", translate_drawing(dummy_drawing(dummy_layer(), dummy_score_layer()), (1, 1)))
    print("Rotate cs line point list by 90deg :", round_drawing(rotate_drawing(dummy_drawing(dummy_layer(), dummy_score_layer()), 90), 0))

    print("\nMin, Max coords")
    print(path_xybounds(dummy_path()))
    print(layer_xybounds(dummy_layer()))
    print(layer_xybounds(dummy_layer2()))

    print(merge_drawings(dummy_drawing(dummy_layer(),dummy_score_layer()), dummy_drawing(dummy_layer2(), dummy_score_layer()),0,0.5))

