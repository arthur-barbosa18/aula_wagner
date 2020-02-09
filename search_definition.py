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
    definition = parse_request(url, word, "en py-2")
    definition_parse = definition[0].split("; ")
    return definition_parse


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

words = ["你好", "可以"]
for word in words:
    for (key, url) in URLS.items():
        if key == "mgdb":
            definition = parse_request_mdgb(url, word)
            item_mongo = create_response(key, definition, word)
            insert_mongo(item_mongo)
        elif key == "purpleculture":
            definition = parse_request_purple_culture(url, word)
            item_mongo = create_response(key, definition, word)
            insert_mongo(item_mongo)
        elif key == "archchinese":
            #definition = parse_request_archchinese(url, word)
            # parse de outro
