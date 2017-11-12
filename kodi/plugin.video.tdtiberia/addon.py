import sys
import xbmcgui
import xbmcplugin

import urllib2
from urlparse import urlparse
from string import whitespace

def uri_validator(x):
    try:
        result = urlparse(x)
        return result.scheme and result.netloc and result.path
    except:
        return False

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

response = urllib2.urlopen('https://raw.githubusercontent.com/ruvelro/TV-Online-TDT-Spain/master/README.md')
html = response.read()
# TODO: this could fail, handle the error

# Parse the readme.md
# get to the list
header, channelList = html.split('--- | ---')

# Split for each row
for channel in channelList.split('\n'):
	# This delimits a element in the list
	if '|' in channel:	
		channelName , channelURL = channel.split('|')
		# Remove annoying first space
		channelURL=channelURL[1:]
		# If we can set some day any icon ...
		# li = xbmcgui.ListItem('My First Video!', iconImage='DefaultVideo.png')
		if uri_validator(channelURL):
			channelListItem = xbmcgui.ListItem(channelName)
			xbmcplugin.addDirectoryItem(handle=addon_handle, url=channelURL, listitem=channelListItem)

xbmcplugin.endOfDirectory(addon_handle)
