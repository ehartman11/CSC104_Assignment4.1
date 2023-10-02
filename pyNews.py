from bs4 import BeautifulSoup
import requests
import random

images = []
path = "./images/"
for i in range(45):
    images.append(path + "image_" + str(i + 1) + ".png")

print()


def retrieve_news():
    url = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFY2TVY4U0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=" \
          "US%3Aen"
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    titles = []
    div = doc.find_all(class_='JtKRv')
    for d in div:
        innerhtml = d.decode_contents()
        titles.append(innerhtml)

    hrefs = []
    div = doc.find_all(class_="WwrzSb")
    for d in div:
        href = d.get('href')
        hrefs.append("https://news.google.com" + href.lstrip("."))

    return zip(titles, hrefs)


class HyperlinksTag:
    def __init__(self, name, title, link):
        self.name = name
        self.title = title
        self.link = link
        self.id = "link_id"
        self.image = images.pop(int(random.random()))
        self.content = f'           <li id="link_id"><a href={self.link} target="_blank"><br><br>{self.title}</a><p><img src="{self.image}"></p></li>'

    def write_link(self, filename, match, content):
        lines = open(filename).read().splitlines()
        index = lines.index(match)
        lines.insert(index, content)
        open(filename, mode='w').write('\n'.join(lines))


zipped_links = zip(retrieve_news())
hyperlinks = []
i = 1

for z in zipped_links:
    name = "link_" + str(i)
    hyperlinks.append(HyperlinksTag(name, z[0][0], z[0][1]))
    i += 1

for link in hyperlinks:
    link.write_link('PyNews.html', match='        </ul>', content=link.content)


