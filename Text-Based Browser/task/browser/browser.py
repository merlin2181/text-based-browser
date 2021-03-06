import argparse
import os
from collections import deque
import requests
from requests.exceptions import HTTPError
import sys
from bs4 import BeautifulSoup, SoupStrainer
from colorama import Fore, init


def check_name(url):
    """
    Checks the url to see if it contains one of the suffixes in the list below. If it does, it
    is a true URL
    :param url: the webpage name to search
    :return: True or False
    """
    tld_list = ['.com', '.org', '.edu', '.net', '.co', '.us']  # includes the top 5 TLDs
    check_site = os.path.splitext(url)
    if check_site[1] and check_site[1] in tld_list:
        return True
    return False


def check_website(url, filepath):
    """
    Checks whether the user inputted website is a website to GET, is saved as a file or
    incorrectly entered.
    :param url: the website name from the user input
    :param filepath: the path used to check to see if there is a saved file
    :return: True for website, 'file' for saved file, False for incorrect website name
    """
    if check_name(url):
        return True
    if check_file(filepath, url):
        return 'file'
    return False


def check_file(f_path, url):
    """
    Checks to see if a file exists in a given directory
    :param f_path: the path of the directory
    :param url: the name of the file
    :return: True or False
    """
    if os.path.isfile(os.path.join(f_path, url)):
        return True
    return False


def save_website(f_path, website_page, anchor_list):
    """
    Saves a website for off-line browsing
    :param f_path: The path to the directory to save the file
    :param website_page: the name of the file
    :return: none
    """
    with open(f_path, 'w') as f:
        for line in website_page:
            if line in anchor_list:
                f.write(Fore.BLUE + line + '\n')
            else:
                f.write(line + '\n')


def print_saved_website(f_path):
    """
    Outputs a saved website file
    :param f_path: the full path and file name
    :return: none
    """
    with open(f_path) as f:
        print(*f)
    print('\r')


def get_website(url):
    """
    function to get GET a website using the user input.  Checks for errors such as incorrect
    spelling of website name
    :param url: the website name to GET
    :return: string "Error: Incorrect URL" if there is an error, the text of the website or
    the status code from the attempted GET if it is out of range
    """
    if not url.startswith('https://') or not url.startswith('http://'):
        url = os.path.join('https://', url)
    try:
        user_site = requests.get(url)
        user_site.raise_for_status()
    except HTTPError:
        return 'Error: Incorrect URL'
    except Exception:
        return 'Error: Incorrect URL'
    if user_site:
        return user_site.content
    return user_site.status_code


# Initialize Colorama
init(autoreset=True)

# Create ability to pass a directory to the command line as well as give a help screen
browser = argparse.ArgumentParser()
browser.add_argument('dir', nargs='?', default=None, type=str, help='A directory to store your downloaded webpages')
args = browser.parse_args()

# Creates a directory and sets a path to the directory to save websites
if args.dir:
    if not os.path.exists(args.dir):
        os.mkdir(args.dir)
    path = args.dir + '/'
else:
    path = ""

history = deque()  # Browser history
forward = deque()  # ability to go forward in Browser history, not implemented yet
websites = {}  # dictionary of websites used for history keeping and to check files

# Setup a search filter for websites. Only return the following elements using 'parse_only' attribute
elements = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'a', 'ul', 'ol', 'li', 'title']
search_for = SoupStrainer(elements)

while True:
    website = input()
    site = os.path.splitext(website)  # splits website into a tuple ('name', 'extension')
    if website == 'exit':
        sys.exit()
    elif website == 'back':
        if len(history) <= 1:
            continue
        else:
            forward.append(history.pop())
            print_saved_website(os.path.join(path, history[-1]))
    else:
        answer = check_website(website, path)
        if answer == 'file':
            if check_name(website):
                websites[website] = site[0]
                with open(os.path.join(path, site[0])) as web:
                    print(*web)
            else:
                websites[website] = website
                print_saved_website(os.path.join(path, website))
            print('\r')
            history.append(websites[website])
        elif answer:
            websites[website] = site[0]
            webpage = get_website(website)
            if type(webpage) == int:
                print(f"Error #{webpage}")
            else:
                soup = BeautifulSoup(webpage, 'html.parser', parse_only=search_for)
                link_list = [element.text for element in soup.find_all('a')]
                save_website(os.path.join(path, site[0]), soup.stripped_strings, link_list)
                for string in soup.stripped_strings:
                    if string in link_list:
                        print(Fore.BLUE + string)
                    else:
                        print(string)
            history.append(websites[website])
        else:
            print("Error: Incorrect URL\n")
