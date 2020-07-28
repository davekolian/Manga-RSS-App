#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

from lxml import html
import requests
from urllib.request import Request, urlopen

import kivy
kivy.require('1.11.0')

from kivy.config import Config
# Sets Window to: not be resizable, size of 850x1000, not close when 'ESC' key is clicked
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'height', 1000)
Config.set('graphics', 'width', 850)
Config.set('kivy', 'exit_on_escape', 0)

import os

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import mainthread
from functools import partial

# Global Variables
not_read = []
no_of_manga = 0
manga_imgs = []
chapter_links = []
loading = 1
chapt = []  # list of all recent chapters
chapters = []  # list of all links to chapters in same order as chapt
url_counter = 0


# Function which creates a batch file to open the manga chapter in my browser of choice
def func_create_batch_files(link):
    f = open("open_manga.bat", "w")
    code = "start firefox.exe " + link
    f.write(code)
    f.close()

    os.system("open_manga.bat")


# Function which scrapes the websites to find which chapters have been newly released
def func_find_daily_chaps():
    global not_read
    global manga_imgs
    global chapter_links



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
        links = tree.xpath('//div[@class="row"]/span/a/@href')

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
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in views[x] or "hours" in views[x]:
                if int(str(views[x][0:2])) < 24:
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "mins" in views[x] or "min" in views[x] or "minutes" in views[x] or "minute" in views[x]:
                if int(str(views[x][0:1])) < 60:
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break

        for x in range(0, len(views)):
            if "day" in views[x] or "days" in views[x]:
                if int(str(views[x][0:1])) < 2:
                    not_read.append(chap_clean[x])
                    not_read.append(views[x])
                    chapter_links.append(links[x])
            elif "hour" in views[x] or "hours" in views[x]:
                if int(str(views[x][0:2])) < 24:
                    not_read.append(chap_clean[x])
                    not_read.append(views[x])
                    chapter_links.append(links[x])
            elif "mins" in views[x] or "min" in views[x] or "minutes" in views[x] or "minute" in views[x]:
                if int(str(views[x][0:1])) < 60:
                    not_read.append(chap_clean[x])
                    not_read.append(views[x])
                    chapter_links.append(links[x])

        url_counter += 1

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
                'https://leviatanscans.com/comics/524614-rebirth-of-an-8-circled-mage/',
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

        for x in range(0, len(chap_clean)):
            if " " in chap_clean[x]:
                chap_clean[x] = chap_clean[x].replace(" ", "")

        dates = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')

        for x in range(0, len(dates)):
            dates[x] = str(dates[x]).replace("\n", " ")

        imgs_srcs = tree.xpath('//a[@class="media-content"]/@style')
        links = tree.xpath('//a[@class="item-author text-color "]/@href')

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
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
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])

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
        links = tree.xpath('//a[@class="chapter-name text-nowrap"]/@href')

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
                    not_read.append("s")
                    not_read.append(manga[0])
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
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
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    not_read.append(chap_clean[x])
                    not_read.append(dates[x])
                    chapter_links.append(links[x])

        url_counter += 1


# Function to download cover image of all manga chapters released | method used to override that a spider is crawling
def func_find_imgs_manga_active():
    for x in range(0, no_of_manga):
        req = Request(manga_imgs[x], headers={'User-Agent': 'Mozilla/5.0'})

        name = str(x) + ".jpg"
        f = open(name, "wb")
        f.write(urlopen(req).read())
        f.close()


# Function which gets all details, images, image names, etc.
def func_get_stuff():
    global chapters
    global chapt

    func_find_daily_chaps()

    for item in not_read:
        if str(item) == "s":
            print("\n")
            global no_of_manga
            no_of_manga += 1

    func_find_imgs_manga_active()

    # The "s" is added to show a split between each manga
    for item in not_read:
        if item != "s":
            chapters.append(item)

    # To get all the new chapters into an array
    for x in range(0, len(chapters)):
        if " " not in chapters[x]:
            global chapt
            chapt.append(chapters[x])


