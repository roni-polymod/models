import math
from point_routines import translate_path, translate_layer, translate_drawing, pair_drawing, \
    rotate_path, rotate_layer, round_path

def quadr_from_point_dxdy(base_point, dxplus, dxminus, dyplus, dyminus, theta):
    """
    given base point (x,y) return list of 4 points for corners of quadrilateral
    from delta x,y from base and rotated by angle theta
    :param base_point:
    :param dxplus:
    :param dxminus:
    :param dyplus:
    :param dyminus:
    :param theta:
    :return: path of 5 points for quadrilateral, 5th point duplicates the first to form a closed path
    """
    bx, by = base_point
    _path = [(bx + dxplus, by - dyminus), (bx + dxplus, by + dyplus), (bx - dxminus, by + dyplus), (bx - dxminus, by - dyminus), (bx + dxplus, by - dyminus)]
    if theta != 0:
        _path = round_path(rotate_path(_path, theta), 2)
    return _path

def simple_quadrilateral(l, w, theta):
    """
    lxw mm edge quadrilateral, centre at origin
    :parameter l: quad edge length
    :parameter w: quad edge width
    :parameter theta: rotation about origin

    TODO sloped parallelograms
    """

    _cutpath = quadr_from_point_dxdy((0,0), l/2, l/2, w/2, w/2, theta)
    _dwg = {'cut': [_cutpath]}
    return _dwg

def edgetab_dwg(l, le, ta, if2, so, ve, isl, etc, theta, tab_type):
    """
    draw a single edge tab cut layer and score layer
    edge will be duplicated by other routines to form polygon face drawings
    :parameter l: edge length
    :parameter le: end tab length
    :parameter ta: tab thickness. Tabs will have score lines
    :parameter if2: interference distance divided by 2 - to adjust tab interference for cut width
    :parameter so: score offset to give flatter folded edge with score folds level with cuts
    :parameter ve: v taper width to add to edge of tab for end tabs
    :parameter isl: incomplete score length, leave an unscored length so that tabs spring back
    :parameter etc: end tab clearance
    :parameter theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    :parameter tab_type: various types of tab on edge of polygon faces, see below
    :return dict drawing of cut and score layers
    """

    if tab_type == 0: # just a straight line, no score to create polygon face with no tabs
        # cut_path1 = [(0, 0), (l - 0.3, 0)]  # gap to leave piece attached to sheet
        cut_path1 = [(0, 0), (l, 0)]
        return {'cut': [cut_path1]}

    elif tab_type == 1: # tab type Jan 2021` to still allow overlap method but also make tuck in method easier
        cut_path1 = [(0, 0), (le, 0)]
        cut_path1a = [(le + so, 0 - so), (le - ve, ve), (le - (1.25 * ve), ta), ((l / 2) - (ve / 2) - 0.3, ta / 2)]
        cut_path2 = [((l / 2) - (ve / 2), ta / 2), ((l / 2) + (1.1 * if2), ta / 4), ((l / 2) + if2, 0 - so)]
        # cut_path2 = [((l / 2) - (ve / 2), ta / 2), ((l / 2) + if2, 0 - so)]
        cut_path2a = [((l / 2) + if2, 0), (l - le, 0)]
        cut_path2b = [(l - le + so, 0 - so), (l - le - ve, ve), (l - le - (1.25 * ve), ta),
                            (l - etc - (ta * math.tan(math.radians(theta))), ta), (l - etc + so, 0 - so)]
        cut_path2c = [(l - etc, 0), (l, 0)]

        score_path1 = [(le - if2 + isl, 0 - so), ((l / 2) - isl, 0 - so)]
        score_path2 = [((l - le) - if2 + isl, 0 - so), (l - etc, 0 - so)]
        return {'cut': [cut_path2c, cut_path2b, cut_path2a, cut_path2, cut_path1a, cut_path1], 'score': [score_path2, score_path1]}

    elif tab_type == 2: # original tabs pre Dec 2020 for overlap and slide join method
        # vm retired Jan 2021
        vm = ve
        cut_path1 = [(0, 0), (le, 0)]
        cut_path1a = [(le + so, 0 - so), (le - ve,  1.5 * ve), (le + ve, ta), ((l / 2) - vm - 0.3, ta)]
        cut_path2 = [((l / 2) - vm, ta), ((l / 2) + if2, ta / 3), ((l / 2) + if2, 0 - so)]
        cut_path2a = [((l / 2) + if2, 0), (l - le, 0)]
        cut_path2b = [(l - le + so, 0 - so), (l - le - ve, 1.5 * ve), (l - le + ve, ta),
                            (l - etc - (ta * math.tan((theta / 360) * (2 * math.pi))), ta), (l - etc + so, 0 - so)]
        cut_path2c = [(l - etc, 0), (l, 0)]

        score_path1 = [(le - if2 + isl, 0 - so), ((l / 2) - isl, 0 - so)]
        score_path2 = [((l - le) - if2 + isl, 0 - so), (l - etc, 0 - so)]
        return {'cut': [cut_path2c, cut_path2b, cut_path2a, cut_path2, cut_path1a, cut_path1], 'score': [score_path2, score_path1]}

    elif tab_type == 4: # for acrylic/plywood etc thicker materials castellated mesh together
        acth = 3   #acrylic thickness mm
        cut_path1 = [(0, 0), (0, acth), (l / 4, acth), (l / 4, 0), (l / 2, 0), (l / 2, acth), (3 * l / 4, acth), (3 * l / 4, 0), (l, 0)]
        return {'cut': [cut_path1]}

    else:
        return {}

