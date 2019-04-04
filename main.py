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

viewport = None
display_file_ = []


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

            id = len(display_file_)  # VER

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

            viewp = self.builder.get_object("viewport")
            viewp.draw(viewp.get_window().cairo_create())

            self.dialog_add_object.destroy()
        except ValueError:
            self.print_on_log("Error: Invalid Value / All fields need to be defined\n")


    # defines the funcionality of the cancel button
    def bt_cancel_create_object_clicked_cb(self, button):
        self.dialog_add_object.destroy()

    # function to append a text at the end of the buffer from system_log (TIRAR DAQUI)
    def print_on_log(self, text):
        text_view = self.builder.get_object("system_log")
        buffer = text_view.get_buffer()
        iterator = buffer.get_iter_at_offset(-1)
        buffer.insert(iterator, text, -1)

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
            obj.draw(cairo)
        # self.viewp.draw(widget,event)


class WindowBuilder:
    def __init__(self):
        self.ui_obj_list = None

    def updateObjectList(self, store, name):
        store.append([name])

    def run(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        builder.connect_signals(Handler(builder))
        self.ui_obj_list = builder.get_object("obj_list")

        window = builder.get_object("window_main")
        window.show_all()


        Gtk.main()

if  __name__ =='__main__':
    WindowBuilder().run()
