# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program downloads the unique cover
# art for every releaes in a user's Discogs collection

import os
import sys
from rich.progress import Progress
from PIL import Image
import requests as req
from io import BytesIO
from check_url import check_url


def download_images(username, user_data, albums):
    """
    Download cover art for a given user's Discogs collection.

    Creates a directory ./username_Images if it does not already exist,
    and for each item in a given dataset of Discogs releases, Downloads
    the cover art if the release has any, and if the image is not
    already present in ./username_Images. Returns a new dataset with
    items lacking a cover removed, as well as the number of items that
    were found to not have a cover. Works if running the script by itself or as executable.
    """
    # For resizing art
    size = (600, 600)

    # So that Discogs allows me to download stuff
    # (I have registered the app as 'DiscArt' on their website)
    headers = {
        'User-Agent': 'DiscArt https://github.com/drewms05/discart',
        'Referer': 'https://www.discogs.com/'
    }
    album_count = 1

    # Creates './username_Images' if is does not exist
    if getattr(sys, 'frozen', False):
        image_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        image_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')
    image_dir = os.path.join(image_dir, f'{username}_Images')
    
    if os.path.exists(image_dir):
        pass
    else:
        os.mkdir(image_dir)

    # Remove releases which don't have a cover
    no_cover = 0
    new_data = []
    for item in user_data:
        if item['basic_information']['cover_image'] == '':
            no_cover += 1
            continue
        else:
            new_data.append(item)

    albums = len(new_data)

    # Downloads cover art one image at a time,
    # but importantly skips images that are already downloaded.
    # This is achieved by naming each image after the unchanging
    # ID tied to its release.
    with Progress() as progress:
        bar = progress.add_task('Downloading cover art...', total = albums)
        for item in new_data:
            progress.update(bar, advance=1, description=(f'Downloading image {album_count} of {albums}...'))
            path = rf'{image_dir}/{item['basic_information']['id']}.jpeg'
            # Image is already downloaded
            if os.path.exists(path):
                item['local_path'] = path
                pass
            # Image is not already downloaded
            else:
                url = (item['basic_information']['cover_image'])
                valid = check_url(url)
                if not valid:
                    print(f'\nImage at {url} skipped. URL is invalid.')
                    continue
                response = req.get(url, headers=headers)
                response.raise_for_status()
                image = Image.open(BytesIO(response.content))
                image = image.resize((size), Image.Resampling.LANCZOS)
                path = rf'{image_dir}/{item['basic_information']['id']}.jpeg'
                image.save(path)
            item['local_path'] = path
            album_count += 1

    return new_data, no_cover
