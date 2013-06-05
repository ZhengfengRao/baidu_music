#encoding=utf8

import urllib,urllib2,re,cookielib
import os
import time
from bs4 import BeautifulSoup
import socket
import json
from html_string import HtmlString
import db

class BaiduMusic():
    def __init__(self):
        socket.setdefaulttimeout(10)
        self.path = ""
        self.album_path = ""
        self.singers = {}
        self.top_list = {}
        self.top_list[u"dayhot"] = u"歌曲TOP500"
        self.top_list[u"new"] = u"新歌TOP100"
        self.top_list[u"oumei"] = u"欧美金曲榜"
        self.top_list[u"huayu"] = u"华语金曲榜"
        self.top_list[u"yingshijinqu"] = u"影视金曲榜"
        self.top_list[u"lovesong"] = u"情歌对唱榜"
        self.top_list[u"netsong"] = u"网络歌曲榜"
        self.top_list[u"oldsong"] = u"经典老歌榜"
        self.top_list[u"rock"] = u"摇滚榜"
        self.top_list[u"jazz"] = u"爵士榜"
        self.top_list[u"folk"] = u"民谣榜"
        self.top_list[u"ktv"] = u"KTV热歌榜"
        self.top_list[u"billboard"] = u"Billboard"
        self.top_list[u"ukchart"] = u"UK Chart"
        self.top_list[u"hito"] = u"Hito中文榜"
        self.top_list[u"chizha"] = u"叱咤歌曲榜"
        self.record_extra_info = u"No"
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.opener.addheaders = [('User-agent','Opera/9.23')]
        urllib2.install_opener(self.opener)

    def _get_all_singers(self):
        if len(self.singers) != 0:
            return
        singer_urls = ['http://music.baidu.com/artist']
        singer_urls.append('http://music.baidu.com/artist/cn/male')
        singer_urls.append('http://music.baidu.com/artist/cn/female')
        singer_urls.append('http://music.baidu.com/artist/cn/group')
        singer_urls.append('http://music.baidu.com/artist/western/male')
        singer_urls.append('http://music.baidu.com/artist/western/female')
        singer_urls.append('http://music.baidu.com/artist/western/group')
        singer_urls.append('http://music.baidu.com/artist/jpkr/male')
        singer_urls.append('http://music.baidu.com/artist/jpkr/female')
        singer_urls.append('http://music.baidu.com/artist/jpkr/group')
        singer_urls.append('http://music.baidu.com/artist/other')
        for url in singer_urls:
            print url
            count = 0
            singers_page = self._read_url(url)
            soup = BeautifulSoup(singers_page)
            singer_list = soup.findAll('li', attrs={'class': 'list-item'})
            if singer_list:
                for singer in singer_list:
                    arts = singer.findAll('li')
                    for a in arts:
                        art_item = a.find('a')
                        if art_item:
                            if art_item['title'] and art_item['href']:
                                name = art_item['title']
                                self.singers[name] = art_item['href']
                                count = count+1
            print count
        print "singers count = " + str(len(self.singers))
        #print self.singers


    def _login(self,username,password):
        get_api_url = 'http://passport.baidu.com/v2/api/?getapi&class=login&tpl=music&tangram=false'

        req = urllib2.Request(get_api_url)
        urllib2.urlopen(req)

        req = urllib2.Request(get_api_url)
        page = urllib2.urlopen(req)
        c = page.read()

        tokent_regex = re.compile('''bdPass\.api\.params\.login_token='(.*?)';''',re.DOTALL)
        match = tokent_regex.findall(c)
        if match :
            self.token = match[0]
        else :
            print u"登陆失败"
            return

        login_url = 'https://passport.baidu.com/v2/api/?login'
        params = {}
        params['charset'] = 'UTF-8'
        params['codestring'] = ''
        params['token'] = self.token
        params['isPhone'] = 'false'
        params['index'] = '0'
        params['u'] = ''
        params['safeflg'] = '0'
        params['staticpage'] = 'pass_jump.html'
        params['loginType'] = '1'
        params['tpl'] = 'music'
        params['callback'] = 'callback'
        params['username'] = username
        params['password'] = password
        params['verifycode'] = ''
        params['mem_pass'] = 'on'
        req = urllib2.Request(login_url)
        page = urllib2.urlopen(req,urllib.urlencode(params))
        c = page.read()

    def _read_url(self,url):
        fails = 0
        while(True):
            req = urllib2.Request(url)
            try:
                if fails >= 10:
                    exit(0)
                page = urllib2.urlopen(req,None,timeout=5)
                c = page.read()
                regex = re.compile('''verify.baidu.com''')
                match = regex.findall(c)
                if match :
                    regex = re.compile('''name=[ \S]+value=[ \S]+"''')
                    match = regex.findall(c)
                    if match :
                        before_url = match[0][match[0].find("value=")+6:].strip()
                        before_url = before_url.replace("\"","")
                        vcode = match[1][match[1].find("value=")+6:].strip()
                        vcode = vcode.replace("\"","")
                        id = match[2][match[2].find("value=")+6:].strip()
                        id = id.replace("\"","")
                        di = match[3][match[3].find("value=")+6:].strip()
                        di = di.replace("\"","")
                        image_url = "http://verify.baidu.com/cgi-bin/genimg?" + vcode
                        verify_url = "http://verify.baidu.com/verify?url=" + before_url+"&vcode="+vcode+"&id="+id+"&di="+di+"&verifycode="
                        try:
                            data = urllib2.urlopen(image_url).read()
                            f = file(self.album_path + os.sep + 'genimg.jpg',"wb")
                            f.write(data)
                            f.close()
                        except Exception, e:
                            print e.message
                        verify_code = self.dlg.verify(self.album_path + os.sep + 'genimg.jpg')
                        if verify_code == u"":
                            continue
                        verify_url = verify_url + verify_code
                        os.remove(self.album_path + os.sep + 'genimg.jpg')
                        data = urllib2.urlopen(verify_url).read()
                else:
                    break
            except Exception, e:
                print "[Error]_read_url():"+e.message+", " + url
                fails += 1
                time.sleep(5)
        return c

    def _replace_special_str(self,str):
        str = str.replace(u"?",u"？")
        str = str.replace(u'\\', u'_')
        str = str.replace(u'/', u'_')
        str = str.replace(u':', u'_')
        str = str.replace(u'*', u'_')
        str = str.replace(u'\"', u'_')
        str = str.replace(u'<', u'_')
        str = str.replace(u'>', u'_')
        str = str.replace(u'|', u'_')

        if str.find(u'&') != -1:
            for ch in HtmlString:
                str = str.replace(ch, HtmlString[ch])
        return str

    def _set_save_path(self,path):
        self.path = path

    def _get_command_field(self,command,opt):
        if command.find(opt) == -1:
            return u""
        end = command.find(u"-",command.find(opt)+1)
        if end != -1:
            return command[command.find(opt)+3:command.find(u"-",command.find(opt)+1)-1].strip()
        return command[command.find(opt)+3:].strip()

    def _download_top(self,type):
        content = self._read_url(u"http://music.baidu.com/top/" + type)
        soup = BeautifulSoup(content)
        obj = soup.find("div", attrs={'class': 'head clearfix'}).find('h2')
        if obj:
            title = obj.text.strip()
            title = self._replace_special_str(title)
            current_path = self.path + title + os.sep
            if not os.path.exists(current_path):
                os.makedirs(current_path)
            self.album_path = current_path
        else:
            print u"没有发现此榜单"
            return
        self._download_page_songs(current_path, soup)

    def invoke_command(self,command):
        user = self._get_command_field(command,u"-u")
        if(user == ""):
            user = "baidu_crawler@sohu.com"
        password = self._get_command_field(command,u"-p")
        if(password == ""):
            password = "aa123456"
        path = self._get_command_field(command,u"-d")

        singer_parameters = self._get_command_field(command,u"-s")
        list_parameters = self._get_command_field(command,u"-l")
        album_parameters = self._get_command_field(command,u"-a")
        info_parameters = self._get_command_field(command,u"-i")

        if info_parameters == u"1":
            self.record_extra_info = u"Yes"
            self.localdb = db.db()

        if user != u"" and password != u"":
            self._login(user, password);

        if path == u"":
            path = u"."
        if not path.endswith(os.sep):
            path += os.sep

        self._set_save_path(path)
        if singer_parameters != u"":
            self._get_all_singers();
            if singer_parameters == u"all":
                for name in self.singers:
                    self._download_singer(name,"")
            else:
                singer_list = singer_parameters.split(u",")
                for name in singer_list:
                    if name not in self.singers.keys():
                        print u"没有发现此歌手: " + name
                        continue
                    self._download_singer(name, "")

        if list_parameters != u"":
            if list_parameters == u"all":
                for i in self.top_list.keys():
                    print ""
                    self._download_top(i)
            else:
                top_lists = list_parameters.split(u",")
                for i in top_lists:
                    print ""
                    self._download_top(i.strip())

        if album_parameters != u"":
            self._get_all_singers();
            name_album_list = album_parameters.split(u",")
            for i in name_album_list:
                name_album = i.split(u":")
                if len(name_album) == 2:
                    self._download_singer(name_album[0],name_album[1])

        print u"全部完成"

    def setUI(self,dlg):
        self.dlg = dlg

    def _download_singer(self,singer_name,match_album_name = ""):
        url = "http://music.baidu.com" + self.singers[singer_name]
        print "------------------Artist:"+singer_name+",     "+url
        # check singer name
        if singer_name not in self.singers.keys():
            print u"没有发现此歌手: " + singer_name
            return

        # create path
        singer_name = singer_name.strip()
        singer_name = self._replace_special_str(singer_name)
        current_path = self.path + singer_name
        if not os.path.exists(current_path):
            os.makedirs(current_path)

        content = self._read_url(url)
        soup = BeautifulSoup(content)
        album_node = soup.find('div', attrs={'class': 'album-list'})
        ting_uid = url[url.rfind('/')+1:]
        if not album_node:
            self._download_singer_songs(current_path,soup)
            self._download_singer_songs_nextpage(current_path,ting_uid, soup)
        else:
            if self.record_extra_info == u"Yes":
                self._collect_albums_info(singer_name, soup)
            self._download_album_list(current_path,soup,match_album_name)
            self._download_albums_list_nextpage(singer_name, current_path, ting_uid , soup, match_album_name)

    def _download_album_list(self, current_path,soup,match_album_name = ""):
        albums = soup.find('div', attrs={'class': 'album-list'}).find("ul", attrs={'class': 'clearfix'}).findAll("li");
        for album_name in albums:
            link = album_name.find("div", attrs={'class': 'title clearfix'}).find('a')
            if link['href']:
                album_name = link['title']
                album_name = self._replace_special_str(album_name)
                match_album_name = match_album_name.strip()
                if match_album_name != "" and  album_name != match_album_name:
                    continue
                download_path = current_path + os.sep + album_name
                if not os.path.exists(download_path):
                    os.makedirs(download_path)
                self.album_path = download_path
                url = "http://music.baidu.com"+link['href']
                print u"****Album: " + album_name +",    "+ url
                album_soup = BeautifulSoup(self._read_url(url))
                self._download_album(download_path,album_soup)

    # find & download next page's albums(if have)
    def _download_albums_list_nextpage(self, singer_name, current_path, ting_uid, soup, match_album_name):
        if self.record_extra_info == u"Yes":
            self._collect_albums_info(singer_name, soup)

        all_nextPages = soup.find('div', attrs={'id': 'albumList'}).findAll('a', attrs={'class': 'page-navigator-number         PNNW-S'})
        num_nextPages = len(all_nextPages)
        if num_nextPages  > 0:
            for i in range(0,num_nextPages ):
                i = i+1
                next_url = "http://music.baidu.com/data/user/getalbums?start="
                next_url = next_url + str(i*10)
                next_url = next_url + "&ting_uid=" + ting_uid
                next_url = next_url + "&order=time"
                try:
                    jsonObj = json.JSONDecoder().decode(self._read_url(next_url))
                    html = jsonObj['data']['html']
                    if html:
                        next_soup = BeautifulSoup(html)
                        self._download_album_list(current_path, next_soup, match_album_name)
                    else:
                        print "[Error]_download_albums_list_nextpage():No section [\'data\'][\'html\'] found in json","url:",next_url
                except Exception, e:
                    print "[Error]_download_albums_list_nextpage():",e,"url:",next_url

    def _download_album(self,current_path, soup):
        self._download_page_songs(current_path,soup)

    def _download_singer_songs(self,current_path,soup):
        self._download_page_songs(current_path,soup)

    def _download_singer_songs_nextpage(self,current_path,ting_uid,soup):
        try:
            all_nextPages = soup.find('div', attrs={'class': 'ui-tab-content songs-list'}).findAll('a', attrs={'class': 'page-navigator-number         PNNW-S'})
            num_nextPages = len(all_nextPages)
            if num_nextPages  > 0:
                for i in range(0,num_nextPages ):
                    i = i+1
                    next_url = "http://music.baidu.com/data/user/getsongs?start="
                    next_url = next_url + str(i*20)
                    next_url = next_url + "&ting_uid=" + ting_uid
                    next_url = next_url + "&order=hot"
                    jsonObj = json.JSONDecoder().decode(self._read_url(next_url))
                    html = jsonObj['data']['html']
                    if html:
                        next_soup = BeautifulSoup(html)
                        self._download_page_songs(current_path, next_soup)
                    else:
                        print "[Error]_download_singer_songs_nextpage():No section [\'data\'][\'html\'] found in json","url:",next_url
        except Exception, e:
            print "[Error]_download_singer_songs_nextpage():",e

    def _collect_albums_info(self,artist, pageSoup):
        try:
            infoItems = pageSoup.findAll('div', attrs={'class': 'album-info'})
            for infoItem in infoItems:
                id = ''
                title = ''
                releasedate = ''
                genres = ''
                company = ''
                description = ''

                titleItem = infoItem.find('div', attrs={'class': 'title clearfix'})
                if titleItem:
                    title_link = titleItem.find('a')
                    if title_link:
                        title = title_link['title']
                        uri = title_link['href']
                        id = uri[uri.rfind('/')+1:]

                activeItem = infoItem.find('div', attrs={'class': 'album-active'})
                if activeItem:
                    time_link = activeItem.find('span', attrs={'class': 'time'})
                    if time_link:
                        releasedate = time_link.text

                    genres_link = activeItem.find('span', attrs={'class': 'styles'})
                    if genres_link:
                        genres = genres_link.text

                    company_link = activeItem.find('span', attrs={'class': 'company'})
                    if company_link:
                        company = company_link.text

                descpritionItem = infoItem.find('div', attrs={'class': 'desc'})
                if descpritionItem:
                    description = self._replace_special_str(descpritionItem.text.strip())

                if id != '' and title != '':
                    self.localdb.add_album(id, title, artist, releasedate, genres, company, description)
        except Exception, e:
            print "[Error]_collect_albums_info():"+e.message

    def _download_page_songs(self,current_path, soup):
        songItems = soup.findAll('div', attrs={'class': 'song-item'})
        for item in songItems :
            obj = item.find('span', attrs={'class': 'song-title '})
            if obj:
                music = obj.find('a')
                if music:
                    music_name = music['title']
                    if music_name.find(u"审批文号") != -1:
                        music_name = music_name[:music_name.find(u"审批文号")]
                    music_name = self._replace_special_str(music_name)
                    music_id = music['href'].replace('/song/', '')
                    if not os.path.isfile(current_path + os.sep + music_name +'.mp3'):
                        self._download_music(current_path,music_name, music_id)

    def _download_music(self,current_path,music_name, music_id):
        url = 'http://music.baidu.com/song/' + music_id + '/download'
        content = self._read_url(url)
        regex = re.compile('''"high-rate" data-data = '{"rate\S+}''')
        match = regex.findall(content)
        mp3_url = ""
        if match :
            regex = re.compile('''http\S+[\w]''')
            match = regex.findall(match[0])
            if match:
                mp3_url = match[0].replace('\\','')
                print u"下载 " + music_name + " (高品质)" + url
        else :
            regex = re.compile('''=http://\S+[\w]''')
            match = regex.findall(content)
            if match:
                mp3_url = match[0][1:]
                print u"下载 " + music_name + "   "+ url

        if mp3_url == "":
            print music_name + u" 没有找到"
            return

        return
        self._download_file(mp3_url, current_path + os.sep + music_name +'.mp3')
        self._download_lyrics(current_path,music_name, music_id)

    def _download_file(self, url, localfile):
        try:
            with open(localfile, 'wb') as file_handle:
                file_handle.write(self._read_url(url))
        except Exception, e:
            print e.message

    def _download_lyrics(self,current_path,music_name, music_id):
        url = 'http://music.baidu.com/song/' + music_id + '/lyric'
        content = self._read_url(url)
        lrcSoup = BeautifulSoup(content)
        downloadItem = lrcSoup.find('a', attrs={'class': 'down-lrc-btn'})
        if downloadItem:
            download_url = downloadItem['href']
            self._download_file(download_url, current_path + os.sep + music_name + '.lrc')

def main():
    baidu_music = BaiduMusic()
    baidu_music.invoke_command(u"-s all -d music -i 1 -u **** -p ******")

if __name__ == '__main__':
    main()
