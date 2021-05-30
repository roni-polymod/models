# svgwrite docs https://svgwrite.readthedocs.io/en/latest/index.html
# docs are for v1.3.2. pip install has installed v1.4
import svgwrite
import param_dictionaries

import math, os, sys, traceback, argparse
from point_routines import translate_drawing, translate_layer, layer_xybounds, merge_drawings, rotate_drawing, pair_drawing
from strut_routines import asym_strut_lf

PROGNAME = sys.argv[0].rstrip('.py')

# IMPORTANT - Scale factor for writing from program lengths to svg file seems to differ in applications???
# Scale factor to mm on beambox laser 100 length in svg without any other measurement is 35.28 mm in beamstudio
SCALE100 = 0.3528   # beam studio
# SCALE100 = 0.2646   # inkscape 0.92 ubuntu

def scale(x, y):
    return (x / SCALE100, y / SCALE100)

def scalei(x, y):
    return (round(x / SCALE100, 2), round(y / SCALE100, 2))

def scalel(l):
    return round(l / SCALE100, 3)

# def draw_layer_dxf(lp, draw_obj):
#     """
#     draw the list of points as line segments to the drawing object
#     old dxf drawing routine, requires sdxf
#     """
#     for i in range(len(lp) - 1):
#         draw_obj.append(sdxf.Line(points=[lp[i], lp[i + 1]], layer="drawinglayer"))

def draw_layer_svg(layer, svg_drawobj, svg_layerobj, stroke_colour, marktoolpath):
    """
    draw each path in layer as line segments to the svg drawing object
     and optionally mark the laser cutter tool path on an addtional layer
    return counts and lengths of cuts and scores - non functional, for info on cutting time/complexity

    :param layer: list of point lists of (x, y) point coordinates. Line drawn from point to point for each sub list
    :param svg_drawobj: svg drawing object
    :param svg_layerobj: svg layer object for drawing lines
    :param stroke_colour: string colour e.g. 'red' for layer colour
    :param marktoolpath: boolean to indicate if a trace of the tool path is also drawn, visualising toolpath is useful
        during optimisation stages to get better laser cut times.
    :return: returns count of number of lines and length of lines
    """
    markpath = []
    nextp = (0, 0)
    jumppath = []
    linecount = sum([(len(path) - 1) for path in layer])
    linelength = 0
    for path in layer:
        # take in reverse order as beambox seems to reverse the order for tool path, for single object
        #  however using array tool in beam studio mixes again, need to resolve this
        for i in range(len(path) - 2, -1, -1):
            linelength += math.sqrt((path[i][0] - path[i + 1][0])**2 + (path[i][1] - path[i + 1][1])**2)
            sp, ep = scalei(path[i][0], path[i][1]), scalei(path[i + 1][0], path[i + 1][1])
            svg_layerobj.add(svg_drawobj.line(start=sp, end=ep, stroke=stroke_colour))
            #store markline list in rev order
            markpath.insert(0, [sp, ep])
            scaledist = math.sqrt((ep[0] - nextp[0])**2 + (ep[1] - nextp[1])**2)
            if scaledist > 15:   #manually adjust this value for limit length at which 'jumps' are drawn in
                jumppath.insert(0, [ep, nextp])
            nextp = sp

    if marktoolpath:
        markfreq = 2
        markLines = svg_drawobj.add(svg_drawobj.g(id='marklines'))
        marker = svg_drawobj.marker(insert=(3, 1.5), size=(3, 3), orient='auto')
        marker.add(svg_drawobj.polygon([(0, 0), (0, 3), (1.5 * 1.732, 1.5)]).fill('green', opacity=0.7))
        svg_drawobj.defs.add(marker)
        markline = markLines.add(svg_drawobj.line(start=markpath[0][0], end=markpath[0][1], stroke='green'))
        markline.set_markers( (marker, None, marker) )
        for i in range(1, len(markpath)):
            if i % markfreq == 0:
                markline = markLines.add(svg_drawobj.line(start=markpath[i][0], end=markpath[i][1], stroke='green'))
                markline.set_markers( (None, None, marker) )
        for i in range(len(jumppath)):
                markline = markLines.add(svg_drawobj.line(start=jumppath[i][0], end=jumppath[i][1], stroke='red', stroke_width='2'))
                markline.set_markers( (None, None, marker) )

    return linecount, linelength