def tab_testStrips(l, le, w, **faceparamdict):
    """
    draw a tabbed test strip with tab on single edge, width w
    """

    _dwg = edgetab_dwg(l, le, **faceparamdict)
    box_points = [(0, 0), (0, - w), (l, - w), (l, 0)]
    _dwg['cut'].append(box_points)

    return _dwg

def nsided_polygon(edge_dwg, l, n):
    """
    repeat edge drawing to form a regular n sided polygon drawing
    :param edge_dwg: edge drawing
    :param l: edge length
    :param n: number of edges
    :return: polygonised drawing
    """

    #half internal angle of polygon for translation
    theta_radians = (math.pi - (2 * math.pi / n)) / 2
    v = (-l / 2, (l / 2) * math.tan(theta_radians))

    # Translate - assumes edge starts at origin, so first translate to correct radial position
    _edge_dwg = translate_drawing(edge_dwg, v)

    # Rotations - create polygon from n rotations of edge
    _dwg = {}
    for k, layer in _edge_dwg.items():
        _layer = []
        for i in range(n):
            _layer.extend(rotate_layer(layer, math.degrees(2 * math.pi / n) * i))
        _dwg[k] = _layer

    return _dwg

def transformlist_polygon(edge_dwg, trl):
    """
    repeat edge drawing to form a polygon with equal edges from transform list
    :param edge_dwg: edge drawing
    :param trl: transform list = list of tuples (angle, x, y) for sequence of translate(rotate(pl, angle), (x,y) operations
    :return: polygonised drawing
    """
    _dwg = {}
    for k, layer in edge_dwg.items():
        _layer = []
        for (angle, x, y) in trl:
            _layer.extend(translate_layer(rotate_layer(layer, angle), (x, y)))
        _dwg[k] = _layer

    return _dwg

def transformlist_polygon_indexedges(edge_dwg_list, trli):
    """
    repeat edge drawing from list of edges to form a polygon with unequal edges from indexed transform list
    :param edge_dwg_list: list of edge drawings, index position indicated in trli
    :param trli: transform list = list of tuples (angle, x, y, i) for sequence of translate(rotate(pl, angle), (x,y) operations
        with index i used to select edge from list of edges
    :return: polygonised cut and score line point lists
    """
    _dwg = {}
    for k in edge_dwg_list[0]:
        _layer = []
        for (angle, x, y, i) in trli:
            _layer.extend(translate_layer(rotate_layer(edge_dwg_list[i][k], angle), (x, y)))
        _dwg[k] = _layer

    return _dwg

def polygon(l, le, n, **faceparamdict):
    """
    face for n sided regular polygon
    """
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    _dwg = nsided_polygon(_edge_dwg, l, n)

    # pair if needed for easier array tiling
    # _dwg = pair_drawing(_dwg, 0, 0, l * math.sqrt(3) + (1.7 * faceparamdict['ta']))

    return _dwg

def triangle_pair(l, le, **faceparamdict):
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    _dwg = nsided_polygon(_edge_dwg, l, 3)

    # tetrahedron, octahedron, pair with 180deg rotation for better tiling on page
    _dwg = pair_drawing(_dwg, (180, 0.63 * l, -0.25 * l))

    return _dwg

