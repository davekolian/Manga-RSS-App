import requests
from lxml import html

lst_not_read_dicts = []
not_read = []
document_count = 1



def find_manga_reaperzero(url):
    global not_read
    global document_count
    global error_urls

    my_session = requests.Session()
    for_cookies = my_session.get("http://reaperscans.com")
    cookies = for_cookies.cookies
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}

    page = requests.get(url, headers=headers, cookies=cookies)
    tree = html.fromstring(page.content)

    print(page)

    manga = tree.xpath('//h5[@class="text-highlight"]/text()')
    chap = tree.xpath('//span[@class="text-muted text-sm"]/text()')
    dates = tree.xpath('//a[@class="item-company text-muted h-1x"]/text()')
    imgs_srcs = tree.xpath('//a[@class="media-content"]/@style')
    links = tree.xpath('//a[@class="item-author text-color "]/@href')

    print(manga)
    print(chap)

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


if __name__ == "__main__":
    url_list = ['https://reaperscans.com/comics/27937-god-of-blackfield',
                'https://reaperscans.com/comics/316621-the-great-mage-returns-after-4000-years',
                'https://reaperscans.com/comics/917294-kill-the-hero',
                'https://reaperscans.com/comics/563929-limit-breaker',
                'https://reaperscans.com/comics/535459-mercenary-enrollment',
                'https://reaperscans.com/comics/335355-sss-class-suicide-hunter',
                'https://reaperscans.com/comics/147221-superhuman-era',
                'https://reaperscans.com/comics/364640-the-tutorial-is-too-hard',
                'https://reaperscans.com/comics/326450-the-player-that-cant-level-up',
                'https://reaperscans.com/comics/276469-strongest-fighter',
                'https://reaperscans.com/comics/507776-return-of-the-frozen-player',
                'https://reaperscans.com/comics/585562-arcane-sniper']

    for url in url_list:
        find_manga_reaperzero(url)
