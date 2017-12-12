"""A module for grabbing end or year critic list info. 

This module can be used to grab where each album on the End Year Critic List on
albumoftheyear.org fell on certain critics lists. 
"""

import sys
import os
wd = os.path.abspath('.')
sys.path.append(wd + '/../')
from collections import defaultdict
import re
from special_utilities import select_soup, grab_contents_key
from utils.query_utilities import get_html, format_query
from utils.storage_utilities import store_in_mongo
from albums_of_year_lst_ind import find_score

def grab_critics_info(critics_names, critics_hrefs):
    """Pull all relevant information from a critics list page. 

    Issue get requests on all the critics list pages, returning the resulting
    information in a dicionary. 

    Args: 
    ----
        critics_names: list of strings
        critics_hrefs: list of strings

    Return: 
    ------
        json_dct: dictionary of lists 
    """

    critics_hrefs_lst = list(critics_hrefs.values())
    critics_hrefs_values = critics_hrefs_lst[0]

    json_dct = defaultdict(list)

    # Compile this here since we only need to do this once.
    regex = re.compile("^\d+\.")

    # Cycle through each one of the critics. 
    critics_names_lst = list(critics_names.values())
    for idx, critic_name in enumerate(critics_names_lst[0]): 
        
        critic_lst_content_vals, soup = \
                get_critic_lst_content(critics_hrefs_values, idx)
        num_albums_idx = len(critic_lst_content_vals) 
        # Cycle through each one of the ablums on the critics lists. 
        for idx2, values in enumerate(critic_lst_content_vals, 1):
            # Each album is stored in a separate "Post-#". 
            post = soup.select('#post-' + str(num_albums_idx))[0]

            album_title, album_title_txt = get_album_title(post)            

            rating_text = regex.findall(album_title_txt)
            rating = parse_rating(rating_text, idx2)

            critic_dct = {'Critic' : critic_name, 'Rating' : rating}
            # 'User Score': user_score, 'Critic Score': critic_score}
            json_dct[album_title].append(critic_dct)
            num_albums_idx -= 1

    return json_dct 

def get_critic_lst_content(critics_hrefs_values, critic_lst_idx):
    """Grab the CSS element that holds all relevant info. for a critic list. 

    For the critic href at the inputted idx in the critics_hrefs_values, grab
    all of the items with the class '.listLargeTitle'. This will then be used 
    to cycle through each one of them and grab information from them. 

    Args: 
    ----
        critics_hrefs_values: list of strings 
        critic_lst_idx: int

    Return: 
    ------
        critic_lst_content_vals: list 
        soup: bs4.BeautifulSoup object
    """

    base_individual_list_url = 'http://www.albumoftheyear.org'
    css_selectors = ['.listLargeTitle']

    critic_url = base_individual_list_url + critics_hrefs_values[critic_lst_idx]
    soup = get_html(base_individual_list_url + critics_hrefs_values[critic_lst_idx]) 

    critic_content_lst = list(select_soup(soup, css_selectors).values())
    critic_lst_content_vals = critic_content_lst[0]
    # We reverse them because they are posted from the highest ranked (worst album)
    # to the lowest rank (i.e. Post-1 is the highest ranked album on the critic list).
    critic_lst_content_vals.reverse()

    return critic_lst_content_vals, soup

def get_album_title(post): 
    """Parse the inputted post bs4 tag

    Grab the album title from our inputted post. Return the full text in addition 
    to just the album title because the full text potentially has the rating in it. 

    Args: 
    ----
        post: bs4.element.Tag

    Return: 
    ------
        album_title: str
        album_title_text: str
    """

    album_title_txt = post.select('.listLargeTitle')[0].text
    split_album_title_txt = album_title_txt.split('-')

    if len(split_album_title_txt) == 2 or 'Sleater' in split_album_title_txt:
        album_title = (split_album_title_txt[-1]\
                        .encode('ascii', 'xmlcharrefreplace').strip()
                        .decode('utf-8'))
    else: 
        album_title = ('-'.join(split_album_title_txt[1:])
                         .encode('ascii', 'xmlcharrefreplace').strip()
                         .decode('utf-8'))

    return album_title, album_title_txt

def parse_rating(rating_txt, idx): 
    """Parse the rating text to grab an album's rating. 

    Get the rating for the current album on the critics list. This falls into one 
    of two scenarios: (1). Either the rating is already in the inputted rating_txt,   
    and it needs to be parsed, or (2). It's not there, and we need to assign it 
    the idx (this is why we reversed the list in the get_critic_lst_content()
    function). 

    Args: 
    ----
        rating_txt: str
            Text that potentially holds the rating. 
        idx: int
            Holds the rating if the text does not. 

    Return: int
    """

    if len(rating_txt) >= 1: 
        rating = int(rating_txt[0].replace('.', ''))
    else: 
        rating = idx

    return rating

if __name__ == '__main__':
    lists_url = 'http://www.albumoftheyear.org/lists.php'

    soup = get_html(lists_url)
    critics_content = select_soup(soup, '.criticListBlockTitle')
    critics_names = grab_contents_key(critics_content, "text")
    critics_links = grab_contents_key(critics_content, 'a')
    critics_hrefs = grab_contents_key(critics_links, 'href')

    raw_output = grab_critics_info(critics_names, critics_hrefs)
    formatted_output = [{"Album Title": k, "Critics Scores": v} for \
            k, v in raw_output.items()]
    store_in_mongo(formatted_output, 'music', 'music_lists', 
                        key="Album Title")

