"""
15/3/20
Paper tool is too thick. Need to advise on using knife blade or find/design other tool to do this
Trapezium coding done to try reverse perspective model
Vee marks on strut ends done, try large size strut for practice instructions, also try different colours to show joins
Check different colours strut joins to see what is blocking vertex of {3 3}

10/3/20
if2=.1 with vevm 0.2 Now working well on platonics, remake the paper tool to help fitting and try on the {3 5}.

Updated tabs yet again for bigger taper in at top of tab to make fitting easier.
Need to test if2 = 0.05, 0.1 for ve vm = 0.2. 0.3 as if2 0 fitted well but was too loose when fitted
Redo the multicolour {3 3/4/5} and {4 3} for one of these fits, as already have the if2=0 set. Also need the {5 3}

Gluing on the way works well even for loose fit if2=0

May have to accept face models are glued rather than non glue

28/02/20
Try test strips with small v on centre tab to see if easier to lock
then try on 50mm triangles for {3 3} {3 4} with different end tab lengths again to see if easy to join

18/02/20
Moved to new project to get rid of old dxf files. Use folder path to write files.

Added parameter to tab test strip so that v width on centre tab can be different (smaller) to end tabs.

12/02/20 - tried if2 = 0.1 try +0.1 on test strips with tool for assembly
75mm triangles for {3 3} {3 4}
50 and 75 mm for rhom dodec

31/1/20 Done astruts fit allowance for slots - try 3 edge vertices again
    Now also done trim of long edge of tab tt2 to reduce fit interference *** try out different tt2 settings for 3 edge vertex - 0.3 and 0.5 tt for {3,3} and {4,3}
    - then remake the rhomb dodec and cube
        ** Still to do astrut with asymettry on sides as well as ends
    tt2 = 0.5 works ok for {3, 3} {4, 3} but need to ensure it does not become too loose for {3, 4} and {3, 5}

    For now just try different interference and longer end tab - redesign slotting in
    Have completed {3, 4} {5, 3} 2mm tab with longer (10mm) end tab length is OK a bit loose on interference so need to experiment with this -
    Try for {3, 3} {3, 4} {3, 5} and {5, 3} again with tighter fit - if2 = 0 is too loose - trying +0.1

    ....Start working need to start making white shapes and multicolour shapes and costing time.


To run at IoM copy this code to repl.it

July 2019
still to try with birch ply (0,8mm thick)
tabbed to 'press' together with tabs only allowing for thickness, in
this case 0.8mm and tab length to allow small overlap to interfere and
therefore lock together

Nov 2019
To make - vary colours:
0a - test struts with longer (0.5mm vs old 0.3mm) lock length, try 3 and 4 vertex
 - need more testing on this
 - 0b - redo tetrahedron with top tab reduced to help with interference when assembling. Not usually a problem with more than 3 vertex or with larger vertex angles
1 - cube
2a/b - dodecahedron - a full size, b reduced to match icosahedron - divide by 1.618 approx 50mm length
3 - rhombic triacontahedron

0b - test tabs with different interferences then use the best settings for
4 - triangle tabbed - x 12 for tetrahedron and octahedron
5 - square tabbed - x 6 for cube
later 6 - dodecahedron - need to sort function to draw tabs

Jan 2020 - trying variations on slots also want a version of asymetric slots with asymmetry on each side as well as
at ends to allow archmedian polyhedrons.

If new slot works then adapt to triangles and try out

Small laser settings - Red cut - power 95% speed 100%
Blue score  - power 10% speed 50%
Large laser settings - Red cut - power 47% speed 100%
Blue score  - power 5% speed 50%
4 Dec - needing power 100% speed 80% and score 20% 50% to get cuts OK - laser head seems higher than 0.2mm z??
Red card did not cut through need even higher power.
z = 0.2mm - important to keep this to the paper thickness and adjust power/speed otherwise
  laser will be out of focus

Time to cut 23x75mm astruts = 2mins 40secs
50 struts approx 5 mins
 - feels slow need to compare with large laser, higher speed 5

Large laser - 12x50mm tabbed triangles approx 2 mins
"""

import sdxf
import math


def translate_coordlist(lp, v):
    """
    translate a list of points lp by the vector v
    """
    lpt = []
    for p in lp:
        lpt.append((p[0] + v[0], p[1] + v[1]))
    return lpt


def rotate_coordlist(lp, theta):
    """
    rotate a list of points lp by the angle theta, anticlockwise
    theta in degrees is converted to radians inside the function
    """
    theta = math.radians(theta)
    lpt = []
    for p in lp:
        lpt.append((p[0] * math.cos(theta) - p[1] * math.sin(theta), p[0] * math.sin(theta) + p[1] * math.cos(theta)))
    return lpt


