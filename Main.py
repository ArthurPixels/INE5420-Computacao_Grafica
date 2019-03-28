import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
    def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

    def onListRightclicked(self, button, user_data):
        print("Hello World!")

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())

window = builder.get_object("window_main")
window.show_all()

Gtk.main()
