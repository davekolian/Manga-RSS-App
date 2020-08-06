#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

# from lxml import html
# import requests
from urllib.request import Request, urlopen

import kivy
kivy.require('1.11.0')

# import time

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
# from kivy.clock import mainthread
from functools import partial

import mysql.connector as mysql

# Global Variables
no_of_manga = 0
chapter_links = []
url_counter = 0
result = ""
pwd = "D:\Documents\GitHub\Manga-RSS-App\Manga-RSS-App"
# pwd is hardcoded to the directory of the webParse.py file


# Function which creates a batch file to open the manga chapter in my browser of choice
def func_create_batch_files(link):
    file_name = pwd + "\open_manga.bat"
    f = open(file_name, "w")
    code = "start firefox.exe " + link
    f.write(code)
    f.close()

    os.system(file_name)


# Function to download cover image of all manga chapters released | method used to override that a spider is crawling
def func_find_imgs_manga_active(img_link, x):
    req = Request(img_link, headers={'User-Agent': 'Mozilla/5.0'})

    name = str(x) + ".jpg"
    file_name = pwd + "\\" + name
    f = open(file_name, "wb")
    f.write(urlopen(req).read())
    f.close()


# Function to connect to my database and read the tuples in the table
def connect_to_database():
    connection = mysql.connect(host="sql7.freemysqlhosting.net", database="sql7358070", user="sql7358070",
                               password="2iyy8UBTtE")
    cursor = connection.cursor()

    sql = "SELECT * FROM mangarssapp"

    try:
        cursor.execute(sql)
        # connection.commit()
        global result
        result = cursor.fetchall()
        if result != "":
            global no_of_manga
            no_of_manga = len(result)

        # print(result)
    except mysql.Error as error:
        print(error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Creates the layout for each grid/manga
class BabyGrids(FloatLayout):
    def __init__(self, chapter_name, the_chapters, img_name):
        super(BabyGrids, self).__init__()
        global url_counter
        cha1 = []

        img = Image(source=img_name, allow_stretch=True, keep_ratio=False, pos_hint={'x': 0, 'top': 1})
        self.add_widget(img)

        ch_name = str(chapter_name)
        ch_name_words = ch_name.split()
        if len(ch_name_words) >= 6 and 35 < len(ch_name) < 50:
            mid = int(len(ch_name_words) / 2)
            ch_name_words[mid:mid] = "\n"

        if len(ch_name) > 50:
            for x in range(5, len(ch_name_words), 5):
                ch_name_words[x:x] = "\n"

        ch_name = " ".join(ch_name_words)

        self.add_widget(Button(text=ch_name, pos_hint={'x': 0, 'top': 1}, size_hint=(1, 0.25), font_size='16sp',
                               background_color=(0, 0, 0, 0.3)))

        if "," in the_chapters:
            les_words2 = str(the_chapters).split(",")
            for item in les_words2:
                cha1.append(item)
        else:
            cha1.append(the_chapters)

        for x in reversed(range(len(cha1))):
            a = 1 - ((x + 1) * 0.25)
            if a < 0:
                a += int(x / 4)
            b = int(x / 4) * (3 / 20)
            y = len(cha1) - x - 1
            # print("Chapter: " + cha1[y])
            # print(str(a) + " " + str(y))

            btn = Button(text=cha1[y], pos_hint={'x': a, 'y': b}, size_hint=(0.25, 0.15),
                         background_color=(1, 1, 1, 0.9))
            self.add_widget(btn)
            # partial returns a new function with both arguments
            btn.bind(on_press=partial(self.open_chapter, url_counter))
            a -= 0.25
            url_counter += 1

    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def open_chapter(self, index, instance):
        func_create_batch_files(chapter_links[index])


# Creates the whole GridLayout for each manga
class MainGrid(GridLayout):
    # button_list = [Button(disabled=True), Button(disabled=True), Button(disabled=True), Button(disabled=True),
    #               Button(text="Run Manga Search!", font_size=20), Button(disabled=True), Button(disabled=True),
    #               Button(disabled=True), Button(disabled=True)]

    def __init__(self):
        # Initialized a GridLayout where there is a max of 3 columns and we force each row to be a default size of 400px
        super(MainGrid, self).__init__(cols=3, row_force_default="True", row_default_height=400,
                                       height=self.minimum_height, size_hint=(1, None))
        self.bind(minimum_height=self.setter('height'))

        for x in range(no_of_manga):
            the_links = result[x][-1]
            if " " in the_links:
                les_words = the_links.split()
                for item in les_words:
                    chapter_links.append(item)
            else:
                chapter_links.append(the_links)

        for x in range(no_of_manga):
            img_link = result[x][-2]
            chapter_name = result[x][1]
            the_chapters = result[x][2]
            func_find_imgs_manga_active(img_link, x)

            img_name = str(x) + ".jpg"

            self.add_widget(BabyGrids(chapter_name, the_chapters, img_name))

        if x + 1 == no_of_manga:
            all_links_btn = Button(text="Open all chapters!", font_size=20)
            self.add_widget(all_links_btn)
            all_links_btn.bind(on_press=self.all_links_func)

    # Function to open all chapters in one Firefox Browser
    def all_links_func(self, event):
        link = ""
        for x in range(no_of_manga):
            link = link + " " + chapter_links[x]

        func_create_batch_files(link)

        # Adding button_list to create layout
        # for x in range(9):
            # self.add_widget(self.button_list[x])

        # Binding the only clickable button to function
        # self.button_list[4].bind(on_press=self.update_btn_text)
"""
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

        if y == no_of_manga - 1:
            all_links_btn = Button(text="Open all chapters!", font_size=20)
            self.add_widget(all_links_btn)
            all_links_btn.bind(on_press=self.all_links_func)

    def all_links_func(self, event):
        link = ""
        for x in range(no_of_manga):
            link = link + " " + chapter_links[x]

        func_create_batch_files(link)
"""


# Enables us to scroll the content
class ScrollBarView(ScrollView):
    def __init__(self, **kwargs):
        # Created ScrollView which allows us to scroll only in the y direction and set it using a scroll bar
        super(ScrollBarView, self).__init__(do_scroll_x="False", do_scroll_y="True", size=self.size,
                                            scroll_type=['bars', 'content'])
        self.add_widget(MainGrid())


# Function which removes pictures if downloaded
def remove_images():
    for x in range(no_of_manga):
        filename = pwd + "\\" + str(x) + ".jpg"
        if os.path.exists(filename):
            os.remove(filename)

    if os.path.exists(filename):
        os.remove(filename)

    App.get_running_app().stop()


# Main App
class WebParseApp(App):
    def build(self):
        connect_to_database()
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
# Bug #1: App doesnt start with a batch file [Fixed] WITH hardcoding the cwd of the webParse.py before each file
# Bug #2: No Loading Screen, so users think it crashed [Fixed] WITH the help of remote MySQL database.
# Bug #3: If more than 4 updates layout gets messy [Fixed]
# Bug #4: Manga name came in the place of Chapter number. CAUSE: no space in the manga name (algorithm used) [Fixed]
# Bug #5: Text for some manga goes out of bound [Fixed]
# Bug #6: [Not certain] Make a fix if more than 8/12 chapters get updated in a go
# Load the manga more effeciently [Done] WITH the help of remote MySQL database.
# Change which browser opens the manga
# Be able to check which manga has been read (in same day/through-out)
# Need to be able to add manga to the list in a better way
# Try and use .kv / Builder.load