def write_svg_file(filename, sizex, sizey, page_dwg):
    """
    :param filename: file name to write
    :param sizex: str size and unit for svg, x
    :param sizey: str size and unit for svg, y
    :param page_dwg: the page drawing dictionary usually with cut and score object
    :return: none - writes file and message
    """

    dwg = svgwrite.Drawing(filename=filename, size=(sizex, sizey))
    cutLines = dwg.add(dwg.g(id='cutlines'))
    scoreLines = dwg.add(dwg.g(id='scorelines'))

    #draw the point lists to svg object and get counts and lengths of cuts and scores
    layerdict = {'cut' : [cutLines, 'blue'], 'score' : [scoreLines, 'red']}   # index svg layer objects and colours
    print('File : {}, SVG dimension x,y : {}, {}'.format(filename, sizex, sizey))
    for k, layer in page_dwg.items():
        linecount, linelen = draw_layer_svg(layer, dwg, layerdict[k][0], layerdict[k][1], False)
        print(' {} layer : {} lines, {:.0f}cm'.format(k, linecount, linelen/10))

    dwg.save()
    return

def array_objects(dwg: dict, cols, dx, rows, dy):
    """
    create an array copy of the drawing
    in cols columns x rows rows spaced dx and dy respectively
    :parameter cspll: drawing to be arrayed
    :parameter cols: number of columns to copy to
    :parameter dx: repeat length for each col
    :parameter rows: number of rows to copy to
    :parameter dy: repeat length for each row
    """
    if cols == 0:
        _dwg_row = dwg.copy()
    else:
        _dwg_row = {}
        for k, layer in dwg.items():
            _layer = []
            for c in range(0, cols):
                _layer.extend(translate_layer(layer, (dx * c, 0)))
            _dwg_row[k] = _layer

    if rows == 0:
        return _dwg_row

    _dwg_rows = {}
    for k, layer in _dwg_row.items():
        _layer = []
        for r in range(0, rows):
            _layer.extend(translate_layer(layer, (0, dy * r)))
        _dwg_rows[k] = _layer

    return _dwg_rows

def create_face_svg(filename, polyhedron, stkey, polyhedrondict, use_array, faceparamdict):
    """
    :param filename: file name to save
    :param polyhedron: dictionary lookup key for polyhedron
    :param stkey: lookup key size, type and array repeat values for polyhedron
    :param use_array: array repetition of pieces if True, single otherwise
    :param faceparamdict: parameters for face edge tabs, dict read from imported file
    :return: file is written and message printed, also returns the dwg for further processing if reqd
    """

    try:
        # polygon_function for polyhedron face shape and parameters from dictionary
        # special cases, extra parameters dealt with individually
        if polyhedron == 'face_custom':
            if stkey == '5e':  #general 5cm edge polygon, hexagon, octagon, dodecagon for archimedean models
                polygon_func, l, le, n, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, n, **faceparamdict)
            elif stkey == 'simple_quad':
                polygon_func, l, w, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, w, 0)
            elif stkey == 'quad':
                polygon_func, l, le, w, we, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, w, we, **faceparamdict)
            elif stkey == 'tr_nscored':
                polygon_func, l, le, n, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, n, **faceparamdict)
            elif stkey == 'tr_custom':
                polygon_func, l, le, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, **faceparamdict)
            elif stkey == 'great_dodec':
                polygon_func, l, le, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, **faceparamdict)
            elif stkey =='rhombicdodecahedron' or  stkey =='rhombohedron' or stkey =='rhomb_tile':
                polygon_func, l, le, rt, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, rt, **faceparamdict)
            elif stkey =='catalan':
                polygon_func, l, le, catalan_stkey, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, catalan_stkey, **faceparamdict)
            elif stkey =='propeller_unit':
                polygon_func, l, n, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, n)
            elif stkey =='teststrip':
                polygon_func, l, le, w, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
                polygon_dwg = polygon_func(l, le, w, **faceparamdict)

        else:
            polygon_func, l, le, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
            polygon_dwg = polygon_func(l, le, **faceparamdict)

        if use_array:
            page_dwg = array_objects(polygon_dwg, cols, dx, rows, dy)
        else:
            page_dwg = polygon_dwg

        # translate to bring to origin as later versions of beam studio seem to need this
        minx, miny, maxx, maxy = layer_xybounds(page_dwg['cut'])
        page_dwg = translate_drawing(page_dwg, (-minx, -miny))
        sizex = str(round((maxx - minx + 5)/10, 1)) + 'cm'
        sizey = str(round((maxy - miny + 5)/10, 1)) + 'cm'

        write_svg_file(filename, sizex, sizey, page_dwg)

    except Exception as e:
        traceback.print_exc()

    return page_dwg

