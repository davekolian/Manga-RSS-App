#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

import pymongo
from lxml import html
import requests
import time

not_read = []
no_of_manga = 0
manga_imgs = []
chapter_links = []
loading = 1
chapt = []  # list of all recent chapters
chapters = []  # list of all links to chapters in same order as chapt
img_counter = 0
not_read_dict = []


# Function which scrapes the websites to find which chapters have been newly released
def func_find_daily_chaps():
    global not_read
    global manga_imgs
    global chapter_links
    document_count = 1

    # Mangakakalot
    url_counter = 0
    url_list = ['https://mangakakalot.com/read-lm7ib158504847850', 'https://mangakakalot.com/read-ox3yk158504833790',
                'https://mangakakalot.com/read-zs6sp158504840280', 'https://mangakakalot.com/read-ul6pf158504868718',
                'https://mangakakalot.com/read-ep8pm158504835723', 'https://mangakakalot.com/read-ro4rv158504853379',
                'https://mangakakalot.com/read-ja7yn158504838124', 'https://mangakakalot.com/read-jc2wf158504842343',
                'https://mangakakalot.com/read-rp1kv158504840628', 'https://mangakakalot.com/read-ie2ho158504839970',
                'https://mangakakalot.com/read-wx1xd158504840874', 'https://mangakakalot.com/read-od1pe158504845657',
                'https://mangakakalot.com/read-yp6cp158504846116', 'https://mangakakalot.com/read-ol2fi158504849602',
                'https://mangakakalot.com/read-sz0gg158504854945', 'https://mangakakalot.com/read-dl7bc158504854888',
                'https://mangakakalot.com/read-yv2vd158504858458', 'https://mangakakalot.com/read-fv5mg158504856152',
                'https://mangakakalot.com/read-ml8nb158504854664', 'https://mangakakalot.com/read-ek1hu158504836793',
                'https://mangakakalot.com/read-ts3gp158504833220', 'https://mangakakalot.com/read-ny9yj158504835342',
                'https://mangakakalot.com/read-zg1oh158504842553', 'https://mangakakalot.com/read-vg0sa158504844980',
                'https://mangakakalot.com/read-gj8eg158504836414', 'https://mangakakalot.com/read-of6id158504884374',
                'https://mangakakalot.com/read-jb3vb158504854796', 'https://mangakakalot.com/read-jm4cz158504894339',
                'https://mangakakalot.com/read-tv7mr158504845382', 'https://mangakakalot.com/read-cq3sf158504857171',
                'https://mangakakalot.com/read-oe6uc158504836571', 'https://mangakakalot.com/read-mo5of158504931270',
                'https://mangakakalot.com/read-kh6ab158504854282', 'https://mangakakalot.com/read-rc4ti158504848110',
                'https://mangakakalot.com/read-nz2fb158504821825', 'https://mangakakalot.com/read-of5ex158504840587',
                'https://mangakakalot.com/manga/sw922557', 'https://mangakakalot.com/manga/xo924628',
                'https://mangakakalot.com/manga/fe922634', 'https://mangakakalot.com/manga/lo924793',
                'https://mangakakalot.com/read-rl4cd158504850497']

    while url_counter < len(url_list):
        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//ul[@class="manga-info-text"]/li/h1/text()')
        chap = tree.xpath('//div[@class="row"]/span/a/text()')
        # views = tree.xpath('//div[@class="row"]/span/text()')
        times = tree.xpath('//div[@class="row"]/span/text()')
        imgs_srcs = tree.xpath('//div[@class="manga-info-pic"]/img/@src')
        links = tree.xpath('//div[@class="row"]/span/a/@href')

        manga_clean = str(manga)[2:-2]
        times = [times[i] for i in range(1, len(times), 2)]

        if " " not in manga_clean:
            manga_clean += " "

        chap_clean = []

        # Gets the exact Chapter number
        for x in range(0, len(chap)):
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
            else:
                chap_clean.append(str(chap[x][start_chapter + 8:]))

        """
        # Cleans and organizes the data to be in a cleaner form
        if views[0] == '0':
            start = 0
        elif views[1] == '0':
            start = 1

        for x in range(start, len(views) // 2, 1):
            views.pop(x)

        if start != -1:
            for x in range(start, len(views) // 2, 1):
                views.pop(x)
                chap.pop(x)
        # End of the cleaning
        """

        for x in range(0, len(times)):
            if "day" in times[x] or "days" in times[x]:
                if int(str(times[x][0:1])) < 4:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "hour" in times[x] or "hours" in times[x]:
                if int(str(times[x][0:2])) < 24:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "mins" in times[x] or "min" in times[x] or "minutes" in times[x] or "minute" in times[x]:
                if int(str(times[x][0:1])) < 60:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break

        list_of_chaps = []
        list_of_chap_links = []

        for x in range(0, len(times)):
            if "day" in times[x] or "days" in times[x]:
                if int(str(times[x][0:1])) < 4:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "hour" in times[x] or "hours" in times[x]:
                if int(str(times[x][0:2])) < 24:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "mins" in times[x] or "min" in times[x] or "minutes" in times[x] or "minute" in times[x]:
                if int(str(times[x][0:1])) < 60:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])

        if list_of_chaps:
            not_read.extend([list_of_chaps, list_of_chap_links])

        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            not_read_dict.append(new_document)

        not_read = []
        url_counter += 1

     # Leviatan|Zero Scans|Reaper Scans

    url_counter = 0
    url_list = ['https://leviatanscans.com/comics/i-am-the-sorcerer-king/',
                'https://leviatanscans.com/comics/209074-slave-b',
                'https://leviatanscans.com/comics/656006-auto-hunting',
                'https://leviatanscans.com/comics/337225-the-rebirth-of-the-demon-god',
                'https://leviatanscans.com/comics/524614-rebirth-of-an-8-circled-mage/',
                'https://leviatanscans.com/comics/68254-legend-of-the-northern-blade',
                'https://leviatanscans.com/comics/233081-the-max-leveled-hero-will-return',
                'https://zeroscans.com/comics/55416-record-of-the-war-god',
                'https://zeroscans.com/comics/133460-yong-heng-zhi-zun',
                'https://zeroscans.com/comics/325051-bowblade-spirit',
                'https://zeroscans.com/comics/188504-second-life-ranker',
                'https://zeroscans.com/comics/21941-taming-master',
                'https://zeroscans.com/comics/585998-the-undefeatable-swordsman',
                'https://reaperscans.com/comics/915623-god-of-blackfield',
                'https://reaperscans.com/comics/140270-the-great-mage-returns-after-4000-years',
                'https://reaperscans.com/comics/616418-kill-the-hero',
                'https://reaperscans.com/comics/241725-limit-breaker',
                'https://reaperscans.com/comics/748666-mercenary-enrollment',
                'https://reaperscans.com/comics/542398-sss-class-suicide-hunter',
                'https://reaperscans.com/comics/709388-superhuman-era']

    while url_counter < len(url_list):
        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//h5[@class="text-highlight"]/text()')
        manga_clean = str(manga).replace("\\n", "")
        manga_clean = manga_clean.replace("'", "")
        manga_clean = manga_clean.replace("[", "")
        manga_clean = manga_clean.replace("]", "")
        manga_clean = manga_clean.replace('"', "")

        if " " not in manga_clean:
            manga_clean = manga_clean + " "

        chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')

        for x in range(0, len(chap)):
            chap[x] = "Chapter " + str(chap[x]).replace("\n", "")

        chap_clean = []

        for x in range(0, len(chap)):
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(
                    str(chap[x][start_chapter:end_line]).replace("Chapter ", ""))
            else:
                chap_clean.append(
                    str(chap[x][start_chapter:]).replace("Chapter ", ""))

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
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://zeroscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    manga_imgs.append(imgs_srcs)
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    not_read.append("s")
                    not_read.append(manga_clean)
                    if "leviatan" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://zeroscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    manga_imgs.append(imgs_srcs)
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    not_read.append("s")
                    not_read.append(manga_clean)
                    if "leviatan" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://leviatanscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    elif "reaper" in url_list[url_counter]:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://reaperscans.com")
                        imgs_srcs = imgs_srcs.replace(")", "")
                    else:
                        imgs_srcs = str(imgs_srcs[0]).replace(
                            "background-image:url(", "https://zeroscans.com")
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
                'https://manganelo.com/manga/wu_dong_qian_kun', 'https://manganelo.com/manga/jm923526',
                'https://manganelo.com/manga/the_wrong_way_to_use_healing_magic',
                'https://manganelo.com/manga/lv999_no_murabito', 'https://manganelo.com/manga/tn922327',
                'https://manganelo.com/manga/ff919945', 'https://manganelo.com/manga/bl921472',
                'https://manganelo.com/manga/legend_of_phoenix', 'https://manganelo.com/manga/spirit_sword_sovereign',
                'https://manganelo.com/manga/mushoku_tensei_isekai_ittara_honki_dasu',
                'https://manganelo.com/manga/the_legendary_moonlight_sculptor',
                'https://manganelo.com/manga/ijhr296321559609648', 'https://manganelo.com/manga/kk921357',
                'https://manganelo.com/manga/the_magic_chef_of_ice_and_fire', 'https://manganelo.com/manga/eg919734',
                'https://manganelo.com/manga/read_doupo_cangqiong_manga',
                'https://manganelo.com/manga/bb922866', 'https://manganelo.com/manga/pe922745',
                'https://manganelo.com/manga/yrlq217991556843654', 'https://manganelo.com/manga/the_great_ruler',
                'https://manganelo.com/manga/be922652', 'https://manganelo.com/manga/ra921707',
                'https://manganelo.com/manga/ix921032', 'https://manganelo.com/manga/ir920623',
                'https://manganelo.com/manga/fk918347', 'https://manganelo.com/manga/zu917722',
                'https://manganelo.com/manga/sm917699', 'https://manganelo.com/manga/wo923110',
                'https://manganelo.com/manga/rj922755', 'https://manganelo.com/manga/tv922828',
                'https://manganelo.com/manga/pd924480', 'https://manganelo.com/manga/martial_peak',
                'https://manganelo.com/manga/do918903', 'https://manganelo.com/manga/nidoume_no_jinsei_wo_isekai_de',
                'https://manganelo.com/manga/ku920038', 'https://manganelo.com/manga/aq920543',
                'https://manganelo.com/manga/pg920736', 'https://manganelo.com/manga/rx922672',
                'https://manganelo.com/manga/tn921283']

    while url_counter < len(url_list):

        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//div[@class="story-info-right"]/h1//text()')
        chap = tree.xpath('//a[@class="chapter-name text-nowrap"]/text()')
        dates = tree.xpath('//span[@class="chapter-time text-nowrap"]/text()')
        imgs_srcs = tree.xpath('//span[@class="info-image"]/img/@src')
        links = tree.xpath('//a[@class="chapter-name text-nowrap"]/@href')

        chap_clean = []

        if " " not in manga:
            manga = str(manga) + " "

        manga_clean = str(manga).replace("\\n", "")
        manga_clean = manga_clean.replace("'", "")
        manga_clean = manga_clean.replace("[", "")
        manga_clean = manga_clean.replace("]", "")
        manga_clean = manga_clean.replace('"', "")

        for x in range(0, len(chap)):
            if "Chapter" in chap[x]:
                start_chapter = chap[x].find("Chapter")

                if ":" in chap[x]:
                    end_line = chap[x].find(":")
                    chap_no = str(chap[x][start_chapter:end_line]).replace(
                        "Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                elif " -" in chap[x]:
                    end_line = chap[x].find(" -")
                    chap_no = str(chap[x][start_chapter:end_line]).replace(
                        "Chapter", "")
                    if " " in chap_no:
                        chap_clean.append(chap_no.replace(" ", ""))
                    else:
                        chap_clean.append("SC")
                else:
                    chap_no = str(chap[x][start_chapter:]
                                  ).replace("Chapter", "")
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
                    not_read.append(manga_clean)
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    not_read.append("s")
                    not_read.append(manga_clean)
                    manga_imgs.append(imgs_srcs[0])
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:1])) < 60:
                    not_read.append("s")
                    not_read.append(manga_clean)
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


