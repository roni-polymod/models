import math
from point_routines import translate_path, rotate_path

def asym_strut_lf(l, thetaL, thetaR, vertex, w, ta, tt, ss, twf):
    """
    asym_strut with lock flap join
    e.g.  asym_strut_lf(75, 7.5, 3, 30, 30, 'N', 0.3)
    :param l: strip length mm
    :param thetaL: angle from left edge of slope of strut, degrees
    :param thetaR: angle from right edge of slope of strut, degrees
    :param vertex: P = regular platonic polyhedron, A = archimedean, swap LU RD, R = rhombic, RU, LU copy from LD, RD
    :param w: strip half width mm
    :param ta: tab thickness mm
    :param tt: trim tabs LU and RD for width of paper allowance mm
    :param ss: slot sizing parameter 2.0mm seems OK
    :param twf: tab width factor, closer to 1 will narrow widest part of tab. 0.85 seems good - easy insertion but still some lock
    :return dict drawing of cut and score layers

    For symmetrical strut give same value for thetaL and thetaR
    """

    # angles in radians
    thetaLrad = math.radians(thetaL)
    thetaRrad = math.radians(thetaR)
    # offset in x direction for angle theta
    xoffL = w * math.tan(thetaLrad)
    xoffR = w * math.tan(thetaRrad)
    # half slope length used for length of end of slot from edge
    slopeL = w / (math.cos(thetaLrad))
    slopeR = w / (math.cos(thetaRrad))

    slot_path_LU0 = [(slopeL + tt + ss * math.sin(thetaLrad), -ss * math.cos(thetaLrad)),
                    (slopeL + tt + (slopeL - ss) * math.sin(thetaLrad), -(slopeL - ss) * math.cos(thetaLrad))]
    slot_path_RD0 = [(l - slopeR - tt - ss * math.sin(thetaRrad), ss * math.cos(thetaRrad)),
                    (l - slopeR - tt - (slopeR - ss) * math.sin(thetaRrad), (slopeR - ss) * math.cos(thetaRrad))]

    flap_path_LU0 = [(slopeL + tt - (1.5 * ss) + 0.75 * ss * math.sin(thetaLrad), -0.75 * ss * math.cos(thetaLrad)),
                    (slopeL + tt + ss * math.sin(thetaLrad), -ss * math.cos(thetaLrad))]
    flap_path_LU1 = [(slopeL + tt + (slopeL - ss) * math.sin(thetaLrad), -(slopeL - ss) * math.cos(thetaLrad)),
                    (slopeL + tt - (1.5 * ss) + (slopeL - 0.75 * ss) * math.sin(thetaLrad), -(slopeL - 0.75 * ss) * math.cos(thetaLrad))]

    flap_path_RD0 = [(l - slopeR - tt + (1.5 * ss) - 0.75 * ss * math.sin(thetaRrad), 0.75 * ss * math.cos(thetaRrad)),
                    (l - slopeR - tt - ss * math.sin(thetaRrad), ss * math.cos(thetaRrad))]
    flap_path_RD1 = [(l - slopeR - tt - (slopeR - ss) * math.sin(thetaRrad), (slopeR - ss) * math.cos(thetaRrad)),
                    (l - slopeR - tt + (1.5 * ss) - (slopeR - 0.75 * ss) * math.sin(thetaRrad), (slopeR - 0.75 * ss) * math.cos(thetaRrad))]


    # 0.3 break on corner points to anchor in cut sheet
    base_path_0 = [(xoffL + tt, -w), (tt, 0), (0, 0)]
    base_path_1 = [(0, 0), (xoffL, w), (xoffL + ss, w),
                         (xoffL + twf * ss, w + 0.5 * ss), (xoffL + ss, w + ta), (xoffL + slopeL - ss, w + ta),
                         (xoffL + slopeL - twf * ss, w + 0.5 * ss), (xoffL + slopeL - ss, w), (l - xoffR - tt - 0.3, w)]
    base_path_2 = [(l - xoffR - tt, w), (l - tt, 0), (l, 0)]
    base_path_3 = [(l, 0), (l - xoffR, -w), (l - xoffR - ss, -w),
                         (l - xoffR - twf * ss, -w - 0.5 * ss), (l - xoffR - ss, -w - ta), (l - xoffR - slopeR + ss, -w - ta),
                         (l - xoffR - slopeR + twf * ss, -w - 0.5 * ss), (l - xoffR - slopeR + ss, -w), (xoffL + tt + 0.3, -w)]

    score_path_0 = [(0, 0), (l, 0)]
    score_path_LD = [(xoffL + slopeL - ss, w), (xoffL + ss, w)]
    score_path_RU = [(l - xoffR - ss, -w), (l - xoffR - slopeR + ss, -w)]
    score_path_LU = [(slopeL + tt - ss + ss * math.sin(thetaLrad) / 2, -ss * math.cos(thetaLrad) / 2),
                   (slopeL + tt - ss + (slopeL - ss) * math.sin(thetaLrad), -(slopeL - ss) * math.cos(thetaLrad))]
    score_path_RD = [(l - slopeR - tt + ss - ss * math.sin(thetaRrad) / 2, ss * math.cos(thetaRrad) / 2),
                    (l - slopeR - tt + ss - (slopeR - ss) * math.sin(thetaRrad), (slopeR - ss) * math.cos(thetaRrad))]

    if vertex == 'A': # archimedean, swap LU <> RD
        # adjust end points only for baselp 1 and 3
        base_path_1.pop()
        base_path_1.append((l - xoffL - tt - 0.3, w))
        base_path_3.pop()
        base_path_3.append((xoffR + tt + 0.3 , -w))
        # for the rest copy over rotation
        ptemp = base_path_0
        base_path_0 = translate_path(rotate_path(base_path_2, 180), (l, 0))
        base_path_2 = translate_path(rotate_path(ptemp, 180), (l, 0))
        ptemp = slot_path_LU0
        slot_path_LU0 = translate_path(rotate_path(slot_path_RD0, 180), (l, 0))
        slot_path_RD0 = translate_path(rotate_path(ptemp, 180), (l, 0))
        ptemp = flap_path_LU0
        flap_path_LU0 = translate_path(rotate_path(flap_path_RD0, 180), (l, 0))
        flap_path_RD0 = translate_path(rotate_path(ptemp, 180), (l, 0))
        ptemp = flap_path_LU1
        flap_path_LU1 = translate_path(rotate_path(flap_path_RD1, 180), (l, 0))
        flap_path_RD1 = translate_path(rotate_path(ptemp, 180), (l, 0))
        ptemp = score_path_LU
        score_path_LU = translate_path(rotate_path(score_path_RD, 180), (l, 0))
        score_path_RD = translate_path(rotate_path(ptemp, 180), (l, 0))
    elif vertex == 'R':  # rhombic repeat LD, RD to RU, LU by copy over rotation
        base_path_3 = translate_path(rotate_path(base_path_1, 180), (l, 0))
        base_path_0 = translate_path(rotate_path(base_path_2, 180), (l, 0))
        score_path_RU = translate_path(rotate_path(score_path_LD, 180), (l, 0))
        score_path_LU = translate_path(rotate_path(score_path_RD, 180), (l, 0))
        flap_path_LU0 = translate_path(rotate_path(flap_path_RD0, 180), (l, 0))
        flap_path_LU1 = translate_path(rotate_path(flap_path_RD1, 180), (l, 0))
        slot_path_LU0 = translate_path(rotate_path(slot_path_RD0, 180), (l, 0))
    else:  # vertex == 'P' - regular platonic
        pass  # all done above

    _cut = [flap_path_LU1, slot_path_LU0, flap_path_LU0, base_path_3, base_path_2, flap_path_RD1, slot_path_RD0, flap_path_RD0, base_path_1, base_path_0]
    _score = [score_path_LD, score_path_RU, score_path_0]

    return {'cut': _cut, 'score': _score}

if __name__ == '__main__':
    print("strut_routines.py - printouts of calls")



