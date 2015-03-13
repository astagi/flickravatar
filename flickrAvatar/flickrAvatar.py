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

#! /usr/bin/python
from flickrutils import *
from album import *
from timers import *
from options import *
from modalbox import *
from utility import *
from flickrapi import *
import urllib
import random
import os
import tempfile

gtk.gdk.threads_init()

class App:

	def __init__(self,controller,user):

		self.options=readOpt(user)
		self.flickr=None
		self.albums=None
		self.mbox=None
		self.ht=None
		self.sld=None
		self.ldn=None
		self.cur_photo=0
		self.loaded=0
		self.controller=None

		self.tmpdir=tempfile.mkdtemp(suffix="flickrmsn")

		self.setemesene=0
		self.rnd=-1

		self.logout=True

		self.user=user

		self.curralbum=0
		self.speed=0

		self.needref=1

		self.isclean=False


		if os.path.exists(os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","wait.gif")):
			self.wait_path=os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","wait.gif")
			self.noimg_path=os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","noimg.png")
			self.logo_path=os.path.join(os.getcwd(),"emesene","plugins_base","flickrAvatar","img","logo.png")
		else:
			self.wait_path=os.path.join(os.getcwd(),"plugins_base","flickrAvatar","img","wait.gif")
			self.noimg_path=os.path.join(os.getcwd(),"plugins_base","flickrAvatar","img","noimg.png")
			self.logo_path=os.path.join(os.getcwd(),"plugins_base","flickrAvatar","img","logo.png")

		self.controller=controller

	def cleanAll(self):
		self.isclean=True

	def cleanT(self):
		return self.isclean


	def setOptions(self):
		self.mbox.check_enable.set_active(self.options.enabled)
		self.mbox.check_random.set_active(self.options.random)
		self.speed=self.options.speed
		self.mbox.set_combo_speed_index(self.options.speed)


	def isLoaded(self):
		return self.loaded


	def isSettingEmesene(self):
		return self.setemesene

	def on_get_album(self):

		self.mbox.restore_on_logout()

		if(os.name=="nt"):
			self.refreshSets()
		else:
			self.ldn=refresh(self)
			self.ldn.start()

	def on_logout(self):

		self.mbox.set_on_logout()

		try:
			destroyService(self.user)
		except:
			pass
		else:
			self.logout=True

	def on_dove(self):

		self.curralbum=self.mbox.get_combo_index()
		self.speed=self.mbox.get_combo_speed_index()
		self.stopSlide()

		self.options=FlickrOpt(self.mbox.is_enabled(),self.mbox.is_random(),self.albums[self.mbox.get_combo_index()].title,self.mbox.get_combo_speed_index())

		writeOpt(self.options,self.user)

		if(self.mbox.is_enabled()):
			self.startSlideShow()

		self.mbox.window.hide_all()

	def startSlideShow(self):
		self.sld=slideshow(self)
		self.sld.start()

	def on_change(self):
		if(self.loaded!=0):
			self.ht=loadtim(self)
			self.ht.start()

	def disableAll(self):
		self.mbox.btn_ok.set_sensitive(0)
		self.mbox.btn_get_album.set_sensitive(0)

	def enableAll(self):
		self.mbox.btn_ok.set_sensitive(1)
		self.mbox.btn_get_album.set_sensitive(1)

	def setLoading(self):
		self.mbox.set_preview(self.wait_path)

	def refreshNow(self):
		self.loaded=0

		if(self.cleanT()):
			return

		self.albums=getAlbums(self.flickr)

		titles=[]
		count=0

		for album in self.albums:
			titles.append(album.title + " (" + str(album.getPhotoCount()) + ")")

			if(album.title==self.options.album):
				self.curralbum=count
			count+=1

		self.loaded=1

	def refreshSets(self):
		self.loaded=0

		self.flickr=loginService(self.user,self)

		if(self.flickr!=None):
			self.logout=False
		else:
			self.logout=True
			return

		if(self.cleanT()):
			return

		self.albums=getAlbums(self.flickr)

		titles=[]
		count=0

		for album in self.albums:
			titles.append(album.title + " (" + str(album.getPhotoCount()) + ")")

			if(album.title==self.options.album):
				self.curralbum=count
			count+=1

		self.mbox.set_albums(titles)

		self.mbox.combobox.set_active(self.curralbum)

		self.setPreview()
		self.loaded=1

	def setPreview(self):
		self.albums[self.mbox.get_combo_index()].refreshPhotos(0)
		photo_url= self.albums[self.mbox.get_combo_index()].getPhotos()[0]

		filename=os.path.join(self.tmpdir,"imgprev.jpeg")
		download_file(photo_url,filename)

		self.mbox.set_preview(filename)

	def getSpeed(self):
		return self.speed


	def setEmesene(self):

		self.setemesene=1

		if(self.mbox.is_random()):
			newrnd=random.randint(0,self.albums[self.curralbum].getPhotoCount()-1)
			if(self.rnd==newrnd):
				newrnd=(newrnd+1)%self.albums[self.curralbum].getPhotoCount()
			self.rnd=newrnd

		else:
			self.cur_photo=self.cur_photo%self.albums[self.curralbum].getPhotoCount()
			self.rnd=self.cur_photo
			self.cur_photo+=1

		self.albums[self.curralbum].refreshPhotos(self.rnd)
		photo_url= self.albums[self.curralbum].getPhotos()[self.rnd]


		filename=os.path.join(self.tmpdir,"imgemesene.jpeg")
		download_file(photo_url,filename)

		self.controller.changeAvatar(filename)

		self.needref=(self.needref+1)%self.albums[self.curralbum].getPhotoCount()

		self.setemesene=0

		if(self.needref==0 and self.logout==False):
			self.refreshNow()


		return 1

	def stopSlide(self):

		if(self.sld!=None):
			self.sld.stop()

	def main(self):

		self.mbox=ModalBox()

		self.mbox.set_album_callback(self.on_get_album)
		self.mbox.set_done_callback(self.on_dove)
		self.mbox.set_logout_callback(self.on_logout)
		self.mbox.set_combo_change_callback(self.on_change)
		self.mbox.set_preview(self.noimg_path)
		self.mbox.set_app_logo(self.logo_path)

		self.setOptions()

		self.ldn=refresh(self)
		self.ldn.start()

		if(self.options.enabled):
			self.startSlideShow()

		return 0

