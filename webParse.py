from lxml import html
import requests

#Mangakakalot
urlCount = 0
urlList = ['https://mangakakalot.com/read-lm7ib158504847850', 'https://mangakakalot.com/read-ox3yk158504833790',
            'https://mangakakalot.com/read-zs6sp158504840280', 'https://mangakakalot.com/read-uz2ai158504852768',
            'https://mangakakalot.com/manga/ow923334']

while urlCount < len(urlList):
    page = requests.get(urlList[urlCount])
    tree = html.fromstring(page.content)

    manga = tree.xpath('//ul[@class="manga-info-text"]/li/h1/text()')
    chap = tree.xpath('//div[@class="row"]/span/a/text()')
    views = tree.xpath('//div[@class="row"]/span/text()')
    times = tree.xpath('//span/@title')

    start = 0
    count = 1

    # Cleans and organizes the data to be in a cleaner form
    if views[0] == '0':
        start = 0
        count = 2
    elif views[1] == '0':
        start = 1
        count = 2
    else:
        start = -1

    for x in range(start,len(views)//2,1):
        views.pop(x)

    if start != -1:
        for x in range(start,len(views)//2,1):
            views.pop(x)
            chap.pop(x)
    # End of the cleaning


    for x in range(0, len(views)):
        if "day" in views[x] or "days" in views[x]:
            if int(str(views[x][0:1])) < 2:
                print("\n")
                print(manga, end="\n")
                break
        elif "hour" in views[x] or "hours" in views[x]:
            if int(str(views[x][0:2])) < 24:
                print("\n")
                print(manga, end="\n")
                break


    for x in range(0, len(views)):
        if "day" in views[x] or "days" in views[x]:
            if int(str(views[x][0:1])) < 2:
                print(chap[x] + " |", end=" ")
                print(views[x])
        elif "hour" in views[x] or "hours" in views[x]:
            if int(str(views[x][0:2])) < 24:
                print(chap[x] + " |", end=" ")
                print(views[x])



    #print('Date: ', views)

    urlCount += 1;

"""
#Leviatan|Zero Scans|Reaper Scans

urlCount = 0
urlList = ['https://leviatanscans.com/comics/i-am-the-sorcerer-king/', 'https://leviatanscans.com/comics/chronicles-of-heavenly-demon',
           'https://leviatanscans.com/comics/157887-a-returners-magic-should-be-special/', 'https://leviatanscans.com/comics/866673-the-descent-of-the-demonic-master',
           'https://leviatanscans.com/comics/209074-slave-b', 'https://leviatanscans.com/comics/656006-auto-hunting',
           'https://leviatanscans.com/comics/246282-medical-return', 'https://leviatanscans.com/comics/11268-survival-story-of-a-sword-king-in-a-fantasy-world',
           'https://leviatanscans.com/comics/337225-the-rebirth-of-the-demon-god', 'https://zeroscans.com/comics/204586-omniscient-readers-point-of-view',
           'https://zeroscans.com/comics/55416-record-of-the-war-god', 'https://zeroscans.com/comics/188504-second-life-ranker',
           'https://zeroscans.com/comics/133460-yong-heng-zhi-zun', 'https://reaperscans.com/comics/915623-god-of-blackfield',
           'https://reaperscans.com/comics/140270-the-great-mage-returns-after-4000-years']

while urlCount < len(urlList):
    page = requests.get(urlList[urlCount])
    tree = html.fromstring(page.content)

    manga = tree.xpath('//h5[@class="text-highlight"]/text()')
    manga_clean = str(manga[0]).replace("\n","")

    chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')

    for x in range(0, len(chap)):
        chap[x] = "Chapter " + str(chap[x]).replace("\n","")

    date = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')

    for x in range(0, len(date)):
        date[x] = str(date[x]).strip("\n")


    print(manga_clean)
    print(chap)
    print(date)
    print('\n')
    urlCount += 1
"""
"""
#Manganelo
urlCount = 0
urlList = ['https://manganelo.com/manga/xn921310', 'https://manganelo.com/manga/apotheosis',
           'https://manganelo.com/manga/huku267071576897767','https://manganelo.com/manga/hyer5231574354229',
           'https://manganelo.com/manga/read_boku_no_hero_academia_manga', 'https://manganelo.com/manga/read_one_punch_man_manga_online_free3',
           'https://manganelo.com/manga/black_clover', 'https://manganelo.com/manga/uaxz925974686', 'https://manganelo.com/manga/dnha19771568647794'
           ,'https://manganelo.com/manga/doulou_dalu_manga','https://manganelo.com/manga/pn918005']

while urlCount < len(urlList):

    page = requests.get(urlList[urlCount])
    tree = html.fromstring(page.content)

    manga = tree.xpath('//div[@class="story-info-right"]/h1//text()')
    chaps = tree.xpath('//a[@class="chapter-name text-nowrap"]/text()')
    dates = tree.xpath('//span[@class="chapter-time text-nowrap"]/text()')

    print(manga)
    print(chaps)
    print(dates)

    print("\n")
    urlCount += 1
"""
"""
#Mangatx
urlCount = 0
urlList = ['https://mangatx.com/manga/battle-through-the-heavens/', 'https://mangatx.com/manga/wu-dong-qian-kun/']

while urlCount < len(urlList):

    page = requests.get(urlList[urlCount])
    tree = html.fromstring(page.content)

    manga = tree.xpath('//div[@class="post-title"]/h1//text()')
    manga  = str(manga[0]).replace("\n", "")
    manga = str(manga).replace("\t", "")

    chap = tree.xpath('//li[@class="wp-manga-chapter  "]/a/text()')
    for x in range(0, len(chap)):
        chap[x] = str(chap[x]).replace("\n","")
        chap[x] = str(chap[x]).replace("\t","")

    dates = tree.xpath('//span[@class="chapter-release-date"]/i/text()')
    for x in range(0, len(dates)):
        dates[x] = str(dates[x]).replace("\n","")
        dates[x] = str(dates[x]).replace("\t","")

    print(manga)
    print(chap)
    print(dates)

    print("\n")
    urlCount += 1
"""

#if first is 0 then go in odd, else in even, else dont change
#i can check whatever i have not read and start counting from today