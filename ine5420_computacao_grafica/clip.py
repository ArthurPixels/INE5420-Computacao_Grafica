from ine5420_computacao_grafica.base_forms import Point2D, Line, Polygon

############# POINT CLIPPING #####################
# clips a point checking if it is inside the window or not
def pointClip(point: Point2D):
    if point.x <= 1 and point.x >= -1 and point.y <= 1 and point.y >= -1: return point
    else: return None


############# COHEN-SUTHERLAND Line Clipping #####################
# Type OutCode
# INSIDE = 0  // 0000
# LEFT   = 1  // 0001
# RIGHT  = 2  // 0010
# BOTTOM = 4  // 0100
# TOP    = 8  // 1000

# compute the OutCode of a point
def computeOutCode(point: Point2D, xmin, ymin, xmax, ymax):
    code = 0
    if point.x < xmin:
        code |= 1
    elif point.x > xmax:
        code |= 2
    if point.y < ymin:
        code |= 4
    elif point.y > ymax:
        code |= 8

    return code


# clips a line using Cohen-Sutherland
def cohenSutherlandClip(line: Line):
    p0 = line.start
    p1 = line.end

    codeP0 = computeOutCode(p0, -1, -1, 1, 1)
    codeP1 = computeOutCode(p1, -1, -1, 1, 1)

    if not(codeP0 | codeP1):
        # TOTALMENTE CONTIDA
        return line
    elif (codeP0 & codeP1):
        # TOTALMENTE FORA DA JANELA
        return None
    else:
        # PARCIALMENTE CONTIDA (CALCULAR CLIP PARA OS DOIS PONTOS)
        if p1.x == p0.x:
            y0 = p0.y
            y1 = p1.y
            if p1.y > 1: y1 = 1
            elif p1.y < -1: y1 = -1
            if p0.y < -1: y0 = -1
            elif p0.y > 1: y0 = 1
            return Line(Point2D(p0.x, y0), Point2D(p1.x, y1))

        m = (p1.y-p0.y)/(p1.x-p0.x)

        if codeP0:
            p0 = calculateCSInterception(p0, codeP0, m, -1, 1, -1, 1)

        if p0 and codeP1:
            p1 = calculateCSInterception(p1, codeP1, m, -1, 1, -1, 1)

        if not(p0) or not(p1):
            return None
        else:
            return Line(p0, p1)


# calculates a new point over the window based on the coordinates and region code
def calculateCSInterception(p: Point2D, regionCode, m, xe, xd, yf, yt):
    new_y = None
    new_x = None

    if regionCode & 1: # LEFT
        new_x = xe
        new_y = m * (xe - p.x) + p.y
        if new_y <= yt and new_y >= yf:
            return Point2D(new_x, new_y)

    if regionCode & 2: # RIGHT
        new_x = xd
        new_y = m * (xd - p.x) + p.y
        if new_y <= yt and new_y >= yf:
            return Point2D(new_x, new_y)

    if regionCode & 4: # BOTTOM
        new_x = p.x + 1/m * (yf - p.y)
        new_y = yf
        if new_x <= xd and new_x >= xe:
            return Point2D(new_x, new_y)

    if regionCode & 8: # TOP
        new_x = p.x + 1/m * (yt - p.y)
        new_y = yt
        return Point2D(new_x, new_y)


####################### NICHOLL-LEE-NICHOLL 2D Line Clipping #################################
# returns the type of region of a point in the plan
def getAngularCoeficients(p1: Point2D, p2: Point2D):
    TL = float(1-p1.y) / float(-1-p1.x)
    TR = float(1-p1.y) / float(1-p1.x)
    BR = float(-1-p1.y) / float(1-p1.x)
    BL = float(-1-p1.y) / float(-1-p1.x)
    M = float(p2.y-p1.y) / float(p2.x-p1.x)

    return TL, TR, BR, BL, M


