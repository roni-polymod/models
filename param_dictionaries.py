import math

from face_routines import triangle_pair, triangle_icos, triangle_nscored_pair, square, \
    pentagon, catalan_polygon, rhombus, \
    rhombus_simple, spherical_segment, triangle_custom_pair, \
    simple_quadrilateral, greatdodec_pair, polygon, propeller_unit, tab_testStrips

#golden ratio for pentagons
GR = (1 + math.sqrt(5))/2

"""
Polygon face routines parameter dictionary for call to edgetab_dwg function in face_routines.py

:param ta: tab thickness. Tabs will have score lines
:param if2: interference distance divided by 2 - to adjust tab interference for cut width
:param so: score offset to give flatter folded edge with score folds level with cuts
:param ve: v taper width to add to edge of tab for end tabs
:param vm: v taper width to add to edge of tab for middle tab
:param isl: incomplete score length, leave an unscored length so that tabs spring back
:param etc: end tab clearance
:param theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
"""
faceparamdict = {'ta': 3.5, 'if2': 0.1, 'so': 0.25, 've': 1.0, 'isl': 1.0, 'etc': 2.0, 'theta': 30, 'tab_type': 1}

"""
Polygon edge strut routine parameter dictionary for call to asym_strut function in strut_routines.py

: param w:  strip half width mm
: param ta:  tab thickness mm
: param tt:  trim tabs LU and RD for width of paper allowance mm
: param ss:  slot sizing parameter 2.0mm seems OK
: param twf:  tab width factor, closer to 1 will narrow widest part of tab. 0.85 seems good - easy insertion but still some lock
"""
strutparamdict = {'w': 7.5, 'ta': 3.0, 'tt': 0.4, 'ss': 2.0, 'twf': 0.85}

"""
Polyhedron parameter dictionary

polyhedron face model parameters for length l, end tab length le, and array spacing col, row params
    l, le, cols, dx, rows, dy

    Custom faces, extra parameters after l, le as follows, see the called function for detail
    5e:  n - for n sided regular polygon
    quad:  w, we - width parameters for quadrialateral section of spherical triangles 
    tr_nscored:  nscored - the number of edges of eq triangle_pair that are scored
    rhombicdodecahedron, rhombohedron, rhomb_tile:  rt - rhombus angle (rhombus theta)
    catalan:  catalan_type - so far pi pentagonal icositetrahedron, di deltoidal icositetrahedron

polyhedron edge model parameters for length l, left and right end strut angles thetaL, thetaR, 
    vertex type platonic archimedean or rhombic P A or R
    and array spacing col, row params l, le, cols, dx, rows, dy

    Rhombohedrons parallelepipeds/dodec/icos/triacontahedron rhombus angle for golden ratio diagonal 63.453 deg
        need combinations of P, R and A vertex edges depending on model
    Pentagonal icositetrahedron (snub cube dual), 24x pentagon 3,3,3,3,4, angles 114deg 48.5', 80deg 46', 
        ratio to longer side = 1.4193, short edge x36, long edge x24
            #_layerl.append(array_objects(asym_strut_lf(l / 1.4193, 7.5, 3, -24.81, -24.81, 'P', 0.4), cols, dx, rows, dy)) # 
            _layerl.append(array_objects(asym_strut_lf(l, 7.5, 3, -24.81, 9.23, 'P', 0.4), cols, dx, rows, dy)) # 

"""
polyhedrondict = {
    'face_cube': {'5e': (square, 50, 10, 3, 58, 2, 58), '5r': (square, 57.74, 12, 3, 65.5, 2, 65.5)},
    'face_tetrahedron': {'5e': (triangle_pair, 50, 10, 3, 66, 2, 52), '5r': (triangle_pair, 81.65, 16, 0, 180, 0, 0)},
    'face_octahedron': {'5e': (triangle_pair, 50, 10, 2, 68, 2, 52), '5r': (triangle_pair, 70.71, 14, 2, 90, 2, 67)},
    'face_icosahedron': {'5e': (triangle_icos, 50, 10, 0, 63.5, 3, 49), '5r': (triangle_icos, 52.57, 10, 0, 68, 0, 49.5)},
    'face_dodecahedron': {'5e': (pentagon, 50, 10, 0, 85, 2, 50 * GR), '5r': (pentagon, 35.68, 8, 2, 1.8 * 35.68 * GR, 3, 35.68 * GR)},
    'face_custom': {'5e': (polygon, 50, 10, 6, 2, 102, 3, 95), 'tr_custom': (triangle_custom_pair, 50, 10, 3, 63.5, 2, 60),
                    'tr_nscored': (triangle_nscored_pair, 50, 10, 1, 2, 63.5, 4, 51.5),  'great_dodec': (greatdodec_pair, 50, 10, 0, 63.5, 0, 60),
                    'simple_quad': (simple_quadrilateral, 50, 60, 0, 0, 0, 0), 'quad': (spherical_segment, 70, 20, 100, 20, 0, 107, 0, 107),
                    'rhombicdodecahedron': (rhombus, 50, 10, 70.53, 3, 54, 4, 50 * 1.2), 'rhombohedron': (rhombus, 50, 10, 63.435, 4, 50, 2, 50 * 1.2),
                    'rhomb_tile': (rhombus_simple, 50, 10, 63.435, 4, 54, 2, 50 * 1.2), 'catalan': (catalan_polygon, 50 / 1.4193, 10 / 1.4193, 'di', 0, 85, 0, 50 * GR + 1),
                    'propeller_unit': (propeller_unit, 57.74, 3, 0, 0, 0, 0), 'test': (tab_testStrips, 50, 10, 15, 4, 51, 3, 20)},
    'edge_cube': {'5e': (50, 0, 0, 'P', 4, 50.5, 3, 18.5), '5r': (57.74, 0, 0, 'P', 0, 58.3, 12, 18.5)},
    'edge_tetrahedron': {'5e': (50, 30, 30, 'P', 4, 50.5, 3, 18.5), '5r': (81.65, 30, 30, 'P', 2, 82, 3, 18.5)},
    'edge_octahedron': {'5e': (50, 30, 30, 'P', 4, 50.5, 3, 18.5), '5r': (70.71, 30, 30, 'P', 0, 71.5, 12, 18.5)},
    'edge_icosahedron': {'5e': (50, 30, 30, 'P', 4, 50.5, 12, 18.5), '5r': (52.57, 30, 30, 'P', 3, 55, 10, 18.5)},
    'edge_dodecahedron': {'5e': (50, -18, -18, 'P', 3, 55.5, 10, 18.5), '5r': (35.67, -18, -18, 'P', 5, 41, 6, 18.5)},
    'edge_archimedean': {'5e': (50, -18, 30, 'A', 2, 101.5, 15, 18.5)},
    'edge_rhombicdodecahedron': {'5e': (50, 19.47, -19.47, 'P', 4, 50.5, 6, 18.5), '5r': (49.54, 19.47, -19.47, 'P', 4, 50.5, 6, 18.5)},
    'edge_rhombohedron': {'5eP': (50, -26.547, 26.547, 'P', 4, 50.75, 3, 18.5), '5eR1': (50, -26.547, 26.547, 'R', 3, 50.75, 2, 18.5), '5eR2': (50, -26.547, 26.547, 'R', 3, 50.75, 2, 18.5)},
    'edge_pentagonal_icositetrahedron': {'5eShort': (50 / 1.4193, -24.81, -24.81, 'P', 6, 42, 6, 18.5), '5eLong': (50, -24.81, 9.23, 'P', 4, 53, 6, 18.5)},
    }
