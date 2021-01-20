#####################################################################
#                All rights reserved to davekolian                  #
#####################################################################

import pymongo
from lxml import html
import requests
import time
from requests_html import HTMLSession

lst_not_read_dicts = []


# Function which scrapes the websites to find which chapters have been newly released
def func_find_daily_chaps():
    global lst_not_read_dicts
    not_read = []
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
                'https://mangakakalot.com/read-of5ex158504840587', 'https://mangakakalot.com/read-iq9la158504835986',
                'https://mangakakalot.com/manga/xo924628', 'https://mangakakalot.com/manga/gz922893',
                'https://mangakakalot.com/manga/fe922634', 'https://mangakakalot.com/manga/lo924793',
                'https://mangakakalot.com/manga/lg924896']

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

        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)


        print(manga_clean)
        print(chap_clean)
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
        chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')
        dates = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')
        imgs_srcs = tree.xpath('//a[@class="media-content"]/@style')
        links = tree.xpath('//a[@class="item-author text-color "]/@href')

        manga_clean = str(manga)[4:-4]

        if " " not in manga_clean:
            manga_clean += " "

        for x in range(0, len(chap)):
            chap[x] = "Chapter " + str(chap[x]).replace("\n", "")

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

        # for x in range(0, len(dates)):
        #     dates[x] = str(dates[x]).replace("\n", " ")

        for x in range(0, len(dates)):
            if "day" in dates[x] or "days" in dates[x]:
                if int(str(dates[x][1:2])) < 2:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
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
                    break
            elif "hour" in dates[x] or "hours" in dates[x]:
                if int(str(dates[x][1:2])) < 24:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
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
                    break
            elif "mins" in dates[x] or "min" in dates[x] or "minutes" in dates[x] or "minute" in dates[x]:
                if int(str(dates[x][0:2])) < 60:
                    not_read.append("s")
                    not_read.append(document_count)
                    document_count += 1
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
                    break

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

        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs,
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)


        print(manga_clean)
        print(chap_clean)
        not_read = []
        url_counter += 1

    # Manganelo
    url_counter = 0
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
                'https://manganelo.com/manga/ijhr296321559609648', 'https://manganelo.com/manga/lo924793',
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
                'https://manganelo.com/manga/lj919175']

    while url_counter < len(url_list):

        page = requests.get(url_list[url_counter])
        tree = html.fromstring(page.content)

        manga = tree.xpath('//div[@class="story-info-right"]/h1//text()')
        chap = tree.xpath('//a[@class="chapter-name text-nowrap"]/text()')
        dates = tree.xpath('//span[@class="chapter-time text-nowrap"]/text()')
        imgs_srcs = tree.xpath('//span[@class="info-image"]/img/@src')
        links = tree.xpath('//a[@class="chapter-name text-nowrap"]/@href')

        manga_clean = str(manga)[2:-2]

        if " " not in manga_clean:
            manga_clean += " "

        chap_clean = []

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

        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)


        print(manga_clean)
        print(chap_clean)
        not_read = []
        url_counter += 1

    # ManhuaPlus
    url_counter = 0
    url_list = ['https://manhuaplus.com/manga/almighty-master/', 'https://manhuaplus.com/manga/global-martial-arts/',
                'https://manhuaplus.com/manga/the-great-ruler/', 'https://manhuaplus.com/manga/the-strongest-god-king/',
                'https://manhuaplus.com/manga/rebirth-of-the-urban-immortal-cultivator/',
                'https://manhuaplus.com/manga/demon-magic-emperor/', 'https://manhuaplus.com/manga/apotheosis/',
                'https://manhuaplus.com/manga/battle-through-the-heavens/',
                'https://manhuaplus.com/manga/peerless-battle-spirit/', 'https://manhuaplus.com/manga/versatile-mage/',
                'https://manhuaplus.com/manga/tales-of-demons-and-gods/',
                'https://manhuaplus.com/manga/lit-the-supreme-being/',
                'https://manhuaplus.com/manga/rebirth-city-deity/']

    session = HTMLSession()

    while url_counter < len(url_list):
        r = session.get(url_list[url_counter])
        r.html.render()

        manga = r.html.xpath('//div[@class="post-title"]/h1/text()')
        chap = r.html.xpath('//li[@class="wp-manga-chapter"]/a/text()')
        dates = r.html.xpath('//span[@class="chapter-release-date"]/i/text()')
        imgs_srcs = r.html.xpath('//div[@class="summary_image"]/a/img/@data-src')
        links = r.html.xpath('//li[@class="wp-manga-chapter"]/a/@href')

        if len(manga) >= 2:
            manga_clean = str(manga[1])[7:-20]
        else:
            manga_clean = str(manga)[30:-22]
            # Done just for Lit The Supreme Being which was buggy

        if " " not in manga_clean:
            manga_clean += " "

        chap_clean = []

        for x in range(0, len(chap)):
            chap[x] = str(chap[x])[10:-8]
            start_chapter = chap[x].find("Chapter")
            if ":" in chap[x]:
                end_line = chap[x].find(":")
                chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
            elif " -" in chap[x]:
                end_line = chap[x].find(" -")
                chap_clean.append(str(chap[x][start_chapter + 8:end_line]))
            else:
                chap_clean.append(str(chap[x][start_chapter + 8:]))

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

        if not_read:
            new_document = {
                'record_id': not_read[1],
                'manga_name': not_read[2],
                'manga_chapters': not_read[3],
                'img_link_bg': imgs_srcs[0],
                'chapter_links': not_read[4]
            }

            lst_not_read_dicts.append(new_document)


        print(manga_clean)
        print(chap_clean)
        not_read = []
        url_counter += 1


# Function which connects to my database, clears the collection, and updates with new list of of documents
def clear_and_update_database():
    # Connect to the MongoDB Database
    client = pymongo.MongoClient(
        "mongodb+srv://dbOutside:bs62uTozRGLE84sQ@maincluster.idq3f.mongodb.net/manga_app?retryWrites=true&w=majority")
    my_database = client.get_database("manga_app")
    my_collection = my_database.get_collection("manga_app_records")

    # Clears the Collection
    my_collection.delete_many({})

    # Inserts many documents (containing new manga releases)
    my_collection.insert_many(lst_not_read_dicts)

    # Close the connection to the database
    client.close()


# Main core of the loop to make the program run every x mins
def main_loop():
    while 1:
        global lst_not_read_dicts

        try:
            func_find_daily_chaps()
            print(lst_not_read_dicts)
            clear_and_update_database()

            # Clears the list for next iteration
            lst_not_read_dicts = []

            # Make the app sleep for x mins before restarting
            time.sleep(10 * 60)
        except:
            # using bare 'except' since majority error could be traffic problems with websites or MongoDB
            time.sleep(5 * 60)
            main_loop()


if __name__ == "__main__":
    main_loop()

#######################################################
#                    Learning                         #
#######################################################

# import MySqldb
# db = MySQLdb.connect("sql7.freemysqlhosting.net", "sql7358070", "2iyy8UBTtE", "sql7358070")
# update_sql = """UPDATE mangarssapp SET manga_name='bye' WHERE rownum=3"""
# delete_sql = """DELETE FROM mangarssapp WHERE rownum=1"""
# cursor.execute(update_sql)
# connection.commit()

# MongoDB stuff:
# import pymongo

# client = pymongo.MongoClient("mongodb+srv://dbMain:2G9eS0uUgSaFhzX7@maincluster.idq3f.mongodb.net/manga_app
# ?retryWrites=true&w=majority")

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