def create_edge_strut_svg(filename, polyhedron, stkey, polyhedrondict, use_array, strutparamdict):
    """
    :param filename: file name to save
    :param polyhedron: dictionary lookup key for polyhedron
    :param stkey: lookup key size, type and array repeat values for polyhedron
    :param use_array: array repetition of pieces if True, single otherwise
    :param strutparamdict: parameters for strut, dict read from imported file

    :return: file is written and message printed, also returns the dwg for further processing if reqd
    """

    try:
        l, thetaL, thetaR, vertex, cols, dx, rows, dy = polyhedrondict[polyhedron][stkey]
        strut_dwg = asym_strut_lf(l, thetaL, thetaR, vertex, **strutparamdict)

        # pair if needed
        # strut_dwg = pair_drawing(strut_dwg, (180, 2 * l + 0.5, 0))

        if use_array:
            page_dwg = array_objects(strut_dwg, cols, dx, rows, dy)
        else:
            page_dwg = strut_dwg

        # translate to bring to origin and size as later versions of beam studio seem to need this
        minx, miny, maxx, maxy = layer_xybounds(page_dwg['cut'])
        page_dwg = translate_drawing(page_dwg, (-minx, -miny))
        sizex = str(round((maxx - minx + 5)/10, 1)) + 'cm'
        sizey = str(round((maxy - miny + 5)/10, 1)) + 'cm'

        write_svg_file(filename, sizex, sizey, page_dwg)

    except Exception as e:
        traceback.print_exc()

    return page_dwg

def combine_svgs():
    """
    manual set up to combine svgs if wanting to build A4 sheets of combined models
    use this from code, not available from cli
    :return:
    """
    polyhedrondict = param_dictionaries.polyhedrondict
    strutparamdict = param_dictionaries.strutparamdict
    faceparamdict = param_dictionaries.faceparamdict

    # create first page then second then merge before writing file
    # add code for more models and merge for further combination
    # Face combination examples
    _pagedwg = create_face_svg('working/dwg1.svg', 'face_cube', '5e', polyhedrondict, True, faceparamdict)
    _pagedwgadd = create_face_svg('working/dwg2.svg', 'face_icosahedron', '5e', polyhedrondict, True, faceparamdict)
    _pagedwg = merge_drawings(_pagedwg, _pagedwgadd, 0, 2)

    # _pagedwgadd = create_face_svg('working/dwg3.svg', 'face_octahedron', '5r', polyhedrondict, True, faceparamdict)
    # _pagedwg = merge_drawings(_pagedwg, _pagedwgadd, 0, 2)

    # edge combination examples
    # _pagedwg = create_edge_strut_svg('working/dwg1.svg', 'edge_rhombicdodecahedron', '5e', polyhedrondict, True, strutparamdict)
    # _pagedwgadd = create_edge_strut_svg('working/dwg2.svg', 'edge_rhombohedron', '5eR1', polyhedrondict, True, strutparamdict)
    # _pagedwg = merge_drawings(_pagedwg, _pagedwgadd, 0, 2)

    # _pagedwgadd = create_edge_strut_svg('working/dwg3.svg', 'edge_rhombohedron', '5eR2', polyhedrondict, True, strutparamdict)
    # _pagedwg = merge_drawings(_pagedwg, _pagedwgadd, 0, 2)


    minx, miny, maxx, maxy = layer_xybounds(_pagedwg['cut'])
    sizex = str(round((maxx - minx)/10, 1)) + 'cm'
    sizey = str(round((maxy - miny)/10, 1)) + 'cm'
    write_svg_file('working/combined.svg', sizex, sizey, _pagedwg)

    return

def main():
    """
    set up command line arguments and parameter dictionaries to call polygon and svg writing
    """

    # argument parser
    my_parser = argparse.ArgumentParser(description='Write SVG file for polyhedron face or edge models')
    my_parser.add_argument('Polyhedron', metavar='poly', type=str, help='polyhedron name')
    my_parser.add_argument('SizeTypeKey', metavar='stkey', type=str, help='dict key to size, type and repeat parameters')
    my_parser.add_argument('-n', '--filename', action='store', help='relative path and file name to save, (defaults polyhedron name current folder')
    my_parser.add_argument('-a', '--array', action='store_true', help='True for array repetition of pieces, default to single piece')
    my_parser.add_argument('-f', '--face', action='store_true', help='Face model (default)')
    my_parser.add_argument('-e', '--edge', action='store_true', help='Edge model (no effect if -f also used)')

    args = my_parser.parse_args()
    use_array = args.array
    polyhedron = args.Polyhedron
    stkey = args.SizeTypeKey

    if not args.filename:
        filename = polyhedron + '.svg'
    else:
        filename =  args.filename


    polyhedrondict = param_dictionaries.polyhedrondict

    if args.edge and not args.face:
        model = 'edge'
        polyhedron_dict_key = model + '_' + polyhedron
        strutparamdict = param_dictionaries.strutparamdict
        create_edge_strut_svg(filename, polyhedron_dict_key, stkey, polyhedrondict, use_array, strutparamdict)
    else:
        model = 'face'
        polyhedron_dict_key = model + '_' + polyhedron
        faceparamdict = param_dictionaries.faceparamdict
        create_face_svg(filename, polyhedron_dict_key, stkey, polyhedrondict, use_array, faceparamdict)

    return

if __name__ == '__main__':
    # combine_svgs()
    main()


