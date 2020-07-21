from lxml import html
import requests
from urllib.request import Request, urlopen

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Rectangle, Color
from kivy.uix.widget import Widget
from kivy.uix.anchorlayout import AnchorLayout

from kivy.config import Config

Config.set('graphics', 'width', 850)
Config.set('graphics', 'height', 1000)

not_read = []
not_read_counter = 0
no_of_manga = 0
manga_imgs = []
manga_imgs_counter = 0
global g_var


def func_find_daily_chaps():
    # Mangakakalot
    url_counter = 0
    url_list = ['https://mangakakalot.com/read-lm7ib158504847850',
                'https://mangakakalot.com/read-ox3yk158504833790',
                'https://mangakakalot.com/read-zs6sp158504840280',
                'https://mangakakalot.com/read-uz2ai158504852768',
                'https://mangakakalot.com/manga/ow923334']

    while url_counter < len(url_list):
        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//ul[@class="manga-info-text"]/li/h1/text()')
        chap = tree.xpath('//div[@class="row"]/span/a/text()')
        views = tree.xpath('//div[@class="row"]/span/text()')
        times = tree.xpath('//span/@title')
        imgs_srcs = tree.xpath('//div[@class="manga-info-pic"]/img/@src')
        # print(imgs_srcs)

        start = 0
        count = 1

        chap_clean = []

        for x in range(0, len(chap)):
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(str(chap[x][start_chapter:end_line]).replace("Chapter ", ""))
            else:
                chap_clean.append(str(chap[x][start_chapter:]).replace("Chapter ", ""))



        # Cleans and organizes the data to be in a cleaner form
        if views[0] == '0':
            start = 0
            count = 2
        elif views[1] == '0':
            start = 1
            count = 2
        else:
            start = -1

        for x in range(start, len(views) // 2, 1):
            views.pop(x)

        if start != -1:
            for x in range(start, len(views) // 2, 1):
                views.pop(x)
                chap.pop(x)
        # End of the cleaning


        for x in range(0, len(views)):
            if "day" in views[x] or "days" in views[x]:
                if int(str(views[x][0:1])) < 2:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in views[x] or "hours" in views[x]:
                if int(str(views[x][0:2])) < 24:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "mins" in views[x] or "min" in views[x] or "minutes" in views[x] or "minute" in views[x]:
                if int(str(views[x][0:1])) < 60:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break

        for x in range(0, len(views)):
            if "day" in views[x] or "days" in views[x]:
                if int(str(views[x][0:1])) < 2:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(views[x])
                    not_read.append(views[x])
            elif "hour" in views[x] or "hours" in views[x]:
                if int(str(views[x][0:2])) < 24:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(views[x])
                    not_read.append(views[x])
            elif "mins" in views[x] or "min" in views[x] or "minutes" in views[x] or "minute" in views[x]:
                if int(str(views[x][0:1])) < 60:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(views[x])
                    not_read.append(views[x])

        # print('Date: ', views)

        url_counter += 1;

    # Leviatan|Zero Scans|Reaper Scans

    url_counter = 0
    url_list = ['https://leviatanscans.com/comics/i-am-the-sorcerer-king/',
                'https://leviatanscans.com/comics/chronicles-of-heavenly-demon',
                'https://leviatanscans.com/comics/157887-a-returners-magic-should-be-special/',
                'https://leviatanscans.com/comics/866673-the-descent-of-the-demonic-master',
                'https://leviatanscans.com/comics/209074-slave-b',
                'https://leviatanscans.com/comics/656006-auto-hunting',
                'https://leviatanscans.com/comics/246282-medical-return',
                'https://leviatanscans.com/comics/11268-survival-story-of-a-sword-king-in-a-fantasy-world',
                'https://leviatanscans.com/comics/337225-the-rebirth-of-the-demon-god',
                'https://zeroscans.com/comics/204586-omniscient-readers-point-of-view',
                'https://zeroscans.com/comics/55416-record-of-the-war-god',
                'https://zeroscans.com/comics/133460-yong-heng-zhi-zun',
                'https://reaperscans.com/comics/915623-god-of-blackfield',
                'https://reaperscans.com/comics/140270-the-great-mage-returns-after-4000-years']

    while url_counter < len(url_list):
        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//h5[@class="text-highlight"]/text()')
        manga_clean = str(manga).replace("\\n", "")
        manga_clean = manga_clean.replace("'", "")
        manga_clean = manga_clean.replace("[", "")
        manga_clean = manga_clean.replace("]", "")
        manga_clean = manga_clean.replace('"', "")

        chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')

        for x in range(0, len(chap)):
            chap[x] = "Chapter " + str(chap[x]).replace("\n", "")

        chap_clean = []

        for x in range(0, len(chap)):
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(str(chap[x][start_chapter:end_line]).replace("Chapter ", ""))
            else:
                chap_clean.append(str(chap[x][start_chapter:]).replace("Chapter ", ""))


        dates = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')

        for x in range(0, len(dates)):
            dates[x] = str(dates[x]).replace("\n", " ")

        imgs_srcs = tree.xpath('//a[@class="media-content"]/@style')

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
                    # print("\n")
                    # print(manga_clean, end="\n")
                    not_read.append("s")
                    not_read.append(manga_clean)
                    if "leviatan" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://zeroscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    manga_imgs.append(imgs_srcs)
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    # print("\n")
                    # print(manga_clean, end="\n")
                    not_read.append("s")
                    not_read.append(manga_clean)
                    if "leviatan" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://zeroscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    manga_imgs.append(imgs_srcs)
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    # print("\n")
                    # print(manga_clean, end="\n")
                    not_read.append("s")
                    not_read.append(manga_clean)
                    if "leviatan" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://zeroscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    manga_imgs.append(imgs_srcs)
                    break

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])

        # print(manga_clean)
        # print(chap)
        # print(dates)
        # print('\n')
        url_counter += 1

    # Manganelo
    url_counter = 0
    url_list = ['https://manganelo.com/manga/xn921310', 'https://manganelo.com/manga/apotheosis',
                'https://manganelo.com/manga/huku267071576897767', 'https://manganelo.com/manga/hyer5231574354229',
                'https://manganelo.com/manga/read_boku_no_hero_academia_manga',
                'https://manganelo.com/manga/read_one_punch_man_manga_online_free3',
                'https://manganelo.com/manga/black_clover', 'https://manganelo.com/manga/uaxz925974686',
                'https://manganelo.com/manga/dnha19771568647794', 'https://manganelo.com/manga/doulou_dalu_manga',
                'https://manganelo.com/manga/pn918005', 'https://manganelo.com/manga/ad921253',
                'https://manganelo.com/manga/dz919342', 'https://manganelo.com/manga/wu_dong_qian_kun']

    while url_counter < len(url_list):

        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//div[@class="story-info-right"]/h1//text()')
        chap = tree.xpath('//a[@class="chapter-name text-nowrap"]/text()')
        dates = tree.xpath('//span[@class="chapter-time text-nowrap"]/text()')
        imgs_srcs = tree.xpath('//span[@class="info-image"]/img/@src')

        chap_clean = []

        for x in range(0, len(chap)):
            if "Chapter" in chap[x]:
                start_chapter = chap[x].find("Chapter")

                if ":" in chap[x]:
                    end_line = chap[x].find(":")
                    chap_no = str(chap[x][start_chapter:end_line]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                elif " -" in chap[x]:
                    end_line = chap[x].find(" -")
                    chap_no = str(chap[x][start_chapter:end_line]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                else:
                    chap_no = str(chap[x][start_chapter:]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
            else:
                chap_clean.append("SC")


        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:1])) < 60:
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap_clean[x])
                    # print(dates[x])
                    not_read.append(dates[x])

        # print(manga)
        # print(chap)
        # print(dates)

        # print("\n")
        url_counter += 1

    """
    # Mangatx
    url_counter = 0
    url_list = ['https://mangatx.com/manga/battle-through-the-heavens/',
                'https://mangatx.com/manga/wu-dong-qian-kun/']

    while url_counter < len(url_list):

        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//div[@class="post-title"]/h1//text()')
        manga = str(manga[0]).replace("\n", "")
        manga = str(manga).replace("\t", "")

        chap = tree.xpath('//li[@class="wp-manga-chapter  "]/a/text()')
        for x in range(0, len(chap)):
            chap[x] = str(chap[x]).replace("\n", "")
            chap[x] = str(chap[x]).replace("\t", "")

        chap_clean = []

        for x in range(0, len(chap)):
            if "Chapter" in chap[x]:
                start_chapter = chap[x].find("Chapter")

                if ":" in chap[x]:
                    end_line = chap[x].find(":")
                    chap_no = str(chap[x][start_chapter:end_line]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                elif " -" in chap[x]:
                    end_line = chap[x].find(" -")
                    chap_no = str(chap[x][start_chapter:end_line]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                else:
                    chap_no = str(chap[x][start_chapter:]).replace("Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
            else:
                chap_clean.append("SC")

        print(chap_clean)

        dates = tree.xpath('//span[@class="chapter-release-date"]/i/text()')
        for x in range(0, len(dates)):
            dates[x] = str(dates[x]).replace("\n", "")
            dates[x] = str(dates[x]).replace("\t", "")

        imgs_srcs = tree.xpath('//img[@class="img-responsive effect-fade ls-is-cached lazyloaded"]/@src')

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    # print("\n")
                    # print(manga, end="\n")
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap[x])
                    # print(dates[x])
                    not_read.append(dates[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    # print(chap[x] + " |", end=" ")
                    not_read.append(chap[x])
                    # print(dates[x])
                    not_read.append(dates[x])

        # print(manga)
        # print(chap)
        # print(dates)
        url_counter += 1
        """


