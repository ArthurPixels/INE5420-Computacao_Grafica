import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from object import Object
from point import Point
from line import Line
from polygon import Polygon
from viewport import Viewport
from window import Window



class DisplayFile:
    def __init__(self, dr_area):
        self.objects = []
        self.viewport = dr_area

    def append(self,obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            # self.ui_obj_list.AddItem(obj.name)
            pass

class Handler:
    def __init__(self,df,builder):
        self.builder = builder
        self.display_file = df
        self.ui_obj_list = builder.get_object("obj_list")
        self.store = Gtk.ListStore(str)
        self.ui_obj_list.set_model(self.store)
        print("Handler init ok")

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    def obj_list_clicked_cb(self, button, user_data):
        self.builder.add_from_file("add_object.glade")
        self.builder.connect_signals(Handler(self.display_file,self.builder))
        dialog_add_object = self.builder.get_object("dialog_add_object")
        dialog_add_object.show_all()

    def onDraw(self,widget,event):
        pass
        # self.viewp.draw(widget,event)

    def bt_create_object_clicked_cb(self, button):
        entry_obj_name = self.builder.get_object("entry_obj_name")
        entry_point_x = self.builder.get_object("entry_point_x")
        entry_point_y = self.builder.get_object("entry_point_y")
        try:
            x = float(entry_point_x.get_text())
            y = float(entry_point_y.get_text())
        except:
            print("Error: Invalid value")

        obj = Point(entry_obj_name.get_text(),x,y)
        self.display_file.append(obj)
        print(x)
        print(y)
        self.store.append([obj.get_name()])
        self.display_file.update()

class WindowBuilder:
    def run(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        df = DisplayFile(builder.get_object("viewport"))
        builder.connect_signals(Handler(df,builder))

        window = builder.get_object("window_main")
        window.show_all()

        # viewp = builder.get_object("viewport")

        Gtk.main()

if  __name__ =='__main__':
    WindowBuilder().run()