# Function which gets all details, images, image names, etc.
def func_get_stuff():
    global chapters
    global chapt
    global img_counter
    global no_of_manga
    global not_read

    func_find_daily_chaps()

    not_read.append("s")

    for item in not_read:
        if str(item) == "s":
            global no_of_manga
            no_of_manga += 1

    # Added this line because there are two more 's' than the number of manga
    no_of_manga -= 2

    # The "s" is added to show a split between each manga
    for item in not_read:
        if item != "s":
            chapters.append(item)

    # To get all the new chapters into an array
    for x in range(0, len(chapters)):
        if " " not in chapters[x]:
            global chapt
            chapt.append(chapters[x])

    for x in range(len(not_read)):
        if "day ago" in not_read[x] or "hour ago" in not_read[x] or "min ago" in not_read[x] or \
                "days ago" in not_read[x] or "hours ago" in not_read[x] or "mins ago" in not_read[x] or \
                "minutes ago" in not_read[x] or "minute ago" in not_read[x]:
            not_read[x] = chapter_links[img_counter]
            img_counter += 1
        if "“" in not_read[x]:
            not_read[x] = str(not_read[x]).replace("“", "\"")
        if "”" in not_read[x]:
            not_read[x] = str(not_read[x]).replace("”", "\"")


mn = ""
mc = ""
mil = ""
mcl = ""
new_list = []
db_counter = 1