def draw_coordlist(lp, draw_obj):
    """
    draw the list of points as line segments to the drawing object
    """
    for i in range(len(lp) - 1):
        draw_obj.append(sdxf.Line(points=[lp[i], lp[i + 1]], layer="drawinglayer"))


def draw_tab_testStrips(x, y, l, le, ta, if2, ve, vm, theta):
    """
    call eg      draw_tab_testStrips(0, 0, 50, 10, 3, 0.1, 0.5, 0.25, 30)
    draw a pair of test strips - 50mm width, 15mm height with folded tabs
    x, y: coords of top left point of strip
    l: test strip length
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    box_width = 15
    box_points = [(x, y), (x, y - box_width), (x + l, y - box_width), (x + l, y)]
    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, box_points, score1_points, score2_points]

    for p in lp:
        draw_coordlist(p, d)

    for p in lp:
        draw_coordlist(translate_coordlist(p, (l + 5, 0)), d)


def draw_triangle(x, y, ta, if2, aw2):
    """
    draw a pair of triangles - 50mm width
    x, y: coords of top left point of strip
    ta: thickness allowance mm for material = depth of castellation
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    aw2: taper angle width divided by 2 - to give taper to edge of tab
    """
    # 50mm edge eq triangle at x, y
    # final '(50, 0)' is correction to cut to the tab that this line will meet
    base_linePoints = [(0, 0), (12.5 - if2 + aw2, 0), (12.5 - if2 - aw2, ta), (25.0 + if2 + aw2, ta),
                       (25.0 + if2 - aw2, 0), (37.5 - if2 + aw2, 0), (37.5 - if2 - aw2, ta), (50, ta), (50, 0)]

    linePoints0 = translate_coordlist(rotate_coordlist(base_linePoints, 180), (50 + x, y))
    linePoints1 = translate_coordlist(rotate_coordlist(base_linePoints, 60), (x, y))
    linePoints2 = translate_coordlist(rotate_coordlist(base_linePoints, -60), (25 + x, 25 * math.sqrt(3) + y))

    lp = [linePoints0, linePoints1, linePoints2]

    for p in lp:
        draw_coordlist(p, d)

    # duplicate triangle translated by 60,0
    for p in lp:
        draw_coordlist(translate_coordlist(p, (60, 0)), d)


def draw_triangle_tabbed(x, y, l, le, ta, if2, ve, vm, theta):
    """
    draw tabbed triangle, with score for tab folds - l mm width
    x, y: coords of top left point of strip
    l: edge length
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    # lmm edge eq triangle at x, y

    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, score1_points, score2_points]

    for p in lp:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180), (l + x, y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 60), (x, y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, -60), ((l / 2) + x, (l / 2) * math.sqrt(3) + y)), d)


def draw_square_tabbed(x, y, l, le, ta, if2, ve, vm, theta):
    """
    x, y: coords of top left point of strip
    l: edge length
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    # lmm edge square at x, y

    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, score1_points, score2_points]

    for p in lp:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180), (l + x, y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 90), (x, y)), d)
        draw_coordlist(translate_coordlist(p, (x, l + y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 270), (l + x, l + y)), d)


def draw_trapezoid_tabbed(x, y, h, lb, lt, le, ta, if2, ve, vm, theta):
    """
    trapezium to experiement with reverse perspective cubes
    x, y: coords of top left point of strip
    h: height
    lb: bottom edge length
    lt: top edge length
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    # lb lt, h mm edge trapezoid at x, y

    #bottom and diagonal 'edge' lengths and angle of triangular side of trapezium
    tb = (lb - lt)/2
    td = math.sqrt(math.pow(h, 2) + math.pow(tb, 2))
    ttheta = math.atan(h / tb) * 360 / (2 * math.pi)
    lpb = base_score_pointsList(0, 0, lb, 10, 3, 0.1, 0.2, 0.2, 30)
    lpt = base_score_pointsList(0, 0, lt, 10, 3, 0.1, 0.2, 0.2, 30)
    lps = base_score_pointsList(0, 0, td, 10, 3, 0.1, 0.2, 0.2, 30)

    for p in lpb:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180), (lb + x, y)), d)
    for p in lpt:
        draw_coordlist(translate_coordlist(p, (x + tb, h + y)), d)
    for p in lps:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, ttheta), (x, y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, -ttheta), (lt + tb + x, h + y)), d)