# clips the line (P1, P2) when P1 is in the center of the window
def clipCenter(start_point: Point2D, end_point: Point2D):
    x1 = start_point.x
    y1 = start_point.y

    TL, TR, BR, BL, M = getAngularCoeficients(start_point, end_point)

    if (end_point.x > start_point.x):  # P2 is at the right of P1
        if M >= TR:  # TOP BORDER
            y2 = 1
            x2 = (y2-y1) / M + x1

        elif BR <= M and M < TR:  # RIGHT BORDER
            x2 = 1
            y2 = (x2-x1) * M + y1

        elif M < BR:  # BOTTOM BORDER
            y2 = -1
            x2 = (y2-y1) / M + x1

    else:
        if M < TL:  # TOP BORDER
            y2 = 1
            x2 = (y2-y1) / M + x1

        elif TL <= M and M < BL:  # LEFT BORDER
            x2 = -1
            y2 = M * (x2-x1) + y1

        elif M >= BL:  # BOTTOM BORDER
            y2 = -1
            x2 = (y2-y1) / M + x1

    return Line(Point2D(x1, y1), Point2D(x2, y2))


# clips the line (P1, P2) when P1 is in an edge region relative to the window
def clipEdge(start_point: Point2D, end_point: Point2D):
    y2 = end_point.y
    x2 = end_point.x

    TL, TR, BR, BL, M = getAngularCoeficients(start_point, end_point)

    # calculate LEFT border interception (general case)
    x1 = -1
    y1 = end_point.y - M * (end_point.x - x1)

    if M > TR:  # LEFT or TOP-LEFT
        if end_point.y >= 1:  # intercepts the TOP border too
            y2 = 1
            x2 = (y2-y1) / M + x1

    elif M <= BR:  # LEFT or BOTTOM-LEFT
        if end_point.y <= -1:  # intercepts the BOTTOM border too
            y2 = -1
            x2 = (y2-y1) / M + x1

    else:  # LEFT or LEFT-RIGHT
        if end_point.x >= 1:  # intercepts the RIGHT border too
            x2 = 1
            y2 = (x2-x1) * M + y1

    return Line(Point2D(x1, y1), Point2D(x2, y2))


# clips the line (P1, P2) when P1 is in a corner edge region relative to the window
def clipCorner(start_point: Point2D, end_point: Point2D):
    x2 = end_point.x
    y2 = end_point.y

    TL, TR, BR, BL, M = getAngularCoeficients(start_point, end_point)

    if TL < BR:  # case 1 (predominantly bottom)
        if M < TL:  # LEFT or LEFT-BOTTOM
            x1 = -1
            y1 = end_point.y - M * (end_point.x - x1)

            if end_point.y <= -1:  # intercepts BOTTOM border too
                y2 = -1
                x2 = (y2-y1) / M + x1

        else:
            y1 = 1
            x1 = end_point.x - (end_point.y - y1) / M

            if M >= BR:  # TOP or TOP-RIGHT
                if end_point.x >= 1:
                    x2 = 1
                    y2 = (x2-x1) * M + y1

            else:  # TOP or TOP-BOTTOM
                if end_point.y <= -1:
                    y2 = -1
                    x2 = (y2-y1) / M + x1

    else:  # case 2 (predominantly right)
        if M >= TL:  # TOP or TOP-RIGHT
            y1 = 1
            x1 = end_point.x - (end_point.y - y1) / M

            if end_point.x >= 1:
                x2 = 1
                y2 = (x2-x1) * M + y1

        else:
            x1 = -1
            y1 = end_point.y - M * (end_point.x - x1)

            if M <= BR:  # LEFT or LEFT-BOTTOM
                if end_point.y <= -1:  # intercepts BOTTOM border too
                    y2 = -1
                    x2 = (y2-y1) / M + x1

            else:  # LEFT or LEFT-RIGHT
                if end_point.x >= 1:  # intercepts the RIGHT border too
                    x2 = 1
                    y2 = (x2-x1) * M + y1


    return Line(Point2D(x1, y1), Point2D(x2, y2))


