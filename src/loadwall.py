## vk wall download script
## extracting direct picture links from html webpages
## full-size pictures, not only thumbnail images!
##

import re
import os
import urllib.request
import time
import random
import collections

#=================================== CONFIG ===================================#
# if you want to save links from all .html files into one large .txt file
# switch to True
# if you want to save links from each .html file in separate .txt file
# switch to False
ONE_FILE = True

# Do you want to extract thumbnail pics?
EX_THUMBS = True

# Do you want to extract gif pages?
EX_GIFS = True
#==============================================================================#

# USER AGENTS
UA = (
    'Mozilla/2.0 (compatible; MSIE 6.0; Windows NT 5.2)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; Hotbar 4.1.8.0; RogueCleaner; Alexa Toolbar)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Maxthon)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)Opera/9.20 (Windows NT 5.1; U)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; Alexa Toolbar)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; WOW64; Trident/6.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729;',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; BTRS100200; MRA 5.10 (build 5288); .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; MRSPUTNIK 2, 4, 1, 138; MRA 6.2 (build 7314); InfoPath.1; .NET CLR 2.0.50727; .NET CLR',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET4.0C; .NET4.0E)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; eSobiSubscriber 2.0.4.16)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Win32; Trident/5.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media C',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; chromeframe; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729;',
    'Mozilla/4.0 (Compatible; Windows NT 5.1; MSIE 6.0) (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/4.1; DragonFly) KHTML/4.1.4 (like Gecko)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; Touch; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; NOKIA; Lumia 920)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center P',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; LSY; DLHA; DBASE; CloudClient; W2K8R2; NN; C; IE9; CXA_HR-dBA20_AI-PLT1-TEST_XA',
    'Mozilla/5.0 (Linux; Ubuntu 14.04 like Android 4.4) AppleWebKit/537.36 Chromium/35.0.1870.2 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.42 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) QuickLook/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.13 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.12 (KHTML, like Gecko) Maxthon/3.0 Chrome/26.0.1410.43 Safari/535.12',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1',
    'Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.699.0 Safari/534.24',
    'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7',
    'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36 OPR/24.0.1558.64',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:27.0) Gecko/20100101 Firefox/27.0',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E;',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; ',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1707.221 Amigo/32.0.1707.221 MRCHROME SOC Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:27.0) Gecko/20100101 Firefox/27.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; eSobiSubscrib',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NE',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1700.102 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/22.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.59 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.122 Safari/537.36 OPR/24.0.1558.64',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729; McAfee; BRI/2; Tablet',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 (FM Scene 4.6.1)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1b3) Gecko/20090305 Firefox/3.1b3',
    'Mozilla/5.0 (X11; CrOS x86_64 6310.7.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.11 Safari/537.36',
    'Mozilla/5.0 (X11; Linux) AppleWebKit/538.1+ Midori/0.5',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
    'Mozilla/5.0 (X11; Linux i686; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.34 Safari/534.24',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.19 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.37 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/28.0.1500.52 Chrome/28.0.1500.52 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/37.0.2062.120 Chrome/37.0.2062.120 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20121202 Firefox/17.0 Iceweasel/17.0.1',
    'Mozilla/5.0 (X11; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0 SeaMonkey/2.30',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:22.0) Gecko/20100101 Firefox/22.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.9) Gecko/20071025 Firefox/2.0.0.9',
    'Mozilla/6.0 (compatible; AppleWebKit/latest; like Gecko/20120405; };-&gt; infernal_edition:goto-hell) Firefox/666',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.10.0) Presto/2.12.388 Version/12.16',
    'Opera/9.80 (X11; Linux zvav; U; ru) Presto/2.8.119 Version/11.10'
)               

class URLopener(urllib.request.FancyURLopener):
    version = None

    def __init__(self):
        self.version = random.choice(UA)
        urllib.request.FancyURLopener.__init__(self)
        
def pause(milisec):
    time.sleep(milisec/1000.0)

def get_html(url):
    opener = URLopener()
    page = opener.open(url)
    pause(500)
    page_text = page.read().decode('cp1251', 'replace')

    return page_text

def get_wall_url(txt):
    WALL_ID_RE = re.compile('href="/wall-(\d*?)_\d*?')
        
    wall_id = WALL_ID_RE.findall(txt)[0]
    print('wall id:', wall_id)
    
    wall_url = 'http://vk.com/wall-' + wall_id + '?own=1'
    return wall_url

def save_links(lst, filename):
    lst.append('')
    txt = '\n'.join(lst)
    with open(filename, 'w') as lst_f:
        lst_f.write(txt)

def get_wallpages(url):
    gr_page_html = get_html(url)
    wall_url = get_wall_url(gr_page_html)
    wall_html = get_html(wall_url)

    WALL_PAGE_OFFSET_RE = re.compile('href="/wall-\d*?[?]own=1(?:&amp;|&)offset=(\d*?)"')

    wall_page_offsets = WALL_PAGE_OFFSET_RE.findall(wall_html)
    last = int(wall_page_offsets[-1])

    STEP = 20
    wall_page_urls = []
    for i in range(0, last+STEP, STEP):
        wall_page = wall_url + '&offset=%s'%i
        wall_page_urls.append(wall_page)

    save_links(wall_page_urls, 'wall_pages.txt')

    return wall_page_urls

def clean_dir(path):
    for item in os.listdir(path):
        item_fullpath = os.path.join(path, item)
        os.remove(item_fullpath)