def triangle_icos(l, le, **faceparamdict):
    # variation of triangle_pair to give 5 triangles in a row for icosahedron for better fit to A4 size
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    _dwg = nsided_polygon(_edge_dwg, l, 3)

    # icosahedron 5 triangle_pair row for 5r - comment out above line for tetra/octahedron
    _d = _dwg.copy()
    _dwg = pair_drawing(_dwg, (180, 0.63 * l, -0.25 * l))
    _dwg = pair_drawing(_dwg, (0, 1.35 * l, 0))
    for k, layer in _dwg.items():
        layer.extend(translate_layer(_d[k], (2.7 * l, 0)))

    return _dwg

def triangle_nscored_pair(l, le, nscored, **faceparamdict):
    """
    l mm edge equilateral triangle_pair, with nscored edges scored
    testing use of unscored edges for non-convex joins
    :parameter l: eq tri edge length
    :parameter le: length of end tab
    :parameter faceparamdict: see calling routines
    :parameter nscored: the number of scored edges - must be 0, 1 or 2 (3 gives same result as triangle_pair)
    :return dwg
    """
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    # half internal angle of polygon for translation
    n = 3
    theta_radians = (math.pi - (2 * math.pi / n)) / 2
    v = (-l / 2, (l / 2) * math.tan(theta_radians))

    # translate to correct radial position
    _edge_dwg = translate_drawing(_edge_dwg, v)

    # Rotations - create polygon from n rotations of edge
    _dwg = {}
    for k, layer in _edge_dwg.items():
        _layer = []
        for i in range(n):
            if k == 'score':
                if i < nscored:
                    continue
            _layer.extend(rotate_layer(layer, math.degrees(2 * math.pi / n) * i))
        _dwg[k] = _layer

    # add another for easier array tiling
    _dwg = pair_drawing(_dwg, (180, 0.63 * l, -0.25 * l))

    return _dwg

def triangle_custom_pair(l, le, **faceparamdict):
    """
    l mm edge0 triangle_pair, edge1, edge2 in ratio set below
    :parameter l: edge length
    :parameter le: length of end tab
    :parameter faceparamdict: see calling routines
    :return [cutlpl, scorelpl] for polyhedron triangle_pair tabbed face
    """

    # 90, 45, 45 triangle_pair
    # ratio0l for scaling from l, ratio of edge1 and edge2 to edge0
    ratio_0l, ratio_10, ratio_20 = 1, 1, math.sqrt(2)
    # triangle_pair, 3 side transform list
    l0, le0 = ratio_0l * l, ratio_0l * le
    trl = [(180, l0, 0), (90, 0, 0), (-45, 0, l0)]

    # # lengths 1, sqrt2, sqrt3 triangle_pair
    # # ratio0l for scaling from l, ratio of edge1 and edge2 to edge0
    # ratio_0l, ratio_10, ratio_20 = 1, math.sqrt(2), math.sqrt(3)
    # # triangle_pair, 3 side transform list
    # # trl = [(180, l, 0), (90, 0, 0), (-54.74, 0, l * ratio_10)]
    # # mirror
    # trl = [(0, 0, 0), (90, 0, -l * ratio_10), (-(180 - 54.74), l, 0)]

    _edge_dwgl = []
    _edge_dwgl.append(edgetab_dwg(l0, le0, **faceparamdict))
    _edge_dwgl.append(edgetab_dwg(l0 * ratio_10, le0 * ratio_10, **faceparamdict))
    _edge_dwgl.append(edgetab_dwg(l0 * ratio_20, le0 * ratio_20, **faceparamdict))

    _dwg = {}
    for k in _edge_dwgl[0]:
        _layer = []
        for i in range(3):
            angle, x, y = trl[i]
            _layer.extend(translate_layer(rotate_layer(_edge_dwgl[i][k], angle), (x, y)))
        _dwg[k] = _layer

    # pair for easier array tiling
    _dwg = pair_drawing(_dwg, (180, 1.1 * l0, 1.1 * l0))

    return _dwg

def square(l, le, **faceparamdict):
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    _dwg = nsided_polygon(_edge_dwg, l, 4)
    return _dwg

