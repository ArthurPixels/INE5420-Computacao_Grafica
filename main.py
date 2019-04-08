import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from object import Object
from point import Point
from line import Line
from polygon import Polygon
from viewport import Viewport
from window import Window
import cairo


# CONSTANTS
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800
VIEWPORT_HEIGHT = 600
VIEWPORT_WIDTH = 600


# GENERAL ATTRIBUTES
window_ = Window(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
viewport_ = Viewport(0, 0, VIEWPORT_WIDTH, VIEWPORT_HEIGHT)
display_file_ = []


# FUNCTIONS TO ADAPT X AND Y FROM WINDOW TO VIEWPORT
def viewport_transform_x(x):
    return (x - window_.win_min_.x_)/(window_.win_max_.x_ - window_.win_min_.x_) * (viewport_.x_max_ - viewport_.x_min_)

def viewport_transform_y(y):
    return (1 - (y - window_.win_min_.y_)/(window_.win_max_.y_ - window_.win_min_.y_)) * (viewport_.y_max_ - viewport_.y_min_)


# Create object dialog signal handler
class COHandler:
    def __init__(self,builder,dialog_add_object):
        self.builder = builder
        self.dialog_add_object = dialog_add_object


    # defines a new object insertion into the system
    def bt_create_object_clicked_cb(self, button):
        page = self.builder.get_object("add_obj_notebook").get_current_page()

        try:
            name = self.builder.get_object("entry_obj_name").get_text()
            if name == "":
                raise ValueError()

            id = len(display_file_)

            # new point insertion
            if page == 0:
                x = float(self.builder.get_object("entry_point_x").get_text())
                y = float(self.builder.get_object("entry_point_y").get_text())

                obj = Point(id, name, x, y)

            # new line insertion
            elif page == 1:
                x1 = float(self.builder.get_object("entry_line_x1").get_text())
                y1 = float(self.builder.get_object("entry_line_y1").get_text())
                x2 = float(self.builder.get_object("entry_line_x2").get_text())
                y2 = float(self.builder.get_object("entry_line_y2").get_text())

                obj = Line(id, name, Point(1, "P1", x1, y1), Point(2, "P2", x2, y2))

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
                    pontos.append(Point(i, "P" + str(i), float(x), float(y)))

                obj = Polygon(id, name, pontos)

            # end if

            display_file_.append(obj)

            store = self.builder.get_object("liststore_obj")
            store.append([id, obj.name_, obj.type_])

            da = self.builder.get_object("gtk_drawing_area")
            da.draw(da.get_window().cairo_create())

            self.dialog_add_object.destroy()
        except ValueError:
            WindowBuilder.print_log(self.builder, "Error: Invalid Value / All fields need to be defined\n")


    # defines the funcionality of the cancel button
    def bt_cancel_create_object_clicked_cb(self, button):
        self.dialog_add_object.destroy()

# end of class COHandler


class Handler:
    def __init__(self,builder):
        self.builder = builder
        self.store = builder.get_object("liststore_obj")
        print("Handler init ok")

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    # trata dos eventos que seguem a um clique sobre a object_list
    def obj_list_clicked_cb(self, widget, event):
        # clique com o botao direito
        if event.button == 3:
            self.builder.get_object("obj_list_popup_menu").popup_at_pointer(None)

    # "add object" option selected from obj_list_popup_menu
    def add_obj_activated(self, widget):
        self.builder.add_from_file("add_object.glade")
        dialog_add_object = self.builder.get_object("dialog_add_object")
        self.builder.connect_signals(COHandler(self.builder, dialog_add_object))
        dialog_add_object.show_all()

    def on_draw(self,widget,cairo):
        cairo.set_line_width(1)
        cairo.set_source_rgb(0,0,1)

        for obj in display_file_:
            obj.draw(viewport_transform_x, viewport_transform_y, cairo)



    ################ Navigation #####################
    def bt_zoom_in_clicked_cb(self,button):
        pass

    def bt_zoom_out_clicked_cb(self,button):
        pass

    def bt_rotate_view_clockwise_clicked_cb(self,button):
        pass

    def bt_rotate_view_counter_clockwise_clicked_cb(self,button):
        pass

    def bt_move_view_left_clicked_cb(self,button):
        pass

    def bt_move_view_down_clicked_cb(self,button):
        pass

    def bt_move_view_right_clicked_cb(self,button):
        pass

    def bt_move_view_up_clicked_cb(self,button):
        pass

    # Object
    def bt_rotate_obj_clockwise_clicked_cb(self,button):
        pass

    def bt_rotate_obj_counter_clockwise_clicked_cb(self,button):
        pass

    def bt_move_obj_left_clicked_cb(self,button):
        pass

    def bt_move_obj_down_clicked_cb(self,button):
        pass

    def bt_move_obj_right_clicked_cb(self,button):
        pass

    def bt_move_obj_up_clicked_cb(self,button):
        pass


# end of class Handler


class WindowBuilder:
    def __init__(self):
        self.ui_obj_list = None
        self.text_view = None

    def run(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        builder.connect_signals(Handler(builder))
        self.ui_obj_list = builder.get_object("obj_list")
        self.text_view = builder.get_object("system_log")


        gtk_window = builder.get_object("gtk_window")
        gtk_window.show_all()

        Gtk.main()

    # function to append a text at the end of the buffer from system_log
    def print_log(self, builder, text):
        buffer = self.text_view.get_buffer()
        iterator = buffer.get_iter_at_offset(-1)
        buffer.insert(iterator, text, -1)

# end of class WindowBuilder

if  __name__ =='__main__':
    WindowBuilder().run()
