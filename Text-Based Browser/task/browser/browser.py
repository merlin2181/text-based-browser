import argparse
import os
from collections import deque
import requests
from requests.exceptions import HTTPError
import sys

# Create ability to pass a directory to the command line as well as give a help screen
browser = argparse.ArgumentParser()
browser.add_argument('dir', nargs='?', default=None, type=str, help='A directory to store your downloaded webpages')
args = browser.parse_args()

if args.dir:
    if not os.path.exists(args.dir):
        os.mkdir(args.dir)


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


def save_website(f_path, website_page):
    """
    Saves a website for off-line browsing
    :param f_path: The path to the directory to save the file
    :param website_page: the name of the file
    :return: none
    """
    with open(f_path, 'w') as f:
        f.writelines(website_page)


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
    try:
        user_site = requests.get(os.path.join('https://', url))
        user_site.raise_for_status()
    except HTTPError:
        return 'Error: Incorrect URL'
    except Exception:
        return 'Error: Incorrect URL'

    if user_site:
        return user_site.text
    return user_site.status_code


history = deque()  # Browser history
forward = deque()  # ability to go forward in Browser history, not implemented yet
websites = {}  # dictionary of websites used for history keeping and to check files

# sets the path to the directory to save websites
if args.dir:
    path = args.dir + '/'
else:
    path = ""

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
                save_website(os.path.join(path, site[0]), webpage)
                print(webpage)
            history.append(websites[website])
        else:
            print("Error: Incorrect URL\n")
