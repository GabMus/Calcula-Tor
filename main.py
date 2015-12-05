#!/usr/bin/env python
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Gdk
import os
import sys
import evaluator

builder = Gtk.Builder()
builder.add_from_file("ui.glade")
HOME=os.environ.get('HOME')


window = builder.get_object("window1")

class App(Gtk.Application):
	def __init__(self):
		Gtk.Application.__init__(self, application_id="com.gabmus.calcula-tor", flags=Gio.ApplicationFlags.FLAGS_NONE)

		builder.get_object("aboutdialog").connect("delete-event", lambda *_: builder.get_object("aboutdialog").hide() or True)

		self.connect("activate", self.activateCb)


	def do_startup(self):
	# start the application
		Gtk.Application.do_startup(self)

	def activateCb(self, app):
		window.set_wmclass("CalculaTor", "CalculaTor")
		app.add_window(window)
		appMenu=Gio.Menu()
		appMenu.append("About", "app.about")
		appMenu.append("Quit", "app.quit")
		about_action = Gio.SimpleAction.new("about", None)
		about_action.connect("activate", self.on_about_activate)
		app.add_action(about_action)
		quit_action = Gio.SimpleAction.new("quit", None)
		quit_action.connect("activate", self.on_quit_activate)
		app.add_action(quit_action)
		app.set_app_menu(appMenu)
		window.show_all()
		window.resize(800,1)


	def on_about_activate(self, *agrs):
		builder.get_object("aboutdialog").show()

	def on_quit_activate(self, *args):
		self.quit()


entryOperation = builder.get_object("entryOperation")
entryResult = builder.get_object("entryResult")
buttonMenu = builder.get_object("buttonMenu")
textbufferLog = builder.get_object("textbufferLog")



class Handler:

	log=""
	small=True
	
	def __init__(self):
		entryOperation.connect("key-press-event", self.pressReturn)
	
	def onDeleteWindow(self, *args):
		Gtk.main_quit(*args)

	def computeString(self, op):
		try:
			return evaluator.eval_expr(op)
		except:
			return True #returns true when the op is invalid
			
	def pressReturn(self, entry, keypressevent):
		key=Gdk.keyval_name(keypressevent.keyval)
		if key=="KP_Enter" or key=="Return":
			self.calculateOperation(entryOperation)

	def calculateOperation(self, entry):
		res=self.computeString(entry.get_text())
		if res == True:
			entryResult.set_text("Invalid expression")
		else:
			entryResult.set_text(str(res))
			operation=entryOperation.get_text()+" = "+str(res)+"\n\n"
			self.log+=operation
			textbufferLog.set_text(self.log)

	def on_buttonMenu_clicked(self, btn):
		if self.small:
			window.resize(800,600)
			self.small=False
		else:
			self.small=True
			window.resize(800,1)

	def on_aboutdialog_close(self, dlg):
		dlg.hide()
		
	def on_buttonClearLog_clicked(self, btn):
		self.log=""		
		textbufferLog.set_text(self.log)

builder.connect_signals(Handler())


if __name__ == "__main__":
	app= App()
	app.run(sys.argv)
			
