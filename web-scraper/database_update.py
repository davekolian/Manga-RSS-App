#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

import pymongo
from lxml import html
import requests
import time
# from requests_html import AsyncHTMLSession
import datetime
import sys
from configparser import ConfigParser
import asyncio
import nest_asyncio

nest_asyncio.apply()

lst_not_read_dicts = []
not_read = []
document_count = 1


# Functions which scrape the websites to find which chapters have been newly released

async def find_manga_mangakakalot(url):
    await asyncio.sleep(1)
    global not_read
    global document_count
    global error_urls

    page = requests.get(url)
    tree = html.fromstring(page.content)

    manga = tree.xpath('//ul[@class="manga-info-text"]/li/h1/text()')
    chap = tree.xpath('//div[@class="row"]/span/a/text()')
    times = tree.xpath('//div[@class="row"]/span/text()')
    imgs_srcs = tree.xpath('//div[@class="manga-info-pic"]/img/@src')
    links = tree.xpath('//div[@class="row"]/span/a/@href')

    if page.status_code == 200 and manga:
        times = [times[i] for i in range(1, len(times), 2)]

        # Cleaning the manga's name
        manga_clean = str(manga)[2:-2]

        print(manga)
        print(chap)

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

        # Adding the required manga name and index num into the not_read array
        for x in range(0, len(times)):
            if "day" in times[x] or "days" in times[x]:
                if int(str(times[x][0:1])) < 2:
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

        # Adding the required chapters and their links into array form for MongoDB
        list_of_chaps = []
        list_of_chap_links = []

        for x in range(0, len(times)):
            if "day" in times[x] or "days" in times[x]:
                if int(str(times[x][0:1])) < 2:
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

        # Appending the new chapters into the dictionary
        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)

        not_read = []


async def find_manga_manganelo(url):
    await asyncio.sleep(1)
    global not_read
    global document_count
    global error_urls

    page = requests.get(url)
    tree = html.fromstring(page.content)

    manga = tree.xpath('//div[@class="story-info-right"]/h1//text()')
    chap = tree.xpath('//a[@class="chapter-name text-nowrap"]/text()')
    dates = tree.xpath('//span[@class="chapter-time text-nowrap"]/text()')
    imgs_srcs = tree.xpath('//span[@class="info-image"]/img/@src')
    links = tree.xpath('//a[@class="chapter-name text-nowrap"]/@href')

    if page.status_code == 200 and manga:
        # Cleaning the manga's name
        manga_clean = str(manga)[2:-2]

        print(manga)
        print(chap)

        if " " not in manga_clean:
            manga_clean += " "

        chap_clean = []

        # Removing the 'Chapter' word and getting the chapter number
        for x in range(0, len(chap)):
            if "Chapter" in chap[x]:
                start_chapter = chap[x].find("Chapter")
                if ":" in chap[x]:
                    end_line = chap[x].find(":")
                    chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
                elif " -" in chap[x]:
                    end_line = chap[x].find(" -")
                    chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
                else:
                    chap_clean.append(str(chap[x][start_chapter + 8:]))
            else:
                chap_clean.append("SC")

        # Adding the required manga name and index num into the not_read array
        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:1])) < 60:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break

        # Adding the required chapters and their links into array form for MongoDB
        list_of_chaps = []
        list_of_chap_links = []

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][0:1])) < 2:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][0:2])) < 24:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])

        if list_of_chaps:
            not_read.extend([list_of_chaps, list_of_chap_links])

        # Appending the new chapters into the dictionary
        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)

        not_read = []


