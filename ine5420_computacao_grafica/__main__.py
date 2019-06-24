import sys  # noqa: F401
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # noqa: E402
from ine5420_computacao_grafica.base_forms import Point2D, CurveType  # noqa: E402
from ine5420_computacao_grafica.object import (
    DrawablePolygon,
    DrawablePoint2D,
    DrawableLine,
    DrawableCurve
)  # noqa: E402
from ine5420_computacao_grafica.viewport import Viewport  # noqa: E402
from ine5420_computacao_grafica.window import Window  # noqa: E402
import ine5420_computacao_grafica.descriptorOBJ as descOBJ  # noqa: E402
import math  # noqa: E402

# import os  # noqa: E402


# ################ Create object dialog signal handler #################
class CreateObjectHandler:
    def __init__(self, main_window, dialog_add_object):
        self.main_window = main_window
        self.builder = main_window.builder
        self.dialog_add_object = dialog_add_object

    # defines a new object insertion into the system
    def bt_create_object_clicked_cb(self, button):
        page = self.builder.get_object("add_obj_notebook").get_current_page()

        try:
            name = self.builder.get_object("entry_obj_name").get_text()

            new_id = 0
            if self.main_window.display_file:
                new_id = max(self.main_window.display_file)
                new_id += 1

            # new point insertion
            if page == 0:
                x = float(self.builder.get_object("entry_point_x").get_text())
                y = float(self.builder.get_object("entry_point_y").get_text())

                if name == "":
                    name = f"Point {new_id}"
                obj = DrawablePoint2D(new_id, name, x, y)

            # new line insertion
            elif page == 1:
                x1 = float(self.builder.get_object("entry_line_x1").get_text())
                y1 = float(self.builder.get_object("entry_line_y1").get_text())
                x2 = float(self.builder.get_object("entry_line_x2").get_text())
                y2 = float(self.builder.get_object("entry_line_y2").get_text())

                if name == "":
                    name = f"Line {new_id}"
                obj = DrawableLine(new_id, name, Point2D(x1, y1), Point2D(x2, y2))

            # new wireframe insertion
            elif page == 2:
                buffer = self.builder.get_object("wireframe_points_view").get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                entrada = buffer.get_text(start_iter, end_iter, False)
                entrada = entrada.split("\n")

                pontos = []
                for i in range(len(entrada)):
                    x, y = entrada[i].split()
                    pontos.append(Point2D(float(x), float(y)))

                if name == "":
                    name = f"Wireframe {new_id}"
                obj = DrawablePolygon(new_id, name, pontos, False)

            # add curve
            elif page == 3:
                curve_type = None
                if self.builder.get_object("rdb_bezier").get_active():
                    if name == "":
                        name = f"Bezier {new_id}"
                    curve_type = CurveType.bezier
                else:
                    if name == "":
                        name = f"B-spline {new_id}"
                    curve_type = CurveType.b_spline

                buffer = self.builder.get_object("curve_points_view").get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                entrada = buffer.get_text(start_iter, end_iter, False)
                entrada = entrada.split("\n")

                pontos = []
                for i in range(len(entrada)):
                    x, y = entrada[i].split()
                    pontos.append(Point2D(float(x), float(y)))

                obj = DrawableCurve(new_id, name, pontos, curve_type)
            # end if

            if name == "":
                raise ValueError()

            self.main_window.display_file[obj.id] = obj

            store = self.builder.get_object("liststore_obj")
            store.append([new_id, obj.name, obj.type])

            da = self.builder.get_object("gtk_drawing_area")
            da.draw(da.get_window().cairo_create())

            self.dialog_add_object.destroy()
        except ValueError:
            self.main_window.print_log(
                "Error: Invalid Value / All fields need to be defined\n"
            )

    # defines the funcionality of the cancel button
    def bt_cancel_create_object_clicked_cb(self, button):
        self.dialog_add_object.destroy()


# end of class CreateObjectHandler