def pentagon(l, le, **faceparamdict):
    _edge_dwg = edgetab_dwg(l, le, **faceparamdict)
    _dwg = nsided_polygon(_edge_dwg, l, 5)

    # add another for easier array tiling 5e, not 5r
    _dwg = pair_drawing(_dwg, (180, 1.4 * l, 0.7 * l))

    return _dwg

def spherical_segment(l, le, w, we, **faceparamdict):
    """
    lxw mm edge tabbed rectangle, with score for tab folds
    :parameter l: edge length - untabbed
    :parameter le: length of end tab
    :parameter w: side length - sloped tabbed side for spherical triangle_pair
    :parameter we: length of end tab
    :parameter faceparamdict: see calling routines
    :return list of lists [[sublists for sequence of points to be cut],[sublists for sequence of points to be scored]]
    """

    # angles from Coxeter for spherical kaleidoscope
    # 2,3,3  54deg44min x2, 70deg32min
    # 2,3,4  35deg16min, 45deg, 54deg44min
    # 2,3,5  20deg54min, 31deg43min, 37deg23min
    theta = (35 + 16/60)/2
    sint = math.sin(math.radians(theta))
    cost = math.cos(math.radians(theta))

    # comment out one or other of these lines if ends are to be tabbed or not TODO need to lengthen second straight edge
    # _edge_dwgl = edgetab_dwg(l, le, **faceparamdict)      # normal edge
    _edge_dwgl = {'cut': [[(0,0), (2 * l * sint, 0)]]}    # override to give flat edge rather than tab

    _edge_dwgw = edgetab_dwg(w, we, **faceparamdict)

    # rect 4 side alternate transform
    trl = [(180, 2 * l * sint, 0), (270 - theta, 2 * l * sint + w * sint, w * cost), (0, 0, w * cost), (90 + theta, 0, 0)]

    _dwg = {}
    for k in _edge_dwgl:
        _layer = []
        for i in range(4):
            angle, x, y = trl[i]
            if i % 2 == 0:
                _layer.extend(translate_layer(rotate_layer(_edge_dwgl[k], angle), (x, y)))
            else:
                _layer.extend(translate_layer(rotate_layer(_edge_dwgw[k], angle), (x, y)))
        _dwg[k] = _layer

    return _dwg
    # cs_pll = []
    # wlist = [1,3]   #index width sides
    #
    # # cutlists
    # _pll = []
    # for i, (angle, x, y) in enumerate(trl):
    #     if i in wlist:
    #         pll = cpllw
    #     else:
    #         pll = cpll
    #     for pl in pll:
    #         _pll.append(translate_path(rotate_path(pl, angle), (x, y)))
    # cs_pll.append(_pll)
    #
    # # scorelists
    # _pll = []
    # for i, (angle, x, y) in enumerate(trl):
    #     if i in wlist:
    #         pll = spllw
    #     else:
    #         pll = spll
    #     for pl in pll:
    #         _pll.append(translate_path(rotate_path(pl, angle), (x, y)))
    # cs_pll.append(_pll)
    #
    # return [cs_pll[0], cs_pll[1]]

def rhombus(l, le, rt, **faceparamdict):
    """
    l mm edge rhombus
    :parameter l: edge length
    :parameter le: length of end tab
    :parameter rt: rhombus theta - first internal angle of rhombus - see Cundy and Rollett
        rhombic dodecahedron = 70.53 deg, rhombic triacontahedron = 63.43
    :parameter faceparamdict: see calling routines
    :return list of lists [[sublists for sequence of points to be cut],[sublists for sequence of points to be scored]]
    """

    _dwg = edgetab_dwg(l, le, **faceparamdict)

    sinrt = math.sin((rt / 360) * (2 * math.pi))
    cosrt = math.cos((rt / 360) * (2 * math.pi))

    # transform list 4 sides of rhombus
    trl = [(90, 0, 0), (-(90 + rt), l * sinrt, l * cosrt), (-90, l * sinrt, l * (1 + cosrt)), (90 - rt, 0, l)]

    _dwg = transformlist_polygon(_dwg, trl)

    # pair for easier tiling
    # _dwg = pair_drawing(_dwg, (0, l * sinrt + faceparamdict['ta'] + 1, -1.5))

    return _dwg