# clips a line using Nicholl-Lee-Nicholl algorithm
def nichollLeeNichollClip(line: Line):
    p1 = line.start
    p2 = line.end

    codeP1 = computeOutCode(p1, -1, -1, 1, 1)
    codeP2 = computeOutCode(p2, -1, -1, 1, 1)

    if (codeP1 | codeP2) == 0:  # trivially accepted
        return line
    elif (codeP1 & codeP2) > 0: # trivially rejected
        return None

    if p1.x == p2.x:  # to prevent division by zero error
        x1 = p1.x
        x2 = p2.x
        y1 = p1.y
        y2 = p2.y

        if p1.y > 1:
            y1 = 1
        elif p1.y < -1:
            y1 = -1
        if p2.y > 1:
            y2 = 1
        elif p2.y < -1:
            y2 = -1

        return Line(Point2D(x1, y1), Point2D(x2, y2))


    if codeP1 == 0:  # CENTER
        clipped = clipCenter(p1, p2)

    elif codeP1 == 1:  # LEFT
        clipped = clipEdge(p1, p2)

    elif codeP1 == 2:  # RIGHT (-x, y)
        p1_aux = Point2D(-p1.x, p1.y)
        p2_aux = Point2D(-p2.x, p2.y)
        clipped = clipEdge(p1_aux, p2_aux)
        clipped.start.x *= -1
        clipped.end.x *= -1

    elif codeP1 == 4:  # BOTTOM (y, x)
        p1_aux = Point2D(p1.y, p1.x)
        p2_aux = Point2D(p2.y, p2.x)
        clipped = clipEdge(p1_aux, p2_aux)

        temp = clipped.start.x
        clipped.start.x = clipped.start.y
        clipped.start.y = temp
        temp = clipped.end.x
        clipped.end.x = clipped.end.y
        clipped.end.y = temp

    elif codeP1 == 8:  # TOP (-y, x)
        p1_aux = Point2D(-p1.y, p1.x)
        p2_aux = Point2D(-p2.y, p2.x)
        clipped = clipEdge(p1_aux, p2_aux)

        temp = clipped.start.x
        clipped.start.x = clipped.start.y
        clipped.start.y = -temp
        temp = clipped.end.x
        clipped.end.x = clipped.end.y
        clipped.end.y = -temp

    elif codeP1 == 5:  # LEFT-BOTTOM (x, -y)
        p1_aux = Point2D(p1.x, -p1.y)
        p2_aux = Point2D(p2.x, -p2.y)
        clipped = clipCorner(p1_aux, p2_aux)
        clipped.start.y *= -1
        clipped.end.y *= -1

    elif codeP1 == 6:  # RIGHT-BOTTOM (-x, -y)
        p1_aux = Point2D(-p1.x, -p1.y)
        p2_aux = Point2D(-p2.x, -p2.y)
        clipped = clipCorner(p1_aux, p2_aux)
        clipped.start.x *= -1
        clipped.end.x *= -1
        clipped.start.y *= -1
        clipped.end.y *= -1

    elif codeP1 == 9:  # TOP-LEFT
        clipped = clipCorner(p1, p2)

    else:  # TOP-RIGHT (-x, y)
        p1_aux = Point2D(-p1.x, p1.y)
        p2_aux = Point2D(-p2.x, p2.y)
        clipped = clipCorner(p1_aux, p2_aux)
        clipped.start.x *= -1
        clipped.end.x *= -1

    return clipped


####################### WEILER-ATHERTON Polygon Clipping #################################
# returns the points list ordered clockwise starting from the left-most
def getOrderedPoints(polygon: Polygon):
    # leftmost and uppermost point identification
    leftmostPoint = 0
    leftmost = polygon.points[0].x
    leftmost_y = polygon.points[0].y
    for i in range(1, len(polygon.points)):
        point = polygon.points[i]
        if point.x < leftmost or (point.x == leftmost and point.y > leftmost_y):
            leftmostPoint = i
            leftmost = point.x
            leftmost_y = point.y

    # orientation test
    previous = leftmostPoint-1
    next = leftmostPoint+1
    if previous < 0:
        previous = len(polygon.points)-1
    if next == len(polygon.points):
        next = 0

    p = polygon.points[leftmostPoint]
    pp = polygon.points[previous]
    np = polygon.points[next]

    if pp.x == p.x:
        if np.x < p.x: orientation = -1
        else: orientation = 1
    elif np.x == p.x:
        if pp.x < p.x: orientation = 1
        else: orientation = -1
    else:
        m0 = (np.y - p.y) / (np.x - p.x)
        m1 = (pp.y - p.y) / (pp.x - p.x)

        if m0 > m1:
            orientation = 1
        else:
            orientation = -1

    # reordering
    points = []
    for i in range(len(polygon.points)):
        index = (i*orientation + leftmostPoint) % len(polygon.points)
        points.append(polygon.points[index])

    return points