class PreferencesWindowHandler:
    def __init__(self, main_window, dialog_preferences):
        self.main_window = main_window
        self.builder = main_window.builder
        self.dialog_preferences = dialog_preferences

    def cb_preferences_apply(self, *args):
        if self.builder.get_object("rb_rotation_center_world").get_active():
            self.main_window.rotationCenter = RotationCenter.WORLD
        elif self.builder.get_object("rb_rotation_center_object").get_active():
            self.main_window.rotationCenter = RotationCenter.OBJECT
        elif self.builder.get_object("rb_rotation_center_arbitrary").get_active():
            self.main_window.rotationCenter = RotationCenter.ARBITRARY

        if self.builder.get_object("rb_clipping_algorithm_cs").get_active():
            self.main_window.clippingAlgorithm = ClippingAlgorithm.CS
        elif self.builder.get_object("rb_clipping_algorithm_nln").get_active():
            self.main_window.clippingAlgorithm = ClippingAlgorithm.NLN

        self.dialog_preferences.destroy()

    def cb_preferences_cancel(self, button):
        self.dialog_preferences.destroy()


class SelectFileHandler:
    def __init__(self, main_window, main_window_handler, load, dialog_select_file):
        self.main_window = main_window
        self.main_window_handler = main_window_handler
        self.builder = main_window.builder
        self.dialog_select_file = dialog_select_file
        self.load = load

    def bt_cancel_select_file_clicked_cb(self, *args):
        self.main_window.save = False
        self.dialog_select_file.destroy()

    def bt_ok_select_file_clicked_cb(self, *args):
        filename = self.builder.get_object("entry_filepath").get_text()
        if filename == "":
            filename = "persistance"
        filename = str.replace(filename, "\\ ", " ")
        self.main_window.filepath = f"obj_files/{filename}.obj"
        self.main_window.save = True
        if self.load:
            self.main_window_handler.file_load()
        else:
            self.main_window_handler.file_save()
        self.dialog_select_file.destroy()


class MouseButtons:
    left = 1
    middle = 2
    right = 3


class RotationCenter:
    WORLD = 1
    OBJECT = 2
    ARBITRARY = 3


class ClippingAlgorithm:
    CS = 1
    NLN = 2


