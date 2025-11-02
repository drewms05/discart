# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program retrieves a user's
# Discog's data based on a given username


import discogs_api as disc
import time
from rich.progress import Progress


def get_account_info(username):
    """
    Retrive a user's Discogs collection data.

    Given a Discogs username for a public profile,
    retrieves the user's collection data as a list
    of dictionaries, where each dictionary represents
    a single release. Limited to 1 page of 100 per second.
    Returns the user's data, as well as the number of releaases they have.
    """

    # Retrive user info
    client = disc.Client('DiscArt', user_token='ZAapAoDKPbaKnwTRGPkogXxTULgzDJXnVCszAwtk')
    user = client.user(username)

    user_data = []

    # Retrieve information about the user's entire collection
    collection = user.collection_folders[0].releases
    albums = user.collection_folders[0].releases.count
    max_pages = (albums//100)+1
    collection.per_page = 100
    
    collection_page = 1
    album_count = 1

    # Download release data (including title and 
    # image URL) one page (100 items) at a time.
    with Progress() as progress:
        bar = progress.add_task('Retrieving collection data...', total = albums)
        while not progress.finished:
            releases = collection.page(collection_page)
            progress.update(bar, advance=1)
            if not releases:
                break
            for item in releases:
                progress.update(bar, advance=1, description=(f'Processing release {album_count} of {albums}...'))
                user_data.append(item.data)
                time.sleep(0.01)

                album_count += 1
            
            collection_page += 1

            if collection_page > max_pages:
                progress.finished

    return user_data, albums