def func_find_imgs_manga_active():
    for x in range(0, no_of_manga):
        req = Request(manga_imgs[x], headers={'User-Agent': 'Mozilla/5.0'})
        # print(manga_imgs[x])

        # if no update pop up no update
        name = str(x) + ".jpg"
        f = open(name, "wb")
        f.write(urlopen(req).read())
        f.close()


func_find_daily_chaps()

for item in not_read:
    if str(item) == "s":
        print("\n")
        no_of_manga += 1
    else:
        print(item, end="|")

func_find_imgs_manga_active()


#ScrollView > GridLayout(cols=3) > ____Layout > Button (takes up the whole page) >

class BabyGrids2(GridLayout):
    def __init__(self):
        GridLayout.__init__(self, rows=3)

        #self.add_widget(Button(text="hi"))

        # self.add_widget(Label(text="hi", pos_hint={'x': 0, 'top': 1}))
        self.add_widget(Button(size_hint=(1,1)))





class BabyGrids(FloatLayout):
    def __init__(self, title, name_pic):
        FloatLayout.__init__(self)

        #img = Image(source="1.jpg")
        #self.add_widget(img)
        #self.add_widget(BabyGrids2())
        img = Image(source=name_pic, allow_stretch=True, keep_ratio=False, pos_hint={'x': 0, 'top': 1})
        self.add_widget(img)
        print(title)
        self.add_widget(Button(text=title[0], pos_hint={'x':0, 'top': 1}, size_hint=(1, 0.25), font_size='15sp', background_color=(0,0,0,0.4)))
        self.add_widget(Button(pos_hint={'x': 0, 'top': 0.6}, size_hint=(1, 0.3)))
        self.add_widget(Button(pos_hint={'x': 0, 'top': 0.3}, size_hint=(1, 0.3)))
        #self.add_widget(BabyGrids2())
        #self.add_widget(Button())