def base_score_pointsList(x, y, l, le, ta, if2, ve, vm, theta):
    """
    Helper routine to return base and score lines for a tabbed edge
    x, y: coords of top left point of strip
    l: edge length
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, score1_points, score2_points]
    return lp


def draw_rhombus_tabbed(x, y, l, le, rt, ta, if2, ve, vm, theta):
    """
    draw rhombus  - l mm edge
    x, y: coords of top left point of strip
    l : edge length
    rt: rhombus theta - first internal angle of rhombus - see Cundy and Rollett
        rhombic dodecahedron = 70.53 deg, rhombic triacontahedron = 63.43
    x, y: coords of top left point of strip
    le: length of end tab
    ta: tab thickness. Need a score line for tabs as well
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    ve: v taper width to add to edge of tab for end tabs
    vm: v taper width to add to edge of tab for middle tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    # l mm edge rhombus at x, y

    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, score1_points, score2_points]

    for p in lp:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180), (l + x, y)), d)
        draw_coordlist(rotate_coordlist(p, rt), d)
        draw_coordlist(translate_coordlist(p, (l * math.cos((rt / 360) * (2 * math.pi)), l * math.sin((rt / 360) * (2 * math.pi)))), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180 + rt), (l * (1 + math.cos((rt / 360) * (2 * math.pi))), l * math.sin((rt / 360) * (2 * math.pi)))), d)


def draw_pentagon_tabbed(x, y, l, le, ta, if2, ve, vm, theta):
    """
    draw tabbed pentagon - l mm edge
    x, y: coords of top left point of strip
    l : edge length
    ta: thickness allowance mm for material = depth of castellation
    if2: interference distance divided by 2 - to make top tab width greater than slot width
    v: v taper width - to give v taper to add to edge of tab
    theta: end tab angle, chamfer angle on end tab to prevent interference when fitted
    """
    # lmm edge square at x, y

    base_linePoints1 = [(x, y), (x + le - if2, y), (x + le - if2 - ve, y + 1), (x + le - if2 + (2 * ve), y + ta),
                        (x + (l / 2) - 0.3 + if2 - (2 * vm), y + ta)]
    base_linePoints2 = [(x + (l / 2) + if2 - (2 * vm), y + ta), (x + (l / 2) + if2 + vm, y + 1), (x + (l / 2) + if2, y),
                        (x + (l - le) - if2, y), (x + (l - le) - if2 - ve, y + 1), (x + (l - le) - if2 + (2 * ve), y + ta),
                        (x + l - 0.3 - (ta * math.tan((theta / 360) * (2 * math.pi))), y + ta), (x + l - 0.3, y),
                        (x + l, y)]

    score1_points = [(x + le - if2, y), (x + (l / 2) + if2, y)]
    score2_points = [(x + (l - le) - if2, y), (x + l, y)]

    lp = [base_linePoints1, base_linePoints2, score1_points, score2_points]

    for p in lp:
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 180), (l + x, y)), d)
        draw_coordlist(rotate_coordlist(p, 108), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, -108), (l * (1 + math.cos((72 / 360) * (2 * math.pi))) + x, l * math.sin((72 / 360) * (2 * math.pi)) + y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, 36), (-l * math.cos((72 / 360) * (2 * math.pi)) + x, l * math.sin((72 / 360) * (2 * math.pi)) + y)), d)
        draw_coordlist(translate_coordlist(rotate_coordlist(p, -36), ((l / 2) + x, l * (math.sin((72 / 360) * (2 * math.pi)) + math.sin((36 / 360) * (2 * math.pi))) + y)), d)


