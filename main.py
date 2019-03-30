import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# import Viewport

class Handler:
    def __init__(self,builder):
        self.builder = builder

    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    def onListRightclicked(self, button, user_data):
        # print("Hello World!")
        dialog_add_object = self.builder.get_object("dialog_add_object")
        dialog_add_object.show_all()

    def onDraw(self,widget,event):
        pass
        # self.viewp.draw(widget,event)

    def bt_create_object_clicked_cb(self, button):
        lb_point_x = self.builder.get_object("lb_point_x")
        lb_point_y = self.builder.get_object("lb_point_y")
        try:
            x = int(lb_point_x.get_text())
            y = int(lb_point_y.get_text())
            print(x)
            print(y)
        except:
            print("Invalid value")

class WindowBuilder:
    def run(self):
        builder = Gtk.Builder()
        builder.add_from_file("ui.glade")
        builder.add_from_file("add_object.glade")
        builder.connect_signals(Handler(builder))

        window = builder.get_object("window_main")
        window.show_all()

        # viewp = builder.get_object("viewport")

        Gtk.main()

if  __name__ =='__main__':
    WindowBuilder().run()