# ################ #################
class MainWindowHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.builder = main_window.builder
        self.main_window.filepath = "obj_files/persistance.obj"
        self.store = self.builder.get_object("liststore_obj")
        self.scrolled_window = self.builder.get_object("scrolled_window_log")
        self.lb_window_pos = self.builder.get_object("lb_window_pos")
        self.entry_step = self.builder.get_object("entry_step")
        self.entry_angle = self.builder.get_object("entry_angle")
        self.da_width = 0
        self.da_height = 0
        self.mouse_start_pos = None
        self.mouse_pressed = False
        self.window = Window(Point2D(0, 0), 0, 200, 200)
        self.viewport = Viewport(0, 0, 100, 100, 100, 100)

    def file_load(self):
        try:
            self.window, self.main_window.display_file = descOBJ.file_load(
                self.main_window.filepath
            )
        except FileNotFoundError:
            self.main_window.print_log(f"File not found: {self.main_window.filepath}")
        except Exception as e:
            self.main_window.print_log(f"Exception: {e}")

        for obj in self.main_window.display_file.values():
            self.store = self.builder.get_object("liststore_obj")
            self.store.append([obj.id, obj.name, obj.type])

        # draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    def gtk_window_show_cb(self, *args):
        self.file_load()

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    def cb_menu_file_new(self, *args):
        self.main_window.display_file.clear()
        self.store.clear()

        self.window = Window(Point2D(0, 0), 0, 200, 200)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    def open_filepath_dialog(self, load):
        self.builder.add_from_file("ine5420_computacao_grafica/ui/select_file.glade")
        dialog_select_file = self.builder.get_object("dialog_select_file")
        self.builder.connect_signals(
            SelectFileHandler(self.main_window, self, load, dialog_select_file)
        )
        dialog_select_file.show_all()

    def cb_menu_file_open(self, *args):
        self.open_filepath_dialog(True)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    def file_save(self):
        if self.main_window.save:
            descOBJ.file_save(
                self.main_window.filepath, self.window, self.main_window.display_file
            )
            self.main_window.print_log(f"FILE SAVED: {self.main_window.filepath}")

    def cb_menu_file_save(self, *args):
        self.file_save()

    def cb_menu_file_save_as(self, *args):
        self.open_filepath_dialog(False)

    def cb_menu_file_quit(self, *args):
        self.main_window.gtk_window.destroy()

    def cb_menu_edit_reset_window(self, *args):
        self.window = Window(Point2D(0, 0), 0, 200, 200)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    def cb_menu_edit_preferences(self, *args):
        self.builder.add_from_file("ine5420_computacao_grafica/ui/preferences.glade")
        dialog_preferences = self.builder.get_object("dialog_preferences")
        self.builder.connect_signals(
            PreferencesWindowHandler(self.main_window, dialog_preferences)
        )

        if self.main_window.rotationCenter == RotationCenter.WORLD:
            self.builder.get_object("rb_rotation_center_world").set_active(True)
        elif self.main_window.rotationCenter == RotationCenter.OBJECT:
            self.builder.get_object("rb_rotation_center_object").set_active(True)
        elif self.main_window.rotationCenter == RotationCenter.ARBITRARY:
            self.builder.get_object("rb_rotation_center_arbitrary").set_active(True)

        if self.main_window.clippingAlgorithm == ClippingAlgorithm.CS:
            self.builder.get_object("rb_clipping_algorithm_cs").set_active(True)
        elif self.main_window.clippingAlgorithm == ClippingAlgorithm.NLN:
            self.builder.get_object("rb_clipping_algorithm_nln").set_active(True)

        dialog_preferences.show_all()

    # trata dos eventos que seguem a um clique sobre a object_list
    def obj_list_clicked_cb(self, widget, event):
        # clique com o botao direito
        if event.button == MouseButtons.right:
            self.builder.get_object("obj_list_popup_menu").popup_at_pointer(None)

    # "add object" option selected from obj_list_popup_menu
    def add_obj_activated(self, widget):
        self.builder.add_from_file("ine5420_computacao_grafica/ui/add_object.glade")
        dialog_add_object = self.builder.get_object("dialog_add_object")
        self.builder.connect_signals(
            CreateObjectHandler(self.main_window, dialog_add_object)
        )
        dialog_add_object.show_all()

    def apply_to_selected_objects(self, value, f_win, f_obj):
        if self.builder.get_object("radio_option_window").get_active():
            f_win(value)
        else:
            self.main_window.print_log("Radio button: object selected")
            obj_list_ui = self.builder.get_object("obj_list")
            (model, pathlist) = obj_list_ui.get_selection().get_selected_rows()
            if pathlist:
                for path in pathlist:
                    try:
                        tree_iter = model.get_iter(path)
                        obj_id = int(model.get_value(tree_iter, 0))
                        self.main_window.print_log(f"obj_id: {obj_id}")
                    except TypeError:
                        self.main_window.print_log("failed to select object")
                    else:
                        f_obj(obj_id, value)
            else:
                self.main_window.print_log("Object not selected")

    # "remove object" option selected from obj_list_popup_menu
    def delete_obj_activated(self, widget):
        try:
            obj_list_ui = self.builder.get_object("obj_list")
            (model, pathlist) = obj_list_ui.get_selection().get_selected_rows()
            if pathlist:
                for path in pathlist:
                    try:
                        tree_iter = model.get_iter(path)
                        obj_id = int(model.get_value(tree_iter, 0))
                        self.main_window.print_log(f"obj_id: {obj_id}")
                    except TypeError:
                        self.main_window.print_log("failed to select object")
                    else:
                        self.main_window.display_file.pop(obj_id)
                        model.remove(tree_iter)

            # re-draw objects on drawing_area
            self.main_window.drawing_area.queue_draw()
        except TypeError:
            self.main_window.print_log("No object selected to be removed\n")

    def scroll_log(self, widget, event, data=None):
        adj = self.scrolled_window.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    # draws the objects in the world of representation
    def on_draw(self, widget, cairo_):
        # def viewport_transform(point: Point):
        #     coords = np.matrix([[point.x, point.y, 1]])
        #
        #     return Point()
        wx = self.window.wc.x
        wy = self.window.wc.y
        self.lb_window_pos.set_text(f"Window: ({wx:.2f}, {wy:.2f})")

        width = self.main_window.drawing_area.get_allocation().width
        height = self.main_window.drawing_area.get_allocation().height
        if self.da_width != width or self.da_height != height:
            self.da_width = width
            self.da_height = height
            self.main_window.print_log("drawing area width:" + str(width))
            self.main_window.print_log("drawing area height:" + str(height) + "\n")

        self.viewport = Viewport(10, 10, width - 10, height - 10, width, height)

        cairo_.save()
        cairo_.set_source_rgb(0, 0, 0)
        cairo_.move_to(self.viewport.x_min, self.viewport.y_max)
        cairo_.line_to(self.viewport.x_max, self.viewport.y_max)
        cairo_.line_to(self.viewport.x_max, self.viewport.y_min)
        cairo_.line_to(self.viewport.x_min, self.viewport.y_min)
        cairo_.line_to(self.viewport.x_min, self.viewport.y_max)
        cairo_.stroke()
        cairo_.restore()

        cairo_.set_line_width(1)
        cairo_.set_source_rgb(0, 0, 1)
        for obj in self.main_window.display_file.values():
            obj.update_scn(self.window.transform)
            obj.clip(self.main_window.clippingAlgorithm)
            if obj.visible:
                obj.draw(self.viewport.transform, cairo_)

    # ############### NAVIGATION #####################
    # drag
    def on_mouse_press(self, widget, event):
        # self.main_window.print_log("MOUSE PRESS")
        if event.button == MouseButtons.left:
            self.mouse_start_pos = Point2D(event.x, event.y)
            self.mouse_pressed = True

    def on_mouse_move(self, widget, event):
        # translate window
        if self.mouse_pressed:
            current_pos = Point2D(event.x, event.y)
            # self.main_window.print_log(f'event-x:{event.x} eventy:{event.y}')
            delta_viewport = Point2D(
                current_pos.x - self.mouse_start_pos.x,
                current_pos.y - self.mouse_start_pos.y,
            )
            # self.main_window.print_log(
            #         f'd_vp_x:{delta_viewport.x} d_vp_y:{delta_viewport.y}')
            delta_scn = self.viewport.viewport_to_scn(delta_viewport)
            # self.main_window.print_log(
            #         f'd_scn_x:{delta_scn.x} d_scn_y:{delta_scn.y}')
            delta_world = self.window.scn_to_world(delta_scn)

            def f_win(val):
                self.window.translate(val, 2)

            def f_obj(obj_id, val):
                self.main_window.display_file[obj_id].translate(val)

            self.apply_to_selected_objects(delta_world, f_win, f_obj)

            self.mouse_start_pos = current_pos
            widget.queue_draw()

    def on_mouse_release(self, widget, event):
        # self.main_window.print_log("MOUSE RELEASE")
        if event.button == MouseButtons.left:
            self.mouse_pressed = False

    def on_mouse_scroll(self, widget, event):
        # Handles zoom in / zoom out on Ctrl+mouse wheel
        accel_mask = Gtk.accelerator_get_default_mod_mask()
        direction = event.direction
        if event.state & accel_mask == Gdk.ModifierType.CONTROL_MASK:
            amount = 1 + (float(self.entry_step.get_text()) / 100)

            def f_win(amount):
                if direction == Gdk.ScrollDirection.UP:
                    self.window.zoom(-amount)
                else:
                    self.window.zoom(amount)

            def f_obj(obj_id, amount):
                if direction == Gdk.ScrollDirection.UP:
                    self.main_window.display_file[obj_id].scale(
                        1 / amount, self.main_window.rotationCenter
                    )
                else:
                    self.main_window.display_file[obj_id].scale(
                        amount, self.main_window.rotationCenter
                    )

            self.apply_to_selected_objects(amount, f_win, f_obj)

        else:
            angle = math.radians(float(self.entry_angle.get_text()))

            def f_win(angle):
                if direction == Gdk.ScrollDirection.UP:
                    self.window.rotate(angle)
                else:
                    self.window.rotate(-angle)

            def f_obj(obj_id, angle):
                if direction == Gdk.ScrollDirection.UP:
                    self.main_window.display_file[obj_id].rotate(
                        2 * angle, self.main_window.rotationCenter
                    )
                else:
                    self.main_window.display_file[obj_id].rotate(
                        -2 * angle, self.main_window.rotationCenter
                    )

            self.apply_to_selected_objects(angle, f_win, f_obj)

        widget.queue_draw()

    # Zoom in
    def bt_zoom_in_clicked_cb(self, button):
        self.handle_bt_scale(True)

    # Zoom out
    def bt_zoom_out_clicked_cb(self, button):
        self.handle_bt_scale(False)

    # scale: True to increase, False to decrease
    def handle_bt_scale(self, increase):
        amount = 0
        try:
            amount = 1 + (float(self.entry_step.get_text()) / 100)
        except ValueError:
            self.main_window.print_log("invalid value")

        if increase:
            amount = 1 / amount

        def f_win(amount):
            self.window.zoom(amount)

        def f_obj(obj_id, amount):
            self.main_window.display_file[obj_id].scale(
                amount, self.main_window.rotationCenter
            )

        self.apply_to_selected_objects(amount, f_win, f_obj)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    # Rotate left
    def bt_rotate_left_clockwise_clicked_cb(self, button):
        self.handle_bt_rotation(-1)

    # Rotate right
    def bt_rotate_rigth_clockwise_clicked_cb(self, button):
        self.handle_bt_rotation(1)

    # orientation multiply angle (1, -1)
    def handle_bt_rotation(self, orientation):
        try:
            angle = math.radians(float(self.entry_angle.get_text()))
        except ValueError:
            self.main_window.print_log("invalid value")

        def f_win(angle):
            self.window.rotate(angle)

        def f_obj(obj_id, angle):
            self.main_window.display_file[obj_id].rotate(
                orientation * angle, self.main_window.rotationCenter
            )

        self.apply_to_selected_objects(angle * orientation, f_win, f_obj)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()

    # button translation
    def bt_move_left_clicked_cb(self, button):
        self.handle_bt_translation(-1, 0)

    def bt_move_down_clicked_cb(self, button):
        self.handle_bt_translation(0, -1)

    def bt_move_right_clicked_cb(self, button):
        self.handle_bt_translation(1, 0)

    def bt_move_up_clicked_cb(self, button):
        self.handle_bt_translation(0, 1)

    # x, y multiply amount (-1, 0, 1)
    def handle_bt_translation(self, x, y):
        amount = 0
        try:
            amount = float(self.entry_step.get_text())
        except ValueError:
            self.main_window.print_log("invalid value")

        def f_win(amount):
            self.window.translate(Point2D(x * amount, y * amount), 1)

        def f_obj(obj_id, amount):
            self.main_window.display_file[obj_id].translate(
                Point2D(x * amount, y * amount)
            )

        self.apply_to_selected_objects(amount, f_win, f_obj)

        # re-draw objects on drawing_area
        self.main_window.drawing_area.queue_draw()


# end of class Handler


class MainWindow:
    def __init__(self):
        self.filepath = ""
        self.builder = None
        self.ui_obj_list = None
        self.text_view = None
        self.drawing_area = None
        self.display_file = {}
        self.clippingAlgorithm = ClippingAlgorithm.CS
        self.rotationCenter = RotationCenter.OBJECT
        self.save = True

    def run(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ine5420_computacao_grafica/ui/ui.glade")
        self.builder.connect_signals(MainWindowHandler(self))
        self.ui_obj_list = self.builder.get_object("obj_list")
        self.text_view = self.builder.get_object("system_log")
        self.drawing_area = self.builder.get_object("gtk_drawing_area")

        self.gtk_window = self.builder.get_object("gtk_window")
        self.gtk_window.show_all()

        Gtk.main()

    # function to append a text at the end of the buffer from system_log
    def print_log(self, text):
        buffer = self.text_view.get_buffer()
        iterator = buffer.get_iter_at_offset(-1)
        buffer.insert(iterator, text + "\n", -1)


# end of class MainWindow


if __name__ == "__main__":
    MainWindow().run()
