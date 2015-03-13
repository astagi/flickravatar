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

import pickle
import os

def writeOpt(opt,user):

	output = open(os.path.join(os.path.expanduser("~"),".config",".flickrmsntemp",user+".fkl"), 'wb')
	pickle.dump(opt, output)
	output.close()

def readOpt(user):
	try:
		output = open(os.path.join(os.path.expanduser("~"),".config",".flickrmsntemp",user+".fkl"), 'rb')
		opt=pickle.load(output)
		output.close()
	except IOError as (errno, strerror):
		opt=FlickrOpt(True,True,0,0)
		writeOpt(opt,user)
	return opt


class FlickrOpt:

	def __init__(self,enabled,random,album,speed):
		self.enabled=enabled
		self.random=random
		self.album=album
		self.speed=speed
