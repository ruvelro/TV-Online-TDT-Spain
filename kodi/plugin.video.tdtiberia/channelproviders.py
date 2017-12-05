import urllib2
import json

from urlparse import urlparse
from difflib import SequenceMatcher

def uri_validator(x):
    try:
        result = urlparse(x)
        return result.scheme and result.netloc and result.path
    except:
        return False

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.8

class TvOnlineAPP:
    URL = "http://www.apps4two.com/apps/tvonline/ch_channel.php"
    def __init__(self):
        response = urllib2.urlopen(self.URL)
        self.responseText = response.read()
        self.channelList = list(eval(self.responseText))

    def retrieveList(self):
        processedChannelList = []
        for channel in self.channelList:
            processedChannelList.append([channel[5], channel[7].replace('\/','/')])
        return processedChannelList


class GitHubJSON:
    URL = "https://raw.githubusercontent.com/ruvelro/TV-Online-TDT-Spain/master/tv-spain.json"
    def __init__(self, includeDisabled = False):
        response = urllib2.urlopen(self.URL)
        self.responseText = response.read()
        self.channelList = json.loads(self.responseText)
	self.includeDisabled =includeDisabled

    def retrieveList(self):
        processedChannelList = []
        for channel in self.channelList:
            if self.includeDisabled or channel['enabled'] == True:
                processedChannelList.append([channel['name'].encode('UTF-8'), channel['link_m3u8'].encode('ascii')])
        return processedChannelList


class GitHubMD:
    URL = "https://raw.githubusercontent.com/ruvelro/TV-Online-TDT-Spain/master/README.md"
    def __init__(self):
        response = urllib2.urlopen(self.URL)
        self.responseText = response.read()
        
    def retrieveList(self):
        processedChannelList = []
        # Parse the readme.md
        # get to the list
        header, channelList = self.responseText.split('--- | ---')

        # Split for each row
        for channel in channelList.split('\n'):
            # This delimits a element in the list
            if '|' in channel:	
                channelName , channelURL = channel.split('|')
                # Remove annoying first space
                channelURL=channelURL[1:]
                if uri_validator(channelURL):
                    processedChannelList.append([channelName, channelURL])
        
        return processedChannelList

''' Method for comparing the information provided by 2 channel providers '''
def CheckChannelList(list1, list2):
    for channel in list1:
        for searchchannel in list2:
            if similar(channel[0], searchchannel[0]) and channel[1] != searchchannel[1]:
                print("\nChannel description matches for \""+channel[0]+"\" and \""+searchchannel[0]+"\" But URL...")
                print("\t"+ channel[1])
                print("\t"+ searchchannel[1])


if __name__ == "__main__":
    #cp1 = TvOnlineAPP()
    #cp2 = GitHubMD()
    cp2 = GitHubJSON(True)
    print(cp2.retrieveList())
    #CheckChannelList(cp1.retrieveList(), cp2.retrieveList())
