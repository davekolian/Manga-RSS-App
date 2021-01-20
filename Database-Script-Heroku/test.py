import pymongo
from lxml import html
import requests
import time
from requests_html import HTMLSession

lst_not_read_dicts = []

not_read = []
document_count = 1

# Mangakakalot
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

while url_counter < len(url_list):
    page = requests.get(url_list[url_counter])
    tree = html.fromstring(page.content)

    manga = tree.xpath('//div[@class="post-title"]/h1/text()')
    chap = tree.xpath('//li[@class="wp-manga-chapter"]/a/text()')
    times = tree.xpath('//span[@class="chapter-release-date"]/i/text()')
    imgs_srcs = tree.xpath('//div[@class="summary_image"]/a/img/@data-src')
    links = tree.xpath('//li[@class="wp-manga-chapter"]/a/@href')

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