# verifies if a point already exists in a list before inserting it
def insertPoint(lista: list, point: Point2D, index: int):
    if point in lista: return

    lista.insert(index, point)


# mark all points in a list not visited to execute weiler-atherton algorithm
def markUnvisited(lista: list):
    for point in lista:
        point.visited = False


# clips a polygon (filled or not) using Weiler-Atherton algorithm
# POINT TYPES
# 0 : undefined
# 1 : IN
# 2 : OUT
######################
def weilerAthertonPolygonClip(polygon: Polygon):
    polygon = Polygon([Point2D(-2,0.75),
                        Point2D(-2,-0.75),
                        Point2D(0,-0.75),
                        Point2D(0,-0.25),
                        Point2D(-1.5,-0.25),
                        Point2D(-1.5,0.25),
                        Point2D(0,0.25),
                        Point2D(0,0.75)
                        ])  # REMOVER
    points = getOrderedPoints(polygon)

    # lista todas interseções
    i = 0
    while i < len(points):
        p1 = points[i]
        p2 = points[(i+1)%len(points)]

        line = cohenSutherlandClip(Line(p1, p2))

        if line:
            t1 = pointClip(p1)
            t2 = pointClip(p2)
            if t1:
                if not t2:
                    np = line.end
                    np.type = 2
                    insertPoint(points, np, i+1)
            else:
                if t2:
                    np = line.start
                    np.type = 1
                    insertPoint(points, np, i+1)
                else:
                    np1 = line.start
                    np2 = line.end
                    np1.type = 1
                    np2.type = 2
                    insertPoint(points, np1, i+1)
                    insertPoint(points, np2, i+2)
                    i+=1
        i += 1
    # END FOR

    # nova lista dos pontos clip (varre as bordas externas)
    control = len(points)
    # borda superior
    sup = [Point2D(-1, 1)]
    for i in range(control):
        if points[i].y == 1 and points[i] not in sup:
            sup.append(points[i])
    sup.sort(key=lambda a: a.x)
    # borda direita
    right = [Point2D(1, 1)]
    for i in range(control):
        if points[i].x == 1 and points[i] not in right:
            right.append(points[i])
    right.sort(key=lambda a: a.y, reverse=True)
    # borda inferior
    inf = [Point2D(1, -1)]
    for i in range(control):
        if points[i].y == -1 and points[i] not in inf:
            inf.append(points[i])
    inf.sort(key=lambda a: a.x, reverse=True)
    # borda esquerda
    left = [Point2D(-1, -1)]
    for i in range(control):
        if points[i].x == -1 and points[i] not in left:
            left.append(points[i])
    left.sort(key=lambda a: a.y)

    clipping = sup + right + inf + left

    markUnvisited(points)

    # fluxo principal
    visible = []
    for i in range(len(points)):  # FLUXO PARA PERCORRER TODOS OS PONTOS DO OBJETO CLIPPADO
        if points[i].visited: continue

        if pointClip(points[i]):
            # DEFINE UM NOVO ESPACO PARA POLIGONO
            visible.append([])

            point = points[i]
            l = 1
            index = i
            while True:
                if point.visited:
                    break
                else:  # INSERE O PONTO NO POLIGONO A SER DESENHADO
                    point.visited = True
                    visible[-1].append(point)

                # DEFINING NEXT LIST
                if point.type == 1:  # INCOMING
                    l = 1
                    index = (points.index(point)+1)
                elif point.type == 2:  # OUTGOING
                    l = 2
                    index = (clipping.index(point)+1)
                else:
                    index = index+1

                # DEFINING NEXT
                if l == 1:
                    point = points[index % len(points)]
                else:
                    point = clipping[index % len(clipping)]

            # end of visits
    # END FOR

    for polygon in visible:
        for point in polygon:
            print(point)
        print("-------------------------")
    print()