def draw_asym_strut(x, y, l, w, theta1, theta2, ll, tt, tt2, fa):
    """
    draw asymmetrical strut with fold down centre of length
    e.g.  draw_asym_strut(0, 0, 75, 6, 30, 30, 0.5, 0.3, 0.5, 0.5)
    x, y: coords of top mid point of strip - currently not being used
    l: strip length
    w: strip half width
    theta: angle from top edge of slope of strut - see dxf
    ll: lock length. 0=simple straight slit. >0 indicates length of lock 'kink' in slit
      ll must be some sensible value, small in comparison to hhalf
    tt: trim tab. Shave off end of tab to remove interference when fitted
    tt2: trim second tab, only needed for 3vertex with small vertex angle e.g. tetrahedron to
      reduce interference during assembly. Only need one of these at each vertex. Set to 0 otherwise
      For tetrahedron do 3 edges with tt2 and 3 without
    fa: fit allowance - move end of slot nearer to edge for easier fitting whilst assembling. End of slots closer to
      sides will make assembly matchup easier but final position will depend on inner end of slot and lock

    For symmetrical strut give same value for theta1 and theta2
    """
    # offset in x direction for angle theta
    xoff1 = w * math.tan((theta1 / 360) * (2 * math.pi))
    xoff2 = w * math.tan((theta2 / 360) * (2 * math.pi))
    fax = fa * math.tan((theta1 / 360) * (2 * math.pi))
    # half length of hypotenuse
    hhalf1 = w / (math.cos((theta1 / 360) * (2 * math.pi)) * 2)
    hhalf2 = w / (math.cos((theta2 / 360) * (2 * math.pi)) * 2)
    # without break: base_linePoints = [(0, 0), (xoff, w), (l - xoff, w),(l, 0), (l - xoff, -w), (xoff, -w), (0, 0)]
    # with 0.3mm break on corner points
    if tt2 == 0:
        base_linePoints1 = [(xoff1, -w), (0, 0), ((xoff1 / 2) + fax, (w / 2) + fa), ((xoff1 / 2) + fax + tt, (w / 2) + fa), (xoff1 + tt, w),
                            (l - xoff2 - 0.3, w)]
        base_linePoints2 = [(l - xoff2, w), (l, 0), (l - (xoff2 / 2) - fax, -w / 2 - fa), (l - (xoff2 / 2) - fax - tt, -w / 2 - fa),
                            (l - xoff2 - tt, -w), (xoff1 + 0.3 + tt2, -w)]
    else:
        base_linePoints1 = [(xoff1 + tt2, -w), (tt2, 0), (0, 0), ((xoff1 / 2) + fax, (w / 2) + fa), ((xoff1 / 2) + fax + tt, (w / 2) + fa),
                            (xoff1 + tt, w), (l - xoff2 - 0.3 - tt2, w)]
        base_linePoints2 = [(l - xoff2 - tt2, w), (l - tt2, 0), (l, 0), (l - (xoff2 / 2) - fax, -w / 2 - fa), (l - (xoff2 / 2) - fax - tt, -w / 2 - fa),
                            (l - xoff2 - tt, -w), (xoff1 + 0.3 + tt2, -w)]
    scoreline = [(0, 0), (l, 0)]

    if ll == 0:
        slotline1 = [(xoff1 / 2, w / 2), ((xoff1 / 2) + hhalf1, w / 2)]
        slotline2 = [(xoff1 / 2 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w / 2),
                     (xoff1 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w)]
        slotline3 = [(xoff2 / 2, w / 2), ((xoff2 / 2) + hhalf2, w / 2)]
        slotline4 = [(xoff2 / 2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w / 2),
                     (xoff2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w)]
    else:
        xint1 = hhalf1 + (xoff1 / 2) * (hhalf1 - ll) / hhalf1
        yint1 = (w / 2) * (hhalf1 - ll) / hhalf1
        # pre fa -> slotline1 = [(xoff1 / 2, w / 2), (xint1, yint1), ((xoff1 / 2) + hhalf1, w / 2)]
        # slotline2 = [(xoff1 / 2 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w / 2),
        #              (ll + xoff1 / 2 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w / 2),
        # #              (xoff1 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w)]
        # slotline3 = [(xoff2 / 2, w / 2), (xint2, yint2), ((xoff2 / 2) + hhalf2, w / 2)]
        # slotline4 = [(xoff2 / 2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w / 2),
        #              (ll + xoff2 / 2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w / 2),
        #              (xoff2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w)]
        slotline1 = [((xoff1 / 2) + fax + tt, (w / 2) + fa), (xint1, yint1), ((xoff1 / 2) + hhalf1, w / 2)]
        slotline2 = [(xoff1 / 2 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w / 2),
                     (ll + xoff1 / 2 + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w / 2),
                     (xoff1 - fa + w / (2 * math.cos((theta1 / 360) * (2 * math.pi))), -w)]
        xint2 = hhalf2 + (xoff2 / 2) * (hhalf2 - ll) / hhalf2
        yint2 = (w / 2) * (hhalf2 - ll) / hhalf2
        slotline3 = [((xoff2 / 2) + fax + tt, (w / 2) + fa), (xint2, yint2), ((xoff2 / 2) + hhalf2, w / 2)]
        slotline4 = [(xoff2 / 2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w / 2),
                     (ll + xoff2 / 2 + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w / 2),
                     (xoff2 - fa + w / (2 * math.cos((theta2 / 360) * (2 * math.pi))), -w)]

    slottrans1 = translate_coordlist(rotate_coordlist(slotline3, 180), (l, 0))
    slottrans2 = translate_coordlist(rotate_coordlist(slotline4, 180), (l, 0))

    lp = [base_linePoints1, base_linePoints2, scoreline, slotline1, slotline2, slottrans1, slottrans2]

    for p in lp:
        draw_coordlist(p, d)


