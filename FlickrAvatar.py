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
import Login
import Plugin
from gobject import timeout_add, source_remove
from flickrAvatar.flickrAvatar import *
import os

#Plugin Class
class MainClass(Plugin.Plugin):

	description = _('Get emesene\'s avatar images from your Flickr sets [Ver.1.0]')
	authors = {
		'Stagi Andrea (4ndreaSt4gi)' : 'stagi dot andrea at gmail dot com'
	}

	website = 'http://code.google.com/p/flickravatar'

	displayName = _('Flickr Avatar')
	name = 'FlickrAvatar1.0'

	def __init__(self, controller, msn):
		Plugin.Plugin.__init__(self, controller, msn)
		self.controller = controller
		self.app=None

		self.current_user = self.controller.config.getCurrentUser()

	def start(self):
		'''start the plugin'''

		self.img = gtk.Image()

		if os.path.exists(os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","flickr.png")):
			self.img.set_from_file(os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","flickr.png"))
		else:
			self.img.set_from_file(os.path.join(os.getcwd(),"plugins_base","flickrAvatar","img","flickr.png"))

		self.flickrbtn = gtk.Button()
		self.flickrbtn.connect("clicked",self.show_dialog)
		self.flickrbtn.set_tooltip_text("Load Avatar from Flickr")
		self.flickrbtn.set_image(self.img)
		self.flickrbtn.set_relief(gtk.RELIEF_NONE)
		self.flickrbtn.set_alignment(1.0,0.0)


		try:
			os.mkdir(os.path.join(os.path.expanduser("~"),".config",".flickrmsntemp"))
		except:
			pass

		self.hbox = gtk.HBox()
		self.hbox.pack_start(self.flickrbtn,False,False)
		self.controller.mainWindow.userPanel.hbox2.pack_start(self.hbox,False,False)
		self.hbox.show_all()

		self.app=App(self.controller,self.current_user)
		self.app.main()

		self.enabled = True

	def stop(self):

		self.app.stopSlide()
		self.app.cleanAll()
		self.hbox.destroy()
		self.enable=False

	def check(self):
		return (True, 'Ok')

	def show_dialog(self,event):
		self.app.mbox.show()