async def find_manga_reaperzero(url):
    await asyncio.sleep(1)
    global not_read
    global document_count
    global error_urls

    page = requests.get(url)
    tree = html.fromstring(page.content)

    manga = tree.xpath('//h5[@class="text-highlight"]/text()')
    chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')
    dates = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')
    imgs_srcs = tree.xpath('//a[@class="media-content"]/@style')
    links = tree.xpath('//a[@class="item-author text-color "]/@href')

    if page.status_code == 200 and manga:
        # Preparing image links to upload to DB
        if "reaper" in url:
            if "reaperscans.com" in str(imgs_srcs[0]):
                imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "")
            else:
                imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://reaperscans.com")
            imgs_srcs = imgs_srcs.replace(")", "")
        # else:
        #     if "zeroscans.com" in str(imgs_srcs[0]):
        #         imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "")
        #     else:
        #         imgs_srcs = str(imgs_srcs[0]).replace("background-image:url(", "https://zeroscans.com")
        #     imgs_srcs = imgs_srcs.replace(")", "")

        # Cleaning the manga's name
        manga_clean = str(manga)[4:-4]

        print(manga)
        print(chap)

        if " " not in manga_clean:
            manga_clean += " "

        # Adding 'Chapter ' infront of the chapter numbers for method to get the numbers accurately (improv)
        for x in range(0, len(chap)):
            chap[x] = "Chapter " + str(chap[x]).replace("\n", "")

        # Removing the 'Chapter' word and getting the chapter number
        chap_clean = []

        for x in range(0, len(chap)):
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
            else:
                chap_clean.append(str(chap[x][start_chapter + 8:]))

            if " " in chap_clean[x]:
                chap_clean[x] = chap_clean[x].replace(" ", "")

        # Adding the required manga name and index num into the not_read array
        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
                    not_read.append(manga_clean)
                    break

        # Adding the required chapters and their links into array form for MongoDB
        list_of_chaps = []
        list_of_chap_links = []

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    list_of_chaps.append(chap_clean[x])
                    list_of_chap_links.append(links[x])

        if list_of_chaps:
            not_read.extend([list_of_chaps, list_of_chap_links])

        # Appending the new chapters into the dictionary
        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs,
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)

        not_read = []


# async def find_manga_mangaplus(url):
#     global not_read
#     global document_count
#
#     session = AsyncHTMLSession()
#     r = await session.get(url)
#     manga = r.html.xpath('//div[@class="post-title"]/h1/text()')
#     if r.status_code == 200 and manga:
#         await r.html.arender(timeout=7000)
#
#         chap = r.html.xpath('//li[@class="wp-manga-chapter"]/a/text()')
#         dates = r.html.xpath('//span[@class="chapter-release-date"]/i/text()')
#         imgs_srcs = r.html.xpath('//div[@class="summary_image"]/a/img/@data-src')
#         links = r.html.xpath('//li[@class="wp-manga-chapter"]/a/@href')
#
#         if len(manga) >= 2:
#             manga_clean = str(manga[1])[7:-20]
#         else:
#             manga_clean = str(manga)[30:-22]
#             # Done just for Lit The Supreme Being which was buggy
#
#         # Cleaning the manga's name
#         if " " not in manga_clean:
#             manga_clean += " "
#
#         # Removing the 'Chapter' word and getting the chapter number
#         chap_clean = []
#
#         for x in range(0, len(chap)):
#             chap[x] = str(chap[x])[10:-8]
#             start_chapter = chap[x].find("Chapter")
#             if ":" in chap[x]:
#                 end_line = chap[x].find(":")
#                 chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
#             elif " -" in chap[x]:
#                 end_line = chap[x].find(" -")
#                 chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
#             else:
#                 chap_clean.append(str(chap[x][start_chapter + 8:]))
#
#         # Adding the required manga name and index num into the not_read array
#         for x in range(0, len(dates)):
#             if "day" in dates[x] or "days" in dates[x]:
#                 if int(str(dates[x][0:1])) < 2:
#                     not_read.append("s")
#                     not_read.append(document_count)
#                     document_count += 1
#                     not_read.append(manga_clean)
#                     break
#             elif "hour" in dates[x] or "hours" in dates[x]:
#                 if int(str(dates[x][0:2])) < 24:
#                     not_read.append("s")
#                     not_read.append(document_count)
#                     document_count += 1
#                     not_read.append(manga_clean)
#                     break
#             elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
#                 if int(str(dates[x][0:1])) < 60:
#                     not_read.append("s")
#                     not_read.append(document_count)
#                     document_count += 1
#                     not_read.append(manga_clean)
#                     break
#
#         # Adding the required chapters and their links into array form for MongoDB
#         list_of_chaps = []
#         list_of_chap_links = []
#
#         for x in range(0, len(dates)):
#             if "day" in dates[x] or "days" in dates[x]:
#                 if int(str(dates[x][0:1])) < 2:
#                     list_of_chaps.append(chap_clean[x])
#                     list_of_chap_links.append(links[x])
#             elif "hour" in dates[x] or "hours" in dates[x]:
#                 if int(str(dates[x][0:2])) < 24:
#                     list_of_chaps.append(chap_clean[x])
#                     list_of_chap_links.append(links[x])
#             elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
#                 if int(str(dates[x][0:2])) < 60:
#                     list_of_chaps.append(chap_clean[x])
#                     list_of_chap_links.append(links[x])
#
#         if list_of_chaps:
#             not_read.extend([list_of_chaps, list_of_chap_links])
#
#         # Appending the new chapters into the dictionary
#         if not_read:
#             new_document = {
#                 'record_id': not_read[1],
#                 'manga_name': not_read[2],
#                 'manga_chapters': not_read[3],
#                 'img_link_bg': imgs_srcs[0],
#                 'chapter_links': not_read[4]
#             }
#
#             lst_not_read_dicts.append(new_document)
#
#         not_read = []
#         await session.close()