class MainGrid(GridLayout):
    def __init__(self):
        GridLayout.__init__(self, cols=3, row_force_default="True", row_default_height=400, height=self.minimum_height,
                            size_hint=(1, None))
        self.bind(minimum_height=self.setter('height'))

        counter = 0

        name_chapter_time = []
        x = 0

        for y in range(0, no_of_manga):
            if not_read[x] == "s":
                x += 1

            while not_read[x] != "s":
                name_chapter_time.append(not_read[x])
                name_chapter_time.append("\n")
                if x + 1 < len(not_read):
                    x += 1
                else:
                    break

            # layout.add_widget(Button(text=name_chapter_time))
            name2 = str(y) + ".jpg"
            img = Image(source=name2, allow_stretch=True, keep_ratio=False)
            #self.add_widget(img)
            self.add_widget(BabyGrids(name_chapter_time, name2))
            name_chapter_time = []


class ScrollBarView(ScrollView):
    def __init__(self):
        ScrollView.__init__(self, do_scroll_x="False", do_scroll_y="True", size=self.size, scroll_type=['bars'])
        self.add_widget(MainGrid())


class WebParseApp(App):
    def build(self):
        return ScrollBarView()


WebParseApp().run()

# if first is 0 then go in odd, else in even, else dont change
# i can check whatever i have not read and start counting from today
# how do i save what i have not read
