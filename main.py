import gi
from gi.repository import Gtk
from object import Object
from point import Point
from drawable_line import DrawableLine
from drawable_point import DrawablePoint
from line import Line
from polygon import Polygon
from viewport import Viewport
from window import Window
import cairo
gi.require_version('Gtk', '3.0')


# ################ CONSTANTS #################
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
VIEWPORT_HEIGHT = 600
VIEWPORT_WIDTH = 600


# ################ GENERAL ATTRIBUTES #################
window_ = Window(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
viewport_ = Viewport(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
display_file_ = []
id_cont_ = 0


# ########## FUNCTIONS TO ADAPT X AND Y FROM WINDOW TO VIEWPORT ###############
def viewport_transform_x(x):
    return (x - window_.win_min_.x_)/(window_.win_max_.x_ - window_.win_min_.x_) * (viewport_.x_max_ - viewport_.x_min_)


def viewport_transform_y(y):
    return (1 - (y - window_.win_min_.y_)/(window_.win_max_.y_ - window_.win_min_.y_)) * (viewport_.y_max_ - viewport_.y_min_)


# ################ Create object dialog signal handler #################
class CreateObjectHandler:
    def __init__(self, main_window, dialog_add_object):
        self.builder = main_window.builder
        self.dialog_add_object = dialog_add_object

    # defines a new object insertion into the system
    def bt_create_object_clicked_cb(self, button):
        page = self.builder.get_object("add_obj_notebook").get_current_page()

        try:
            name = self.builder.get_object("entry_obj_name").get_text()
            if name == "":
                raise ValueError()

            global id_cont_
            id = id_cont_
            id_cont_ += 1

            # new point insertion
            if page == 0:
                x = float(self.builder.get_object("entry_point_x").get_text())
                y = float(self.builder.get_object("entry_point_y").get_text())

                obj = DrawablePoint(id, name, x, y)

            # new line insertion
            elif page == 1:
                x1 = float(self.builder.get_object("entry_line_x1").get_text())
                y1 = float(self.builder.get_object("entry_line_y1").get_text())
                x2 = float(self.builder.get_object("entry_line_x2").get_text())
                y2 = float(self.builder.get_object("entry_line_y2").get_text())

                obj = DrawableLine(id, name, Point(x1, y1), Point(x2, y2))

            # new wireframe insertion
            elif page == 2:
                buffer = self.builder.get_object("wireframe_points_view")\
                        .get_buffer()
                start_iter = buffer.get_start_iter()
                end_iter = buffer.get_end_iter()
                entrada = buffer.get_text(start_iter, end_iter, False)
                entrada = entrada.split("\n")

                pontos = []
                for i in range(len(entrada)):
                    x, y = entrada[i].split()
                    pontos.append(Point(float(x), float(y)))

                obj = Polygon(id, name, pontos)

            # end if

            display_file_.append(obj)

            store = self.builder.get_object("liststore_obj")
            store.append([id, obj.name_, obj.type_])

            da = self.builder.get_object("gtk_drawing_area")
            da.draw(da.get_window().cairo_create())

            self.dialog_add_object.destroy()
        except ValueError:
            MainWindow.print_log(
                "Error: Invalid Value / All fields need to be defined\n"
            )

    # defines the funcionality of the cancel button
    def bt_cancel_create_object_clicked_cb(self, button):
        self.dialog_add_object.destroy()

# end of class CreateObjectHandler


# ################ #################
class MainWindowHandler:
    def __init__(self, main_window):
        self.main_window = main_window
        self.builder = main_window.builder
        self.store = self.builder.get_object("liststore_obj")

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    # trata dos eventos que seguem a um clique sobre a object_list
    def obj_list_clicked_cb(self, widget, event):
        # clique com o botao direito
        if event.button == 3:
            self.builder.get_object("obj_list_popup_menu")\
                    .popup_at_pointer(None)

    # "add object" option selected from obj_list_popup_menu
    def add_obj_activated(self, widget):
        self.builder.add_from_file("add_object.glade")
        dialog_add_object = self.builder.get_object("dialog_add_object")
        self.builder.connect_signals(CreateObjectHandler(
            self.main_window, dialog_add_object)
        )
        dialog_add_object.show_all()

    # "remove object" option selected from obj_list_popup_menu
    def delete_obj_activated(self, widget):
        try:
            model, item = self.builder.get_object("obj_list")\
                    .get_selection().get_selected()
            id = model.get_value(item, 0)

            for obj in display_file_:
                if obj.id_ == id:
                    display_file_.remove(obj)
                    break

            model.remove(item)

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw(self.builder.get_object("gtk_drawing_area"))
        except TypeError:
            MainWindow.print_log("No object selected to be removed\n")

    # draws the objects in the world of representation
    def on_draw(self, widget, cairo_):
        viewport_.x_max_
        cairo_.set_line_width(1)
        cairo_.set_source_rgb(0, 0, 1)
        for obj in display_file_:
            obj.draw(viewport_transform_x, viewport_transform_y, cairo_)

    # ############### NAVIGATION #####################
    # step changed
    def entry_step_preedit_changed_cb(self, preedit, user_data):
        pass

    # angle changed
    def entry_angle_preedit_changed_cb(self, preedit, user_data):
        pass

    # Zoom in
    def bt_zoom_in_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            if self.builder.get_object("radio_option_window").get_active():
                window_.zoomIn(amount)

            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()
                id = model.get_value(item, 0)
                # IMPLEMENTAR USANDO COORDENADAS HOMOGENEAS

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw(self.builder.get_object("gtk_drawing_area"))
        except TypeError:
            MainWindow.print_log(
                """You must select an object first
                or switch to Window movementation mode\n"""
            )

    # Zoom out
    def bt_zoom_out_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            if self.builder.get_object("radio_option_window").get_active():
                window_.zoomOut(amount)

            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()
                id = model.get_value(item, 0)
                # IMPLEMENTAR USANDO COORDENADAS HOMOGENEAS

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw(self.builder.get_object("gtk_drawing_area"))
        except TypeError:
            MainWindow.print_log(
                """You must select an object first
                or switch to Window movementation mode\n"""
            )

    # Rotate left
    def bt_rotate_left_clockwise_clicked_cb(self, button):
        pass

    # Rotate right
    def bt_rotate_rigth_clockwise_clicked_cb(self, button):
        pass

    # move left
    def bt_move_left_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            if self.builder.get_object("radio_option_window").get_active():
                window_.moveLeft(amount)

            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()
                id = model.get_value(item, 0)
                # IMPLEMENTAR USANDO COORDENADAS HOMOGENEAS

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw(self.builder.get_object("gtk_drawing_area"))
        except TypeError:
            MainWindow.print_log(
                """You must select an object first
                or switch to Window movementation mode\n"""
            )

    # move down
    def bt_move_down_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            if self.builder.get_object("radio_option_window").get_active():
                window_.moveDown(amount)

            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()
                id = model.get_value(item, 0)
                # IMPLEMENTAR USANDO COORDENADAS HOMOGENEAS

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw(self.builder.get_object("gtk_drawing_area"))
        except TypeError:
            MainWindow.print_log(
                """You must select an object first
                or switch to Window movementation mode\n"""
            )

    # move right
    def bt_move_right_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            # identify who is the radio button selected
            # window radio option selected
            if self.builder.get_object("radio_option_window").get_active():
                window_.moveRight(amount)

            # objects radio option selected
            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()

                id = model.get_value(item, 0)
                # IMPLEMENT

            da = self.builder.get_object("gtk_drawing_area")
            Gtk.Widget.queue_draw(da)

        except TypeError:
            MainWindow.print_log(
                """You must select an object first
                or switch to Window movementation mode\n"""
            )

    # move up
    def bt_move_up_clicked_cb(self, button):
        try:
            # PEGAR VALOR DE ALGUM ENTRY BOX
            # QUE VAI REPRESENTAR A QUANTIDADE DE DESLOCAMENTO
            amount = 10

            if self.builder.get_object("radio_option_window").get_active():
                window_.moveUp(amount)

            else:
                model, item = self.builder.get_object("obj_list")\
                        .get_selection().get_selected()
                id = model.get_value(item, 0)
                # IMPLEMENTAR USANDO COORDENADAS HOMOGENEAS

            # re-draw objects on drawing_area
            Gtk.Widget.queue_draw()
        except TypeError:
            MainWindow.print_log(
                self.builder,
                """You must select an object first
                or switch to Window movementation mode\n"""
            )


# end of class Handler

class MainWindow:
    def __init__(self):
        self.builder = None
        self.ui_obj_list = None
        self.text_view = None
        self.drawing_area = None

    def run(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui.glade")
        self.builder.connect_signals(MainWindowHandler(self))
        self.ui_obj_list = self.builder.get_object("obj_list")
        self.text_view = self.builder.get_object("system_log")
        self.drawing_area = self.builder.get_object("gtk_drawing_area")

        gtk_window = self.builder.get_object("gtk_window")
        gtk_window.show_all()

        Gtk.main()

    # function to append a text at the end of the buffer from system_log
    def print_log(self, text):
        buffer = self.text_view.get_buffer()
        iterator = buffer.get_iter_at_offset(-1)
        buffer.insert(iterator, text, -1)

# end of class MainWindow


if __name__ == '__main__':
    MainWindow().run()
