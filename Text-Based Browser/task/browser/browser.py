import argparse
import os
from collections import deque

browser = argparse.ArgumentParser()
browser.add_argument('dir', nargs='?', default=None, type=str, help='A directory to store your downloaded webpages')
args = browser.parse_args()

if args.dir:
    if not os.path.exists(args.dir):
        os.mkdir(args.dir)


def check_website(url, filepath):
    website_list = ['nytimes.com', 'bloomberg.com']
    if url in website_list:
        return True
    if check_file(filepath, url):
        return 'file'
    return False


def check_file(file_path, url):
    file_path += url
    if os.path.isfile(file_path):
        return True
    return False


def save_website(file_path, website_name):
    with open((file_path), 'w') as f:
        f.writelines(website_name)


nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

history = deque()
forward = deque()
websites = {'bloomberg.com': bloomberg_com, 'nytimes.com': nytimes_com}
while True:

    # This keeps the path variable from changing everytime.
    if args.dir:
        path = args.dir + '/'
    else:
        path = ""

    # Main part of the program
    website = input()
    if website == 'exit':
        exit()
    elif website == 'back':
        if len(history) <= 1:
            continue
        else:
            forward.append(history.pop())
            print(history[-1])
    else:
        answer = check_website(website, path)
        if answer == 'file':
            path += website
            with open(path) as web:
                for line in web:
                    print(line.strip())
            print('\r')
            history.append(websites[website + '.com'])
        elif answer:
            name = website[:-4]
            path += name
            print(websites[website])
            history.append(websites[website])
            save_website(path, websites[website])
        else:
            print('Error: Incorrect URL\n')