# Function which connects to my database, clears the collection, and updates with new list of of documents

def clear_and_update_database():
    # Setting up Config Parser for more security, thanks to @bugnounty
    conf_parser = ConfigParser()
    conf_parser.read('db_config.ini')
    connection_url = conf_parser.get('server', 'connection_url')
    db_name = conf_parser.get('server', 'db_name')
    col_name = conf_parser.get('server', 'col_name')

    # Connect to the MongoDB Database
    client = pymongo.MongoClient(connection_url)
    my_database = client.get_database(db_name)
    my_collection = my_database.get_collection(col_name)

    # Clears the Collection
    my_collection.delete_many({})

    # Inserts many documents (containing new manga releases)
    my_collection.insert_many(lst_not_read_dicts)

    # Close the connection to the database
    client.close()


async def main_manga():
    # tasks_mp = []
    # url_list = ['https://manhuaplus.com/manga/almighty-master/', 'https://manhuaplus.com/manga/global-martial-arts/',
    #             'https://manhuaplus.com/manga/the-great-ruler/', 'https://manhuaplus.com/manga/the-strongest-god-king/',
    #             'https://manhuaplus.com/manga/rebirth-of-the-urban-immortal-cultivator/',
    #             'https://manhuaplus.com/manga/demon-magic-emperor/', 'https://manhuaplus.com/manga/apotheosis/',
    #             'https://manhuaplus.com/manga/battle-through-the-heavens/',
    #             'https://manhuaplus.com/manga/peerless-battle-spirit/', 'https://manhuaplus.com/manga/versatile-mage/',
    #             'https://manhuaplus.com/manga/tales-of-demons-and-gods/',
    #             'https://manhuaplus.com/manga/lit-the-supreme-being/',
    #             'https://manhuaplus.com/manga/rebirth-city-deity/']
    #
    # for link in url_list:
    #     tasks_mp.append(asyncio.create_task(find_manga_mangaplus(link)))
    #
    # await asyncio.gather(*tasks_mp)

    tasks_mp = []
    # url_list = ['https://reaperscans.com/comics/27937-god-of-blackfield',
    #             'https://reaperscans.com/comics/316621-the-great-mage-returns-after-4000-years',
    #             'https://reaperscans.com/comics/917294-kill-the-hero',
    #             'https://reaperscans.com/comics/563929-limit-breaker',
    #             'https://reaperscans.com/comics/535459-mercenary-enrollment',
    #             'https://reaperscans.com/comics/335355-sss-class-suicide-hunter',
    #             'https://reaperscans.com/comics/147221-superhuman-era',
    #             'https://reaperscans.com/comics/364640-the-tutorial-is-too-hard',
    #             'https://reaperscans.com/comics/326450-the-player-that-cant-level-up',
    #             'https://reaperscans.com/comics/276469-strongest-fighter',
    #             'https://reaperscans.com/comics/507776-return-of-the-frozen-player',
    #             'https://reaperscans.com/comics/585562-arcane-sniper',
    #             'https://zeroscans.com/comics/55416-record-of-the-war-god',
    #             'https://zeroscans.com/comics/133460-yong-heng-zhi-zun',
    #             'https://zeroscans.com/comics/325051-bowblade-spirit',
    #             'https://zeroscans.com/comics/188504-second-life-ranker',
    #             'https://zeroscans.com/comics/21941-taming-master',
    #             'https://zeroscans.com/comics/585998-the-undefeatable-swordsman']
    #
    # # Reaper Scans | Zero Scans
    # for link in url_list:
    #     tasks_mp.append(asyncio.create_task(find_manga_reaperzero(link)))

    # Mangakakalot
    url_list = ['https://mangakakalot.com/read-lm7ib158504847850', 'https://mangakakalot.com/read-ox3yk158504833790',
                'https://mangakakalot.com/read-zs6sp158504840280', 'https://mangakakalot.com/read-ul6pf158504868718',
                'https://mangakakalot.com/read-ep8pm158504835723', 'https://mangakakalot.com/read-ro4rv158504853379',
                'https://mangakakalot.com/read-ja7yn158504838124', 'https://mangakakalot.com/read-jc2wf158504842343',
                'https://mangakakalot.com/read-rp1kv158504840628', 'https://mangakakalot.com/read-ie2ho158504839970',
                'https://mangakakalot.com/read-wx1xd158504840874', 'https://mangakakalot.com/read-od1pe158504845657',
                'https://mangakakalot.com/read-ol2fi158504849602', 'https://mangakakalot.com/manga/lo924793',
                'https://mangakakalot.com/read-sz0gg158504854945', 'https://mangakakalot.com/read-dl7bc158504854888',
                'https://mangakakalot.com/read-yv2vd158504858458', 'https://mangakakalot.com/read-fv5mg158504856152',
                'https://mangakakalot.com/read-ts3gp158504833220', 'https://mangakakalot.com/read-ny9yj158504835342',
                'https://mangakakalot.com/read-zg1oh158504842553', 'https://mangakakalot.com/read-vg0sa158504844980',
                'https://mangakakalot.com/read-gj8eg158504836414', 'https://mangakakalot.com/read-of6id158504884374',
                'https://mangakakalot.com/read-jb3vb158504854796', 'https://mangakakalot.com/read-jm4cz158504894339',
                'https://mangakakalot.com/read-tv7mr158504845382', 'https://mangakakalot.com/read-cq3sf158504857171',
                'https://mangakakalot.com/read-oe6uc158504836571', 'https://mangakakalot.com/read-mo5of158504931270',
                'https://mangakakalot.com/read-kh6ab158504854282', 'https://mangakakalot.com/read-rc4ti158504848110',
                'https://mangakakalot.com/read-iq9la158504835986', 'https://mangakakalot.com/manga/dy925897',
                'https://mangakakalot.com/manga/xo924628', 'https://mangakakalot.com/manga/eo924794',
                'https://mangakakalot.com/manga/yl923871', 'https://mangakakalot.com/manga/vi924713',
                'https://mangakakalot.com/read-iw9rf158504883256', 'https://mangakakalot.com/read-bo1jc158504861718',
                'https://mangakakalot.com/manga/py923734', 'https://mangakakalot.com/manga/ni924461',
                'https://mangakakalot.com/manga/xl923012', 'https://mangakakalot.com/read-ts7tt158504943623',
                'https://mangakakalot.com/manga/jv925863', 'https://mangakakalot.com/read-fq9iu158504944929',
                'https://mangakakalot.com/manga/xv925862', 'https://mangakakalot.com/manga/cc925283',
                'https://mangakakalot.com/manga/sw922557', 'https://mangakakalot.com/read-xf9fk158504906020',
                'https://mangakakalot.com/read-nz2fb158504821825', 'https://mangakakalot.com/read-rl4cd158504850497',
                'https://mangakakalot.com/manga/gi925311', 'https://mangakakalot.com/manga/vf922819',
                'https://mangakakalot.com/manga/ks924647', 'https://mangakakalot.com/manga/ph925967',
                'https://mangakakalot.com/manga/xv925862',]

    for link in url_list:
        tasks_mp.append(asyncio.create_task(find_manga_mangakakalot(link)))

    # Manganelo
    url_list = ['https://manganelo.com/manga/xn921310', 'https://manganelo.com/manga/huku267071576897767',
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
                'https://manganelo.com/manga/the_legendary_moonlight_sculptor', 'https://manganelo.com/manga/tn921283',
                'https://manganelo.com/manga/ijhr296321559609648', 'https://manganelo.com/manga/si923815',
                'https://manganelo.com/manga/the_magic_chef_of_ice_and_fire', 'https://manganelo.com/manga/eg919734',
                'https://manganelo.com/manga/bb922866', 'https://manganelo.com/manga/pe922745',
                'https://manganelo.com/manga/yrlq217991556843654', 'https://manganelo.com/manga/aq920543',
                'https://manganelo.com/manga/be922652', 'https://manganelo.com/manga/ra921707',
                'https://manganelo.com/manga/ix921032', 'https://manganelo.com/manga/ir920623',
                'https://manganelo.com/manga/fk918347', 'https://manganelo.com/manga/zu917722',
                'https://manganelo.com/manga/sm917699', 'https://manganelo.com/manga/wo923110',
                'https://manganelo.com/manga/rj922755', 'https://manganelo.com/manga/tv922828',
                'https://manganelo.com/manga/pd924480', 'https://manganelo.com/manga/martial_peak',
                'https://manganelo.com/manga/do918903', 'https://manganelo.com/manga/nidoume_no_jinsei_wo_isekai_de',
                'https://manganelo.com/manga/ku920038', 'https://manganelo.com/manga/mq918999',
                'https://manganelo.com/manga/lj919175', 'https://manganelo.com/manga/dr_frost',
                'https://manganelo.com/manga/gz922893', 'https://manganelo.com/manga/shikkaku_mon_no_saikyou_kenja',
                'https://manganelo.com/manga/the_other_world_doesnt_stand_a_chance_against_the_power_of_instant_death',
                'https://manganelo.com/manga/tensei_kenja_no_isekai_raifu_daini_no_shokugyo_wo_ete_sekai_saikyou_ni_narimashita',
                'https://manganelo.com/manga/ec925329', 'https://manganelo.com/manga/read_doupo_cangqiong_manga',
                'https://manganelo.com/manga/pg920736', 'https://manganelo.com/manga/the_great_ruler',
                'https://manganelo.com/manga/rx922672', 'https://manganelo.com/manga/vrin278571580265812',
                'https://manganelo.com/manga/apotheosis', 'https://manganelo.com/manga/kk921357',
                'https://manganelo.com/manga/hyer5231574354229', 'https://manganelo.com/manga/sw923218',
                'https://manganelo.com/manga/rx919523', 'https://manganelo.com/manga/uw924618',
                'https://manganelo.com/manga/dz919342', 'https://manganelo.com/manga/pe922986',
                'https://manganelo.com/manga/pb925700', 'https://manganelo.com/manga/zm924455',
                'https://manganelo.com/manga/yong_heng_zhi_zun', 'https://manganelo.com/manga/kg923596',
                'https://manganelo.com/manga/jx925356', 'https://manganelo.com/manga/jf921342',
                'https://manganelo.com/manga/lg924896', 'https://manganelo.com/manga/fe922634',
                'https://manganelo.com/manga/qp925636', 'https://manganelo.com/manga/dq922693',
                'https://manganelo.com/manga/rm922554', 'https://manganelo.com/manga/go922760',
                'https://manganelo.com/manga/ph925080', 'https://manganelo.com/manga/kj923068',
                'https://manganelo.com/manga/rf925407']

    for link in url_list:
        tasks_mp.append(asyncio.create_task(find_manga_manganelo(link)))

    await asyncio.gather(*tasks_mp)