def draw_vee_marks(x, y, l, w, theta1, theta2):
    """
    draw vee mark next to slots on struts. Mainly for large demo struts
    so user can practice getting the right order.
    """

    # offset in x direction for angle theta
    xoff1 = w * math.tan((theta1 / 360) * (2 * math.pi))
    xoff2 = w * math.tan((theta2 / 360) * (2 * math.pi))
    # half length of hypotenuse
    hhalf1 = w / (math.cos((theta1 / 360) * (2 * math.pi)) * 2)
    hhalf2 = w / (math.cos((theta2 / 360) * (2 * math.pi)) * 2)

    # **** HERE - first vee is OK need to do the other 4 corners and try on asymetric strut
    vee_Points1 = [(xoff1 + hhalf1 / 8, -w + hhalf1 / 2), (xoff1 + hhalf1 / 4, -w + hhalf1 / 4), (xoff1 + 3 * hhalf1 / 8, -w + hhalf1 / 2)]
    vee_Points2 = translate_coordlist(rotate_coordlist(vee_Points1, 180), (l, 0))

    lp = [vee_Points1, vee_Points2]

    for p in lp:
        draw_coordlist(p, d)



if __name__ == '__main__':
    # sdxf drawing object
    d = sdxf.Drawing()

    # f = 'dxffiles/tab_test_vmvept1to3ifpt1.dxf'    # filename
    # if2 = 0.1
    # for i in range(1,4):
    #     ve = i / 10
    #     vm = i / 10
    #     draw_tab_testStrips(0, 20 * (i - 1), 50, 10, 3, if2, ve, vm, 30)

    # f = 'dxffiles/tab_test_vmpt3.dxf'    # filename
    # draw_tab_testStrips(0, 0, 50, 10, 3, 0.1, 0.5, 0.3, 30)

    # f = 'dxffiles/triangle_tab_test50_if1_vevmpt2.dxf'    # filename
    # draw_triangle_tabbed(0, 0, 50, 10, 3, 0.1, 0.2, 0.2, 30)
    # f = 'dxffiles/square_tab_test50_if1_vevmpt2.dxf'    # filename
    # draw_square_tabbed(0, 0, 50, 10, 3, 0.1, 0.2, 0.2, 30)
    f = 'dxffiles/trapezium_tab_test5_if1_vevmpt2.dxf'    # filename
    draw_trapezoid_tabbed(0, 0, 50, 60, 45, 10, 3, 0.1, 0.2, 0.2, 30)
    # f = 'dxffiles/pent_tab_test50_if1_vevmpt2.dxf'    # filename
    # draw_pentagon_tabbed(0, 0, 50, 10, 3, 0.1, 0.2, 0.2, 30)
    # f = 'rhombus_tab_test75_if0_1.dxf'    # filename
    # draw_rhombus_tabbed(0, 0, 75, 70.53, 3, 0.1, 0.5, 30)

    # draw_strut(0, 0, 75, 6, 30, 0.5, 0.3)

    # rhombic dodecahedron uses rhombus with diagonal ratio sqrt(2), 24 edges needed
    # angles from Cundy Rollett theta1 = 19.47, theta2 = -19.47
    # f = 'strut_rhombdodec75.dxf'    # filename
    # draw_asym_strut(0, 0, 75, 6, 19.47, -19.47, 1.0, 0.5, 0.3, 0.5)
    # rhombic triacontahedron uses rhombus with diagonal golden ratio 1.618, 60 edges needed
    # angles from Cundy Rollett theta1 = 26.57, theta2 = -26.57
    # draw_asym_strut(0, 0, 75, 6, 26.57, -26.57, 0.3, 0.3)
    # f = 'strut_trtt2_3.dxf'    # filename
    # draw_asym_strut(0, 0, 75, 6, 30, 30, 1.0, 0.5, 0.3, 0.5)
    # f = 'dxffiles/strut_largDemo.dxf'    # filename
    # draw_asym_strut(0, 0, 50, 15, 30, 30, 2.0, 0.5, 0.3, 1.0)
    # draw_vee_marks(0, 0, 50, 15, 30, 30)
    d.saveas(f)
