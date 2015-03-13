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

from flickrapi import *
from album import album
import time
import os
import webbrowser

api_key = '47b7b29216283347519507046f0562a8'
api_secret = '2510f66995bad407'

def auth(frob, perms):
   	print 'Please give us permission %s ' % (perms)

def loginService(user,app):

	ok=False

	flickr = FlickrAPI(api_key, api_secret,username=user,store_token=True)

	try:
		flickr.token_cache.path=os.path.join(os.path.expanduser("~"),".config",".flickrmsntemp")
		(token, frob) = flickr.get_token_part_one(perms='read')
	except:
		return None

	#if not token:

	while not ok:
		try:
			flickr.get_token_part_two((token, frob))
			ok=True
		except:

			if(app.cleanT()):
				ok=True

			time.sleep(1)
			continue

	return flickr

def destroyService(user):

	os.remove(os.path.join(os.path.expanduser("~"),".config",".flickrmsntemp",api_key,"auth-"+user+".token"))

def getAlbums(flickr):

	sets = flickr.photosets_getList()

	allsets=sets.find('photosets').findall('photoset')

	al=[]

	for aset in allsets:
		al.append(album(aset.find('title').text,aset.attrib['id'],aset.attrib['photos'],flickr))

	return al


