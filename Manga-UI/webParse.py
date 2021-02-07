#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

from urllib.request import Request, urlopen
import os
import pymongo
import tempfile
import shutil
import kivy

kivy.require('1.11.0')

from kivy.config import Config

# Sets Window to: not be resizable, size of 850x1000, not close when 'ESC' key is clicked
Config.set('graphics', 'multisamples', 0)
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'height', 1000)
Config.set('graphics', 'width', 850)
Config.set('kivy', 'exit_on_escape', 0)

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
# from kivy.clock import mainthread
from functools import partial

# Global Variables
no_of_manga = 0
chapter_links = []
url_counter = 0
result = []
pwd = tempfile.mkdtemp()


# Function which creates a batch file to open the manga chapter in my browser of choice
def func_create_batch_files(link):
    file_name = pwd + "\open_manga.bat"
    f = open(file_name, "w")
    code = "start firefox.exe " + link
    f.write(code)
    f.close()

    os.system(file_name)


# Function to download cover image of all manga chapters released | method used to override that a spider is crawling
def func_find_imgs_manga_active(img_link, img_name):
    req = Request(img_link, headers={'User-Agent': 'Mozilla/5.0'})

    file_name = pwd + "\\" + img_name
    f = open(file_name, "wb")
    f.write(urlopen(req).read())
    f.close()


# Function to connect to my database and read the tuples in the table
def connect_to_database():
    global result
    global no_of_manga

    client = pymongo.MongoClient(
        "mongodb+srv://dbOutside:bs62uTozRGLE84sQ@maincluster.idq3f.mongodb.net/manga_app?retryWrites=true&w=majority")

    my_database = client.get_database("manga_app")
    my_collection = my_database.get_collection("manga_app_records")

    result = list(my_collection.find({}))
    no_of_manga = my_collection.count_documents({})

    client.close()


# Creates the layout for each grid/manga
class BabyGrids(FloatLayout):
    def __init__(self, manga_name, img_name, lst_chapters_nos, lst_chapters_links):
        super(BabyGrids, self).__init__()

        tmp_img_name = pwd + "\\" + img_name

        img = Image(source=tmp_img_name, allow_stretch=True, keep_ratio=False, pos_hint={'x': 0, 'top': 1})
        self.add_widget(img)

        list_words_in_name = manga_name.split()
        if len(list_words_in_name) >= 6 and 35 < len(manga_name) < 50:
            mid = int(len(list_words_in_name) / 2)
            list_words_in_name[mid:mid] = "\n"
        if len(manga_name) > 50:
            for x in range(5, len(list_words_in_name), 5):
                list_words_in_name[x:x] = "\n"

        manga_name = " ".join(list_words_in_name)

        self.add_widget(Button(text=manga_name, pos_hint={'x': 0, 'top': 1}, size_hint=(1, 0.25), font_size='16sp',
                               background_color=(0, 0, 0, 0.3)))

        if len(lst_chapters_nos) <= 20:
            for x in reversed(range(len(lst_chapters_nos))):
                a = 1 - ((x + 1) * 0.25)
                if a < 0:
                    a += int(x / 4)
                b = int(x / 4) * (3 / 20)
                y = len(lst_chapters_nos) - x - 1

                btn = Button(text=lst_chapters_nos[y], pos_hint={'x': a, 'y': b}, size_hint=(0.25, 0.15),
                             background_color=(1, 1, 1, 0.9))
                self.add_widget(btn)
                # partial returns a new function with both arguments
                # it's the same as open_chapter(lst_chapters_links[y]])
                btn.bind(on_press=partial(self.open_chapter, lst_chapters_links[y]))
                a -= 0.25
        else:
            # First button labelled '0'
            first = len(lst_chapters_nos) - 1
            btn = Button(text=lst_chapters_nos[first], pos_hint={'x': 0.75, 'y': 0}, size_hint=(0.25, 0.15),
                         background_color=(1, 1, 1, 0.9))
            self.add_widget(btn)
            # partial returns a new function with both arguments
            # it's the same as open_chapter(lst_chapters_links[y]])
            btn.bind(on_press=partial(self.open_chapter, lst_chapters_links[first]))

            # Second button for the other 20+ links, labelled '...'
            other_links = [lst_chapters_links[i] for i in range(len(lst_chapters_nos) - 2, -1, -1)]
            str_links = ' '.join(other_links)

            btn = Button(text="...", pos_hint={'x': 0.5, 'y': 0}, size_hint=(0.25, 0.15),
                         background_color=(1, 1, 1, 0.9))
            self.add_widget(btn)
            # partial returns a new function with both arguments
            # it's the same as open_chapter(lst_chapters_links[y]])
            btn.bind(on_press=partial(self.open_chapter, str_links))

    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def open_chapter(self, links, instance):
        func_create_batch_files(links)


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

        for document in result:
            manga_name = document.get("manga_name")
            img_name = str(document.get("record_id")) + ".jpg"
            lst_chapters_nos = document.get("manga_chapters")
            lst_chapters_links = document.get("chapter_links")

            func_find_imgs_manga_active(document.get("img_link_bg"), img_name)

            self.add_widget(BabyGrids(manga_name, img_name, lst_chapters_nos, lst_chapters_links))

        all_links_btn = Button(text="Open all chapters!", font_size=20)
        self.add_widget(all_links_btn)
        all_links_btn.bind(on_press=self.all_links_func)

    # Function to open all chapters in one Firefox Browser
    def all_links_func(self, event):
        links = ""

        for document in result:
            list_of_chapter_links = document.get("chapter_links")
            for link in list_of_chapter_links:
                links = links + " " + link

        func_create_batch_files(links)


# Enables us to scroll the content
class ScrollBarView(ScrollView):
    def __init__(self, **kwargs):
        # Created ScrollView which allows us to scroll only in the y direction and set it using a scroll bar
        super(ScrollBarView, self).__init__(do_scroll_x="False", do_scroll_y="True", size=self.size,
                                            scroll_type=['bars', 'content'])
        self.add_widget(MainGrid())


# Function which removes pictures if downloaded
def remove_tempfiles():
    for x in range(1, no_of_manga + 1):
        filename = pwd + "\\" + str(x) + ".jpg"
        if os.path.exists(filename):
            os.remove(filename)

    manga_filename = pwd  + "\open_manga.bat"
    if os.path.exists(manga_filename):
        os.remove(manga_filename)

    shutil.rmtree(pwd)

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
        remove_tempfiles()

    # comment below is used to suppress the 'function may be static' error
    # noinspection PyMethodMayBeStatic
    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # keyboard returns the ASCII value in DEC of the key pressed
        if keyboard == 27:
            remove_tempfiles()

    # Binds the Window to a function which checks if a key is pressed
    Window.bind(on_key_down=on_keyboard_down)
    # Binds the Window to a function which is called when the 'X' button is called
    Window.bind(on_request_close=on_request_close)


if __name__ == '__main__':
    WebParseApp().run()

# i can check whatever i have not read and start counting from today
# Log-in system so that users can users can use
# New system to allow for mangas to stay if not read
# Bug #1: No Loading Screen, so users think it crashed
# Bug #2: Text for some manga goes out of bound [Temporarily fixed]
# Bug #6: Make a fix if more than 20 chapters get updated in a go [Temporarily fixed]
# Load the manga more efficiently
# Change which browser opens the manga
# Be able to check which manga has been read (in same day/through-out)
# Try and use .kv / Builder.load