def load_wallpages(lst):
    pages_path = os.path.join(os.path.abspath(os.path.curdir), 'pages')

    clean_dir(pages_path)
    
    count = 1
    for page_url in lst:
        print('loading %s of %s'%(count, len(lst)))
        page_html = get_html(page_url)
        pause(1500)
        page_fullpath = os.path.join(pages_path, str((count-1)*20)+'.html')
        
        with open(page_fullpath, 'w', encoding='cp1251') as pf:
            pf.write(page_html)
        count += 1

def get_fullsize_url(text):
    # find link prefix
    LINK_PREFIX_RE = re.compile('(http[:]//cs\d*?[.]vk[.]me(?:/[c]\d*?){0,1}/[v]\d*?/)')
    link_prefix = LINK_PREFIX_RE.findall(text)[0]

    # find suffixes
    LINK_SUFFIX_RE = re.compile('\\[&quot;(.*?/.*?)&quot;,(\d*?),(\d*?)\\]')
    link_suffix_lst = LINK_SUFFIX_RE.findall(text)

    # find largest by square
    largest  = {
        'size' : 0,
        'suffix' : ''
        }
    
    for (suff, w, h) in link_suffix_lst:
        size = int(w) * int(h)
        if (size > largest['size']):
            largest['size'] = size
            largest['suffix'] = suff

    extension = '.jpg'
    
    link = ''.join([link_prefix, largest['suffix'], extension])

    return link  

def extract_pics(text):
    extracted_pics = []

    SHOW_PHOTO_RE = re.compile('onclick="(return showPhoto.*?)"')
    s_photo_lst = SHOW_PHOTO_RE.findall(text)
    for item in s_photo_lst:
        link = get_fullsize_url(item)
        extracted_pics.append(link)

    return extracted_pics

def uniq_(lst):
    return list(collections.OrderedDict.fromkeys(lst))

def uniq(seq):
    seen = {}
    res = []

    for item in seq:
        if not item in seen:
            seen[item] = 1
            res.append(item)
    return res

def extract_thumbnails(text):
    THUMB_RE = '<img src="(http[:]//cs\d*?[.]vk[.]me(?:/[c]\d*?){0,1}/[v]\d*?/.*?/.*?[.](?:jpg|png))"'
    lst = re.compile(THUMB_RE).findall(text)

    extracted_pics = uniq(lst)

    return extracted_pics 

def extract_gifs(text):
    VK_DOC_PREFIX = 'http://vk.com'
    GIF_REGEX = '<a href="(/doc\d*?_\d*?[?]hash=.*?[&]dl=.*?)"'
    lst = re.compile(GIF_REGEX).findall(text)

    extracted_pics = uniq(lst)
    extracted_pics = list(map(lambda x: VK_DOC_PREFIX + x, extracted_pics))
    
    return extracted_pics

def process_wallpage(text):
    pics = extract_pics(text)
    thumbs = extract_thumbnails(text)
    gifs = extract_gifs(text)

    return pics, thumbs, gifs


def get_pics():
    pics_all = []
    thumbs_all = []
    gifs_all = []
    
    pages_path = os.path.join(os.path.abspath(os.path.curdir), 'pages')
    pics_path = os.path.join(os.path.abspath(os.path.curdir), 'pics')
    clean_dir(pics_path)
    
    files = os.listdir(pages_path)
    html_filtr = lambda f: f.endswith('.htm') or f.endswith('html')
    html_files = list(filter(html_filtr, files))

    count = 1
    total_files = len(html_files)
    for html_file in html_files:
        file_fullpath = os.path.join(pages_path, html_file)
        with open(file_fullpath, 'r', encoding='cp1251') as f:
            html_text = f.read()
        pics, thumbs, gifs = process_wallpage(html_text)
        
        percent = round(count / total_files * 100, 4)
        print('%s : %s links [%s'%(html_file, len(pics), percent), '%]')

        if not ONE_FILE:
            pics_filepath = os.path.join(pics_path, html_file + '_pics.txt')
            save_links(pics, pics_filepath)
            if EX_THUMBS:
                thumbs_filepath = os.path.join(pics_path, html_file + '_thumbs.txt')
                save_links(thumbs, thumbs_filepath)
            if EX_GIFS:
                gifs_filepath = os.path.join(pics_path, html_file + '_gifs.txt')
                save_links(gifs, gifs_filepath)
        else:
            pics_all.extend(pics)
            if EX_THUMBS:
                thumbs_all.extend(thumbs)
            if EX_GIFS:
                gifs_all.extend(gifs)            

        count += 1

    if ONE_FILE:
        pics_all_uniq = uniq(pics_all)
        pics_all_file = os.path.join(pics_path, 'LINKS_ALL.txt')
        save_links(pics_all_uniq, pics_all_file)
        if EX_THUMBS:
            thumbs_all_uniq = uniq(thumbs_all)
            thumbs_all_file = os.path.join(pics_path, 'THUMBS_ALL.txt') 
            save_links(thumbs_all_uniq, thumbs_all_file)
        if EX_GIFS:
            gifs_all_uniq = uniq(gifs_all)
            gifs_all_file = os.path.join(pics_path, 'GIFS_ALL.txt')
            save_links(gifs_all_uniq, gifs_all_file)        

def start(url):
    lst = get_wallpages(url)
    load_wallpages(lst)
    get_pics()

if __name__ == '__main__':
    url = ''
    start(url)

