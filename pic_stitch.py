# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program stiches the square images in a 
# directory into a roughly square collage.


import os
import shutil
import sys
from PIL import Image
import math
from rich.progress import Progress


def pic_stitch(username, user_data):
    """
    Create a collage out of a group of images.

    The images are in a directory named after a given username,
    and images may be used more than once based on how many
    corresponding items are present in the given dataset. The 
    final image is limited to a size of 10000x10000 pixels (100000000 total)
    Works if running the script by itself or as executable.
    """
    # Get the image directory
    if getattr(sys, 'frozen', False):
        image_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        image_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')

    image_dir = os.path.join(image_dir, f'{username}_Images')
    
    release_count = len(user_data)

    # Recursively deletes './Rows' if it exists,
    # and creates an empty version.
    if getattr(sys, 'frozen', False):
        row_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        row_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')

    # Creates the Rows directory
    row_dir = os.path.join(row_dir, 'Rows')
    if os.path.exists(row_dir):
        shutil.rmtree(row_dir)
    os.mkdir(row_dir)
    
    # Calculates the dimensions in images of the collage
    rows = math.isqrt(release_count)
    remainder = release_count-(rows*rows)
    if(remainder > rows):
        columns = rows+1
        remainder -= rows
    else:
        columns = rows

    if remainder == 0:
        total_rows = rows
    else:
        total_rows = rows+1


    # Calculates the size that each image needs to be to make the collage be within 
    Image.MAX_IMAGE_PIXELS = 100000000
    pixel = (10000//columns)
    
    # Creates each row of the collage
    with Progress() as progress:
        bar = progress.add_task('Generating rows...', total = total_rows)
        for row in range(total_rows):
            progress.update(bar, advance=1, description=(f'Generating row {row+1} of {total_rows}...'))
            try:
                top_image = Image.open(user_data[(row)*columns]['local_path'])
                top_image = top_image.resize((pixel, pixel), Image.Resampling.LANCZOS)
                top_image.save(rf'{row_dir}/row{row+1}.jpeg')
                for column in range(columns-1):
                    image1 = Image.open(rf'{row_dir}/row{row+1}.jpeg')
                    image2 = Image.open(user_data[((row*columns)+column+1)]['local_path'])
                    image2 = image2.resize((pixel, pixel), Image.Resampling.LANCZOS)
                    width = image1.width + image2.width
                    height = image1.height
                    new_image = Image.new('RGB', (width, height))
                    new_image.paste(image1, (0, 0))
                    new_image.paste(image2, (image1.width, 0))
                    new_image.save(rf'{row_dir}/row{row+1}.jpeg')
            except:
                break

    # Get the working directory, where the collage will be saved.
    if getattr(sys, 'frozen', False):
        top_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        top_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')

    # Combines the separate rows into the full collage.
    with Progress() as progress:
        bar = progress.add_task('Combining rows...', total = total_rows)
        try:
            collage = Image.open(rf'{row_dir}/row1.jpeg')
            collage.save(rf'{top_dir}/collage.jpeg')
            for row in range(1, total_rows):
                progress.update(bar, advance=1, description=(f'Combining row {row+1} of {total_rows}...'))
                image1 = Image.open(rf'{top_dir}/collage.jpeg')
                image2 = Image.open(rf'{row_dir}/row{row+1}.jpeg')
                width = image1.width
                height = image1.height + image2.height
                new_image = Image.new('RGB', (width, height))
                new_image.paste(image1, (0, 0))
                new_image.paste(image2, (0, image1.height))
                new_image.save(rf'{top_dir}/collage.jpeg')
        except Exception as e:
            print(e)
        progress.update(bar, advance=1, description=(f'Combining row {row+1} of {total_rows}...'))
    
    # Recursively deletes the rows directory
    if os.path.exists(row_dir):
        shutil.rmtree(row_dir)

    # Convert the collage into a PNG 
    if getattr(sys, 'frozen', False):
        top_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        top_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')
