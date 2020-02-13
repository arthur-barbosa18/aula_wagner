from lxml import html
import requests
from pymongo import MongoClient


def insert_mongo(item):

    client = MongoClient("localhost", 27017)
    dict_chinese = client.dictionary_chinese.dict_chi

    dict_chinese.insert_one(item)


def parse_request(url, word, tag_name):
    html_page = requests.get("{0}{1}".format(url, word))
    tree = html.fromstring(html_page.content)

    return tree.xpath('//div[@class="{}"]/text()'.format(tag_name))


def purple(url, word, struct, tag_name):
    html_page = requests.get("{0}{1}".format(url, word))
    tree = html.fromstring(html_page.content)
    return tree.xpath('//{}[@class="{}"]/text()'.format(struct, tag_name))


def parse_request_mdgb(url, word):
    # html_page = requests.get("{0}{1}".format(url, word))
    # tree = html.fromstring(html_page.content)
    # definition = tree.xpath('//div[@class="defs"]/text()')
    definition = parse_request(url, word, "defs")
    # word_utf = html_page.url[html_page.url.find("wdqb=") + 5 :]
    definition_parse = ", ".join(
        [i[:-1] for i in definition if "modal verb" not in i and ", " != i and "variant of" not in i]
    )
    definition_parse = definition_parse.split(",")
    definition_parse = [i.strip() for i in definition_parse if i.strip() != ""]

    return definition_parse


def parse_request_purple_culture(url, word):
    try:
        definition = purple(url, word, "span", "en")

        if not any(definition):
            definition = purple(url, word, "div", "en py-2")
        if any(definition):
            return definition[0].split("; ")
        return definition
    except Exception as err:
        print(err)
        import ipdb

        ipdb.set_trace()  # breakpoint 96b08e4d //


def parse_request_archchinese(url, word):
    tag_name = "col-md-7"
    html_page = requests.get("{0}{1}".format(url, word))
    tree = html.fromstring(html_page.content)
    definition = tree.xpath('//p[@class="{}"]/text()'.format(tag_name))
    ##TODO, NOT WORK YET


URLS = {
    "mgdb": " https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb=",
    "purpleculture": "https://www.purpleculture.net/dictionary-details/?word=",
    "archchinese": "https://www.archchinese.com/chinese_english_dictionary.html?find=",
}


def create_response(origin, parsed_definition, word):
    word = word.encode("gb2312")
    return {"origin": origin, "word": word, "definition": parsed_definition}


# word = "可以"
# word = "吃"'gb2312'z

# words = ["中", "你好", "可以"]
words = ["我吃的东西", "鱼饼", "公司", "肚子", "不舒服", "妻子", "过得", "几天", "完全", "商场", "有的时候", "风", "有风"]


words = [i[:-1] for i in list(open("words_chinese.txt", "r"))]
import ipdb

ipdb.set_trace()  # breakpoint fcfae393 //

for word in words:
    for (site, url) in URLS.items():
        if site == "mgdb":
            continue
            # definition = parse_request_mdgb(url, word)
            # item_mongo = create_response(site, definition, word)
            # insert_mongo(item_mongo)
        elif site == "purpleculture":
            definition = parse_request_purple_culture(url, word)
            item_mongo = create_response(site, definition, word)
            insert_mongo(item_mongo)
        elif site == "archchinese":
            continue
            # definition = parse_request_archchinese(url, word)
            # parse de outro


##install mongodb

##https://treehouse.github.io/installation-guides/mac/mongo-mac.html
