"""
	Developed by
	Andrea Stagi <stagi.andrea@gmail.com>

	FlickrAvatar image feeder for emesene
	Copyright (C) 2010 Andrea Stagi

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gtk
import sys
import os

class ModalBox:

	def __init__(self):

		#attribs
		self.user=gtk.Entry()
		self.time_change=gtk.Entry()
		self.logoutmess=gtk.Label("")

		self.logo=gtk.Image()
		self.preview=gtk.Image()

		self.combobox=gtk.ComboBoxEntry()
		self.combospeed=gtk.ComboBoxEntry()

		self.check_enable=gtk.CheckButton("Enable")
		self.check_random=gtk.CheckButton("Get Randomly")
		self.combo_change_callback=None

		self.btn_get_album=gtk.Button("Refresh your Sets from Flickr")
		self.btn_logout=gtk.Button("Logout")
		self.btn_ok=gtk.Button("Done")

		#gui layout
		self.main_boxv=gtk.VBox()
		self.main_box=gtk.HBox()
		self.main_boxv.pack_start(self.main_box)
		time_layout=gtk.HBox()
		time_layout.pack_start(gtk.Label("Rotation speed:"))
		time_layout.pack_start(self.combospeed)

		desc=gtk.VBox()

		desc.pack_start(self.logo)
		desc.pack_start(gtk.HSeparator())
		desc.pack_start(gtk.Label("Preview"))
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

		desc.pack_start(self.preview)
		desc.pack_start(self.btn_logout)

		fields=gtk.VBox()

		fields.pack_start(gtk.Label(""))
		fields.pack_start(self.logoutmess)
		fields.pack_start(self.btn_get_album)
		fields.pack_start(gtk.Label(""))
		fields.pack_start(gtk.Label("Choose your set to display:"))
		fields.pack_start(self.combobox)
		fields.pack_start(gtk.Label(""))
		fields.pack_start(self.check_enable)
		fields.pack_start(self.check_random)
		fields.pack_start(time_layout)

		self.main_box.pack_start(desc)
		self.main_box.pack_start(gtk.VSeparator())
		self.main_box.pack_start(fields)
		self.main_boxv.pack_start(self.btn_ok)

		#window
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.add(self.main_boxv)
		self.window.set_title("Flickr Avatar for emesene (ver. 1.0)")
		self.window.set_modal(True)

		#init
		self.set_model_from_list( self.combospeed , ["Very Slow","Slow","Medium","Fast"])
		self.combospeed.set_active(0)

		#signal connection
		self.btn_ok.connect("clicked",self.done_cb)
		self.btn_get_album.connect("clicked",self.get_album_cb)
		self.btn_logout.connect("clicked",self.logout_cb)
		self.combobox.connect("changed",self.combo_change_cb)
		self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.window.connect("delete-event", self.delete_event)
		self.window.set_resizable(False)

	#callbacks

	def set_app_logo(self,path):
		self.logo_path=path
		self.set_logo(self.logo_path)


	def set_on_logout(self):
		self.logoutmess.set_text("You have just been logged out.\nNow go on Flickr, login again,\nand press 'Refresh your Sets from Flickr'")

	def restore_on_logout(self):
		self.logoutmess.set_text("")

	def done_cb(self,event):
		if self.done_callback:
			self.done_callback()

	def get_album_cb(self,event):
		if self.get_album_callback:
			self.get_album_callback()
	def logout_cb(self,event):
		if self.logout_callback:
			self.logout_callback()

	def random_cb(self,event):
		if self.random_callback:
			self.random_callback()

	def combo_change_cb(self,event):
		if self.combo_change_callback:
			self.combo_change_callback()

	#callback setter
	def set_album_callback(self,cb):
		self.get_album_callback=cb

	def set_logout_callback(self,cb):
		self.logout_callback=cb

	def set_done_callback(self,cb):
		self.done_callback=cb

	def set_random_callback(self,cb):
		self.random_callback=cb

	def set_combo_change_callback(self,cb):
		self.combo_change_callback=cb

	#window callback

	def self_destroy(self,e,w):
		self.window.hide_all()

	def hide_event(self,e,w):
		self.window.hide()

	def show(self,e=None,w=None):
		self.window.show_all()

	def delete_event(self,event,widget):
		self.window.hide()
		return True

	def set_logo(self,img):
		self.logo.set_from_file(img)

	def set_preview(self,img):
		self.preview.set_from_file(img)

	def set_albums(self,albums):
		self.albums=albums
		self.set_model_from_list(self.combobox,albums)
		self.combobox.set_active(0)

	def get_selected_album(self):
		return self.combobox.get_active_text()

	def set_model_from_list (self,cb, items):
		model = gtk.ListStore(str)
		for i in items:
			model.append([i])
			cb.set_model(model)
			if type(cb) == gtk.ComboBoxEntry:
				cb.set_text_column(0)
			elif type(cb) == gtk.ComboBox:
				cell = gtk.CellRendererText()
				cb.pack_start(cell, True)
				cb.add_attribute(cell, 'text', 0)

	#states
	def is_enabled(self):
		return self.check_enable.get_active()

	def is_random(self):
		return self.check_random.get_active()

	def get_time_text(self,text):
		self.time_change.set_text(text)

	def set_time_text(self):
		return self.time_change.get_text()

	def get_combo_index(self):
		return self.combobox.get_active()

	def get_combo_speed_index(self):
		return self.combospeed.get_active()

	def set_combo_index(self,n):
		return self.combobox.set_active(n)

	def set_combo_speed_index(self,n):
		return self.combospeed.set_active(n)

