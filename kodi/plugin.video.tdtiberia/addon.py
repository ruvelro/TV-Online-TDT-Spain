import sys
import xbmcgui
import xbmcplugin

import channelproviders

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')


thisAddon = xbmcaddon.Addon()
iconsWanted = thisAddon.getSetting('retrieve_icons')
includeDisabled = thisAddon.getSetting('include_disabled_channels')
# thisAddon.setSetting('my_setting', 'false')


# provider = channelproviders.GitHubJSON(includeDisabled)
# provider = channelproviders.TvOnlineAPP()
provider = channelproviders.GitHubMD()

channelList = provider.retrieveList()

for channel in channelList:
	channelListItem = xbmcgui.ListItem(channel[0])
	xbmcplugin.addDirectoryItem(handle=addon_handle, url=channel[1], listitem=channelListItem)

xbmcplugin.endOfDirectory(addon_handle)