# Function which connects to my database and clears the table
def clear_database():
    client = pymongo.MongoClient(
        "mongodb+srv://dbMain:2G9eS0uUgSaFhzX7@maincluster.idq3f.mongodb.net/manga_app?retryWrites=true&w=majority")
    my_database = client.get_database("manga_app")
    my_collection = my_database.get_collection("manga_app_records")

    my_collection.delete_many({})


# Function which connects to my database and updates it
def update_database(id, name, chapters, img_link, chapter_link):
    pass


# Main core of the loop to make the program run every 30 mins
while 1:
    func_get_stuff()
    # clear_database()
    # print(not_read)
    for x in range(1, len(not_read)):
        if not_read[x] != 's':
            new_list.append(not_read[x])
        # 's' at the end of the manga so we process the data for ONE manga and update
        else:
            if len(new_list) > 2:
                mc = mc + str(new_list[1::2])

            if len(new_list) > 2:
                mcl = mcl + str(new_list[2::2])

            mc = mc.replace("[", "")
            mc = mc.replace("]", "")
            mc = mc.replace("'", "")
            mc = mc.replace(" ", "")

            mcl = mcl.replace("[", "")
            mcl = mcl.replace("]", "")
            mcl = mcl.replace("'", "")
            mcl = mcl.replace(",", "")

            mn = new_list[0]
            mil = str(manga_imgs[db_counter - 1])

            # update_database(db_counter, mn, mc, mil, mcl)
            # print(db_counter)
            db_counter += 1

            mcl = ""
            mc = ""
            new_list.clear()
            x += 1

    # Resetting all variables to default
    not_read = []
    no_of_manga = 0
    manga_imgs = []
    chapter_links = []
    loading = 1
    chapt = []  # list of all recent chapters
    chapters = []  # list of all links to chapters in same order as chapt
    img_counter = 0
    mn = ""
    mc = ""
    mil = ""
    mcl = ""
    new_list = []
    db_counter = 1
    # End of Resetting

    # Make the app sleep for 30 mins before restarting
    time.sleep(30 * 60)

#######################################################
#                    Learning                         #
#######################################################

# import MySqldb
# db = MySQLdb.connect("sql7.freemysqlhosting.net", "sql7358070", "2iyy8UBTtE", "sql7358070")
# update_sql = """UPDATE mangarssapp SET manga_name='bye' WHERE rownum=3"""
# delete_sql = """DELETE FROM mangarssapp WHERE rownum=1"""
# cursor.execute(update_sql)
# connection.commit()