# Main core of the loop to make the program run every x mins
if __name__ == "__main__":
    while True:
        document_count = 1

        try:
            # Creating a File Log System
            current_time = str(datetime.datetime.now())
            output_console = "[" + current_time + "] " + "Starting the search for mangas!\n"
            log = open("log.txt", "a")
            log.write(output_console)
            log.close()

            asyncio.run(main_manga())
            # print(lst_not_read_dicts)

            current_time = str(datetime.datetime.now())
            output_console = "[" + str(current_time) + "] " + str(lst_not_read_dicts) + "\n"
            log = open("log.txt", "a")
            log.write(output_console)
            log.close()

            clear_and_update_database()
        except Exception as ex:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            line_no = exception_traceback.tb_lineno
            # Adding (an) exception(s) on the log file
            current_time = str(datetime.datetime.now())
            output_console = "[" + current_time + "] " + "Exception has occured: " + str(line_no) + " - " + str(
                ex.args) + " !\n"

            log = open("log.txt", "a")
            log.write(output_console)
            log.close()

            # time.sleep(5 * 60)
        finally:
            # Clears the list for next iteration
            lst_not_read_dicts = []

            # Make the app sleep for x mins before restarting
            time.sleep(10 * 60)

            # Adding when the sleep timer is over
            current_time = str(datetime.datetime.now())
            output_console = "[" + current_time + "] " + "Restarting the loop!\n"

            log = open("log.txt", "a")
            log.write(output_console)
            log.close()

#######################################################
#                    Learning                         #
#######################################################
# MongoDB stuff:
# import pymongo

# client = pymongo.MongoClient("connection_url")

# db = client.get_database('manga_app')

# table = db.get_collection("manga_app_records")
# collection -> table
# document -> rows

# table.delete_many({})

# print(table.count_documents({}))

# insert a document i.e row insert_one() or insert_many()

# new_row = {
#     'record_id': 3,
#     'manga_name': 'dummy name',
#     'manga_chapters': ['c1', 'c2'],
#     'img_link_bg': 'dummy_link',
#     'chapter_links': ['link1', 'link2']
# }

# table.insert_one(new_row)


# find a document, find() -> returns an iterator, find_one({'keyword': search})
# print(list(table.find({})))

# update, update_one(filter_dict, {'$set': new_dict}) or update_many

# delete, delete_one(filter_dict) or delete_many(filter_dict)
# print(list(table.find({'manga_name': 'dummy name'})))
# table.delete_many({'manga_name': 'dummy name'})
