import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import Viewport

class Handler:
	def onMainWindowDestroy(self, *args):
        Gtk.main_quit()

	def onListRightclicked(self, button, user_data):
        print("Hello World!")

	def onDraw(self,widget,event):
		Viewport.draw(widget,event)

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
builder.connect_signals(Handler())

window = builder.get_object("window_main")
window.show_all()

viewp = builder.get_object("viewport")
# viewp.gdjskafhgdksafkjdfskljgshgf

Gtk.main()
