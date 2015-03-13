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

import urllib
from flickrapi import shorturl

class album:

	title=''
	id_album=0
	n_photo=0
	flickr=None
	imgadd=[]


	def __init__(self,title,id_album,n_photo,flickr):
		self.title=title
		self.id_album=id_album
		self.n_photo=n_photo
		self.flickr=flickr
		self.imgadd=range(0,int(n_photo))

	def getTitle(self):
		return self.title

	def getId(self):
		return self.id_album

	def getPhotoCount(self):
		return int(self.n_photo)

	def refreshPhotos(self,index_p):

			countp=0

			for photo in self.flickr.walk_set(photoset_id=self.id_album,per_page=20):
				if(countp==index_p):

					srcfile="http://farm5.static.flickr.com/"+photo.get('server')+"/"+photo.get('id')+"_"+photo.get('secret')+"_s.jpg"

					self.imgadd[index_p]=srcfile

				countp+=1

	def getPhotos(self):
		return self.imgadd