def rhombus_simple(l, le, rt, **faceparamdict):
    """
    l mm edge rhombus, no tabs or scores to create flat tiling patterns
    :parameter rt: rhombus angle

    other parameters are not used due to simple no tab edges
    """
    sinrt = math.sin(math.radians(rt))
    cosrt = math.cos(math.radians(rt))

    # cut_pll = transformlist_polygon(tpll, [(180, l, 0), (270, l, l), (0, 0, l), (90, 0, 0)])
    _cut = [[(0.3, 0), (l, 0), (l + l * cosrt, l * sinrt)], [(l + l * cosrt - 0.3, l * sinrt), (l * cosrt, l * sinrt), (0, 0)]]
    _dwg = {'cut': _cut}

    # pair for easier tiling
    # _dwg = pair_drawing(_dwg, (0, l * sinrt + faceparamdict['ta'] + 1, -1.5))

    return _dwg

def catalan_polygon(l, le, catalan_type, **faceparamdict):
    """
    l mm short edge catalan polygon
    Pentagonal hexacontahedron (snub dodecahedron dual), face angles 118deg 8', 67deg 28', 60 faces
    :parameter l: edge length
    :parameter le: length of end tab
    :parameter catalan_type: either pi or di for Pentagonal icositetrahedron or Deltoidal icositetrahedron pentagons
    :parameter faceparamdict: see calling routines
    :return polygon drawing
    """

    _edge_dwg0 = edgetab_dwg(l, le, **faceparamdict)

    if catalan_type == 'pi':    # Pentagonal icositetrahedron (snub cube dual), 24x pentagon 3,3,3,3,4, angles 114deg 48.5', 80deg 46'
        A = 180 - (114 + 48.5 / 60)
        B = 180 - 2 * A
        cosA, sinA = math.cos(math.radians(A)), math.sin(math.radians(A))
        cosB, sinB = math.cos(math.radians(B)), math.sin(math.radians(B))

        # ratio to longer side
        l1 = l * (0.5 + cosA) / cosB   # = 1.4193 * l
        le1 = le * l1 / l
        _edge_dwg1 = edgetab_dwg(l1, le1, **faceparamdict)

        #pentagon, 5 side indexed transform list
        trli = [(90, 0, 0, 0), (90 + A, l * sinA, -l * cosA, 0), (90 + 2 * A, l * sinA + l1 * sinB, -l * cosA + l1 * cosB, 1),
                (90 - 2 * A, l * sinA, -l * cosA + 2 * l1 * cosB, 1), (90 - A, 0, l, 0)]
        _dwg = transformlist_polygon_indexedges([_edge_dwg0, _edge_dwg1], trli)

    elif catalan_type == 'di': # Deltoidal icositetrahedron (rhombicuboctahedron dual), 24x kite 3,4,4,4 angles 115deg 16', 81deg 34.67'
        A = (81 + 34.67 / 60) / 2
        B = (115 + 16 / 60) / 2
        cosA, sinA = math.cos(math.radians(A)), math.sin(math.radians(A))
        cosB, sinB = math.cos(math.radians(B)), math.sin(math.radians(B))

        # ratio to longer side
        l1 = l * sinB / sinA   # = 1.2929 * l
        le1 = le * l1 / l
        _edge_dwg1 = edgetab_dwg(l1, le1, **faceparamdict)

        #pentagon, 5 side indexed transform list
        trli = [(A, 0, 0, 1), (180 - A, l1 * cosA, -l1 * sinA, 1), (180 + B, l1 * cosA + l * cosB, 0, 0),(-B, l1 * cosA, l1 * sinA, 0)]
        _dwg = transformlist_polygon_indexedges([_edge_dwg0, _edge_dwg1], trli)

    else:
        _dwg = {}

    # pair for easier tiling
    # _dwg = pair_drawing(_dwg, (180, 0.7 * l, 2.4 * l))

    return _dwg

def greatdodec_pair(l, le, **faceparamdict):
    """
    l mm short edge great dodecahedron triangle pair face
    """
    gr = 0.5 * (1 + math.sqrt(5))
    _edge_dwg0 = edgetab_dwg((gr * l), (gr * le),  **faceparamdict)  # long edge gr x length short edge
    _edge_dwg1 = edgetab_dwg(l, le,  **faceparamdict)  # short edges

    #triangle 3 side indexed transform list
    trli = [(0, 0, 0, 0), (180 - 36, gr * l * math.cos(math.radians(36)), -gr * l * math.sin(math.radians(36)), 0), (180 + 72, gr * l, 0, 1)]

    #great dodecahedron triangle_pair face, 2 short sides and one longer side
    _dwg = transformlist_polygon_indexedges([_edge_dwg0, _edge_dwg1], trli)

    # add on 180deg rotation tiled onto above
    _dwg = pair_drawing(_dwg, (180, 0.8 * gr * l , -1.85 * l * math.sin(math.radians(36))))

    return _dwg

