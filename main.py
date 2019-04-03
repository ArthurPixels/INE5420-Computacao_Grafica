import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from object import Object
from point import Point
from line import Line
from polygon import Polygon
from viewport import Viewport
from window import Window

viewport = None
display_file_ = []

# Create object dialog signal handler
class COHandler:
    def __init__(self,builder,dialog_add_object):
        self.builder = builder
        self.dialog_add_object = dialog_add_object

    def bt_create_object_clicked_cb(self, button):
        entry_obj_name = self.builder.get_object("entry_obj_name")
        entry_point_x = self.builder.get_object("entry_point_x")
        entry_point_y = self.builder.get_object("entry_point_y")
        try:
            x = float(entry_point_x.get_text())
            y = float(entry_point_y.get_text())

            # descobrir id e passar no lugar do 0
            id = 0  # VER
            obj = Point(id, entry_obj_name.get_text(), x, y)
            display_file_.append(obj)

            store = self.builder.get_object("liststore_obj")
            store.append([id, obj.name_, obj.type_])
            self.dialog_add_object.destroy()
        except:
            print("Error: Invalid value\n")

    def bt_cancel_create_object_clicked_cb(self, button):
        self.dialog_add_object.destroy()

class Handler:
    def __init__(self,builder):
        self.builder = builder
        self.store = builder.get_object("liststore_obj")
        print("Handler init ok")

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    def obj_list_clicked_cb(self, button, user_data):
        self.builder.add_from_file("add_object.glade")
        dialog_add_object = self.builder.get_object("dialog_add_object")
        self.builder.connect_signals(COHandler(self.builder, dialog_add_object))
        dialog_add_object.show_all()

    def onDraw(self,widget,event):
        pass
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

        # viewp = builder.get_object("viewport")

        Gtk.main()

if  __name__ =='__main__':
    WindowBuilder().run()