# Creates the layout for each grid/manga
class BabyGrids(FloatLayout):
    def __init__(self, ch_details, pic_name):
        super(BabyGrids, self).__init__()
        global chapt
        global chapter_links
        global url_counter

        img = Image(source=pic_name, allow_stretch=True, keep_ratio=False, pos_hint={'x': 0, 'top': 1})
        self.add_widget(img)

        self.add_widget(Button(text=ch_details[0], pos_hint={'x': 0, 'top': 1}, size_hint=(1, 0.25), font_size='16sp',
                               background_color=(0, 0, 0, 0.3)))

        cha1 = []
        cha2 = []

        # cha1 will contain values without 's' and '\n' in the format of [name, ch_no, time, ch_no, time, ...]
        for item in ch_details:
            if item != "\n":
                cha1.append(item)

        # cha2 will contain just the chapter numbers that have been released for EACH chapter
        for x in range(0, len(cha1)):
            if x % 2 != 0:
                cha2.append(cha1[x])

        for x in reversed(range(len(cha2))):
            a = 1 - ((x + 1) * 0.25)
            btn = Button(text=chapt[0], pos_hint={'x': a, 'y': 0}, size_hint=(0.25, 0.15),
                         background_color=(1, 1, 1, 0.9))
            self.add_widget(btn)
            # partial returns a new function with both arguments
            btn.bind(on_press=partial(self.open_chapter, url_counter))
            a -= 0.25
            url_counter += 1
            chapt.pop(0)

    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def open_chapter(self, index, instance):
        func_create_batch_files(chapter_links[index])


# Creates the whole GridLayout for each manga
class MainGrid(GridLayout):
    button_list = [Button(disabled=True), Button(disabled=True), Button(disabled=True), Button(disabled=True),
                   Button(text="Run Manga Search!", font_size=20), Button(disabled=True), Button(disabled=True),
                   Button(disabled=True), Button(disabled=True)]

    def __init__(self):
        # Initialized a GridLayout where there is a max of 3 columns and we force each row to be a default size of 400px
        super(MainGrid, self).__init__(cols=3, row_force_default="True", row_default_height=400,
                                       height=self.minimum_height, size_hint=(1, None))
        self.bind(minimum_height=self.setter('height'))

        # Adding button_list to create layout
        for x in range(9):
            self.add_widget(self.button_list[x])

        # Binding the only clickable button to function
        self.button_list[4].bind(on_press=self.update_btn_text)

    def update_btn_text(self, event):
        self.button_list[4].text = "Please wait!"
        self.button_list[4].font_size = 30
        self.update_layout()

    @mainthread
    def update_layout(self):
        func_get_stuff()

        for x in range(9):
            self.remove_widget(self.button_list[x])

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

            name2 = str(y) + ".jpg"
            img = Image(source=name2, allow_stretch=True, keep_ratio=False)

            self.add_widget(BabyGrids(name_chapter_time, name2))

            name_chapter_time = []


# Enables us to scroll the content
class ScrollBarView(ScrollView):
    def __init__(self, **kwargs):
        # Created ScrollView which allows us to scroll only in the y direction and set it using a scroll bar
        super(ScrollBarView, self).__init__(do_scroll_x="False", do_scroll_y="True", size=self.size, scroll_type=['bars'])
        self.add_widget(MainGrid())


# Function which removes pictures if downloaded
def remove_images():
    for x in range(no_of_manga):
        filename = str(x) + ".jpg"
        if os.path.exists(filename):
            os.remove(filename)

    if os.path.exists("open_manga.bat"):
        os.remove("open_manga.bat")

    App.get_running_app().stop()


class WebParseApp(App):
    def build(self):
        return ScrollBarView()

    # Calls function to remove all the pictures downloaded when 'X' is clicked
    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def on_request_close(self):

        remove_images()

    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # keyboard returns the ASCII value in DEC of the key pressed
        if keyboard == 27:
            remove_images()

    # Binds the Window to a function which checks if a key is pressed
    Window.bind(on_key_down=on_keyboard_down)
    # Binds the Window to a function which is called when the 'X' button is called
    Window.bind(on_request_close=on_request_close)


if __name__ == '__main__':
    WebParseApp().run()


# i can check whatever i have not read and start counting from today
# how do i save what i have not read
# Bug #1: App doesnt start with a batch file
# Bug #2: No Loading Screen, so users think it crashed (Done more or less, UI still unresponsive but cleaner.)
# Bug #3: If more than 4 updates layout gets messy
# Load the manga more effeciently
# Change which browser opens the manga
# Be able to check which manga has been read (in same day/through-out)
