# Import the necessary modules for webscraping
from bs4 import BeautifulSoup
import requests
import random

# create an empty list for images, and fill the list with the appropriate file path for each image
images = []
path = "./images/"
for i in range(45):
    images.append(path + "image_" + str(i + 1) + ".png")
    

def retrieve_news():
    # parse the page request that has been converted to text from the specified URL
    url = "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNRFY2TVY4U0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=" \
          "US%3Aen"
    page = requests.get(url).text
    doc = BeautifulSoup(page, 'html.parser')

    # creete a list to contain the titles of the each of the hyperlinks from the webpage doc
    titles = []
    div = doc.find_all(class_='JtKRv')
    for d in div:
        innerhtml = d.decode_contents()
        titles.append(innerhtml)

    # create a list to contain the hyperlinks of the associated news articles from the webpage doc
    hrefs = []
    div = doc.find_all(class_="WwrzSb")
    for d in div:
        href = d.get('href')
        hrefs.append("https://news.google.com" + href.lstrip("."))

    # return the titles and hyperlinks zipped together in tuple format
    return zip(titles, hrefs)

# create a class for the hpyerlink tags
class HyperlinksTag:
    # make a constructor that contains the attributes for the title, link, image, and list element with its id to be written to the associated HTML doc
    def __init__(self, name, title, link):
        self.name = name
        self.title = title
        self.link = link
        self.id = "link_id"
        self.image = images.pop(int(random.random()))
        self.content = f'           <li id="link_id"><a href={self.link} target="_blank"><br><br>{self.title}</a><p><img src="{self.image}"></p></li>'

    # a function that will open the desired html doc, seek a specific tag, and write/insert the instance's content (list element), then close the file
    def write_link(self, filename, match, content):
        lines = open(filename).read().splitlines()
        index = lines.index(match)
        lines.insert(index, content)
        open(filename, mode='w').write('\n'.join(lines))

# create an object to house the zipped titles and hyperlinks
zipped_links = retrieve_news()

# create an empty list for each of the HyperlinksTag instances
hyperlinks = []
# Instatiate each Hyperlink object and append them to the hyperlinks list
i = 1
for z in zipped_links:
    name = "link_" + str(i)
    hyperlinks.append(HyperlinksTag(name, z[0][0], z[0][1]))
    i += 1

# write each list element in the hyperlinks list to the HTML doc desired. 
for link in hyperlinks:
    link.write_link('PyNews.html', match='        </ul>', content=link.content)


