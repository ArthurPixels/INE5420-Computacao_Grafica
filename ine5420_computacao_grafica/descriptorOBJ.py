from ine5420_computacao_grafica.object import (
    # Object,
    Point2D,
    DrawablePolygon,
    DrawablePoint2D,
    DrawableLine,
    DrawableCurve,
    CurveType
)

from ine5420_computacao_grafica.window import Window


def encode_point2d(pt: Point2D):
    return f"{pt.x} {pt.y} 1.0"


def encode(window: Window, display_file: dict):
    vertices = ""
    objects = ""

    vertices += f"v {encode_point2d(window.wc)}\n"
    vertices += f"v {window.width} {window.height} 1.0\n"

    objects += f"o window\n"
    objects += f"w 0 1\n"
    vertex_id = 2

    for obj in display_file.values():
        objects += f"o {obj.name}\n"

        if isinstance(obj, DrawablePoint2D):
            vertices += f"v {encode_point2d(Point2D(obj.x, obj.y))}\n"

            objects += f"p {vertex_id}\n"
            vertex_id += 1
        elif isinstance(obj, DrawableLine):
            vertices += f"v {encode_point2d(obj.start)}\n"
            vertices += f"v {encode_point2d(obj.end)}\n"

            objects += f"l {vertex_id} {vertex_id + 1}\n"
            vertex_id += 2
        elif isinstance(obj, DrawablePolygon):
            obj_vertex_id = ""
            for i, vertex in enumerate(obj.points):
                vertices += f"v {encode_point2d(vertex)}\n"
                obj_vertex_id += f" {vertex_id + i}"

            if obj.filled:
                objects += f"usemtl filled\n"
            objects += f"f{obj_vertex_id}\n"
            vertex_id += len(obj.points)

        elif isinstance(obj, DrawableCurve):
            cstype = "cstype "
            if obj.curve_type == CurveType.bezier:
                cstype += "bezier"
            else:  # b-spline
                cstype += "bspline"

            obj_vertex_id = ""
            for i, vertex in enumerate(obj.points):
                vertices += f"v {encode_point2d(vertex)}\n"
                obj_vertex_id += f" {vertex_id + i}"

            objects += cstype + "\n"
            objects += f"curv2{obj_vertex_id}\n"
            vertex_id += len(obj.points)

    return vertices + objects


def decode(text):
    vertices = []
    window = None
    display_file = {}
    obj_name = "default"
    filled = False
    obj_id = 0

    for line in text.splitlines():
        cmd, *args = line.split(" ")

        if cmd == "w":
            size = vertices[int(args[1])]
            window = Window(vertices[int(args[0])], 0, size.x, size.y)
        elif cmd == "v":
            vertices.append(Point2D(float(args[0]), float(args[1])))
        elif cmd == "o":
            obj_name = " ".join(args)
        elif cmd == "usemtl":
            # if args[0] == "texture":
            filled = True
        elif cmd == "p":
            display_file[obj_id] = DrawablePoint2D(
                obj_id, obj_name, vertices[int(args[0])].x, vertices[int(args[0])].y
            )
            obj_id += 1
        elif cmd == "l":
            if len(args) == 2:
                display_file[obj_id] = DrawableLine(
                    obj_id, obj_name, vertices[int(args[0])], vertices[int(args[1])]
                )
            obj_id += 1
        elif cmd == "f":
            display_file[obj_id] = DrawablePolygon(
                obj_id, obj_name, [vertices[int(i)] for i in args], filled
            )
            obj_id += 1
            filled = False
        elif cmd == "cstype":
            curvtype = args[0]
        elif cmd == "curv2":
            if curvtype == "bezier":
                display_file[obj_id] = DrawableCurve(obj_id, obj_name, [vertices[int(i)] for i in args], CurveType.bezier)
            else:
                display_file[obj_id] = DrawableCurve(obj_id, obj_name, [vertices[int(i)] for i in args], CurveType.b_spline)
            obj_id += 1
    return window, display_file


def file_load(file):
    window = None
    display_file = []
    with open(file, "r") as f:
        window, display_file = decode(f.read())
    return window, display_file


def file_save(file, window: Window, display_file: dict):
    with open(file, "w+") as f:
        f.write(encode(window, display_file))
