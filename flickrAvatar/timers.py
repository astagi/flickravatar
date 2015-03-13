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

import os
import re
import time
import sys
from threading import Thread

class refresh(Thread):

	def __init__ (self,app):
		Thread.__init__(self)
		self.app = app

	def run(self):
		self.app.disableAll()
		self.app.setLoading()

		while(self.app.isSettingEmesene()):
			time.sleep(2)

		self.app.refreshSets()
		self.app.enableAll()

class loadtim(Thread):

	def __init__ (self,app):
		Thread.__init__(self)
		self.app = app

	def run(self):
		self.app.setLoading()
		self.app.setPreview()

class slideshow(Thread):

	def __init__ (self,app):
		Thread.__init__(self)
		self.cont=True
		self.app = app
		self.rot=0

	def run(self):

		cost=0.2

		while self.cont:
			if(self.app.isLoaded() and self.rot==5):
				while not self.app.setEmesene():
					time.sleep(2)

				cost=1.0-(self.app.getSpeed()/5.0)
			time.sleep( cost * 20 / 5.0 )
			self.rot=(self.rot+1)%6

	def stop(self):
		self.cont=False