def propeller_unit(l, n):
    """
    Equivalents for Tomoko Fuse propeller units

    l mm edge equilateral triangle_pair (this is the 'inner' triangle_pair of the propeller unit)
    :parameter l: eq tri edge length
    :parameter n: number of edges for propeller type 3
    :return [cutlpl, scorelpl] for polyhedron triangle_pair tabbed face
    """

    propeller_type = 3

    ta, if2 = 3, -0.1    # -ve if2 interference used to expand slot for easier fitting

    if propeller_type == 1:  # first, largest variation - 4 units for one octahedron
        #triangle_pair
        a, b, c = l / (2 * math.sqrt(3)), l * math.sqrt(3) / 2, l / math.sqrt(3)  # proportions of edge length l2 of outer triangle_pair
        l2 = a + b + c

        _cut = [[(0,0), (a / 4, 0), ((a / 4) - 1, 1), ((a / 4) - 1.5, ta), (3 * a / 4, ta / 4), (3 * a / 4, 0), (l2, 0)],
                [(c + (0.625 * ((l2 / 2) - c)) + 0.5 * if2, -0.3125 * l - 0.86 * if2), (c + (0.875 * ((l2 / 2) - c)) - 0.5 * if2, -0.4375 * l + 0.86 * if2)],
                [(0.3 + c + (0.625 * ((l2 / 2) - c)) + 0.5 * if2, -0.15 - 0.3125 * l - 0.86 * if2), (0.3 + c + (0.875 * ((l2 / 2) - c)) - 0.5 * if2, -0.15 - 0.4375 * l + 0.86 * if2)]]
        _score = [[(a,0), (a, -l / 2), (a + b, 0)]]
        _edge_dwg = {'cut': _cut, 'score': _score}
        #eq triangle_pair, 3 side transform list
        _dwg = nsided_polygon(_edge_dwg, l2, 3)

        # _dwg = pair_drawing(_dwg, (180, (l2 / 2) + 5, -30))

    elif propeller_type == 2:  #second, intermediate variation - two type 1 edges and one type 3 edge4
        pass
    else:   # type 3 third, smallest variation, one unit per final face i.e. 8 units for octahedron.
        #half internal angle of polygon for translation
        theta_radians = (math.pi - (2 * math.pi / n)) / 2
        a = (l / 2) * math.tan(theta_radians)

        # triangle_pair
        # a = l / (2 * math.sqrt(3))
        # square
        # a = l / 2
        _cut = [[(0,0), (l / 2, a), (l / 2, 3 * a / 4), ((l / 2) + 0.5, (3 * a / 4) + 0.5), ((l / 2) + ta, (3 * a / 4) - 1), ((l / 2) + ta, (a / 4) + 1.3)],
                [((l / 2) + ta, (a / 4) + 1), (l / 2, a / 4), (l / 2, 0), (l, 0)],
                [(l / 2, -(a / 4) - if2), (l / 2, -(3 * a / 4) + if2)],
                [(0.25 + (l / 2), -(3 * a / 4) + if2), (0.25 + (l / 2), -(a / 4) - if2)]]
        _score = [[(0,0), (l / 2, 0)]]
        _edge_dwg = {'cut': _cut, 'score': _score}
        _dwg = nsided_polygon(_edge_dwg, l, n)

        # _dwg = pair_drawing(_dwg, (180, l + 5, -30))

    return _dwg

if __name__ == '__main__':
    testfaceparamdict = {'ta':3.5, 'if2':0.1, 'so':0.25, 've':1.0, 'isl':1.0, 'etc':2.0, 'theta':30}
    print("face_routines.py - printouts of calls")
    # print(quadr_from_point_dxdy((0,0),1,2,1,4,0))
    # print(simple_quadrilateral(6,2,0))
    print(simple_quadrilateral(50, 40, 0))
    # print(round_drawing(square(50, 10, **testfaceparamdict), 1))
    # print(propeller_unit(100, 3))


