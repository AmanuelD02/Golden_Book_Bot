from pprint import pprint as pp
from libgen_api import LibgenSearch
from bs4 import BeautifulSoup as bs4
import requests

s = LibgenSearch()

# Send message function


def send_msg(update, context, text="", reply_markup=None):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, reply_markup=reply_markup)

# Style information of the book and is used by admins


def styler_admin(name, author, year, genre):
    text = "<b>Book - " + name + "\n" + "Author</b> - " + "<i>" + author + "</i>" + "\n" + \
        "_______________" + "\n" + "<b>Year </b>- " + str(year) + "\n" + "Genre - " + genre + "\n" + \
        "_______________" + "\n" + "@golden_bookstore"
    return text

# style book information used in book request


def styler_users(name, author, year, size, link, extension):
    text = "<b>Book - " + name + "\n" + "Author</b> - " + "<i>" + author + "</i>" + "\n" + \
        "_______________" + "\n" + "<b>Year </b>- " + str(year) + "\n" + "Size - " + size + "\n" + \
        "_______________" + "\n" + "LINK - " + \
        f"<a href = '{link}'>" + f"{extension}</a>" + "\n"   "@golden_bookstore"
    return text


# Extract book link from a webpage
def link_extracter(LINK):
    book = None

    try:
        link = requests.get(LINK)
    except:
        return None

    if link.status_code == 200:
        soup = bs4(link.text, features="lxml")
        tags = soup.find_all('a')
        for tag in tags:
            if tag.text == 'GET':
                book = tag['href']
                return book

    return book


def search_book_by_title(title):

    return s.search_title(title)


def search_book_by_author(author):
    return s.search_author(author)


def json_to_txt(result):
    texts = []
    for book in result:

        link_extract = link_extracter(book['Mirror_1'])
        if link_extracter is None:
            continue
        txt = styler_users(book['Title'], book['Author'],
                           book['Year'], book['Size'], link_extract, book['Extension'])

        texts.append(txt)

    return texts


# a = search_book_by_title("ethiopia")

# pp(json_to_txt(a))
