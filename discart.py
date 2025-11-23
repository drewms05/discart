# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program takes a user's public
# Discogs username as input and creates
# a collage of every album cover in their collection


import time
import os
import shutil
import sys
import subprocess
import copy
from get_account_info import get_account_info
from filter_data import filter_data
from sort_data import sort_data
from download_images import download_images
from pic_stitch import pic_stitch
from word_counter import word_counter
from string_validator import string_validator
from duplicate_remover import duplicate_remover


def move_collage(username):
    """
    Move the collage to the downloads folder.

    Moves the collage to the downloads folder, works
    if running script by itself or as executable. Returns
    True if successe, otherwise returns False.
    """
    # Get path
    if getattr(sys, 'frozen', False):
        top_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        top_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')

    # Delete file at path
    if os.path.exists(rf'{top_dir}/collage.jpeg'):
        shutil.move(rf'{top_dir}/collage.jpeg',
                    (rf'{os.path.expanduser("~/Downloads")}/collage_{username}.jpeg'))
        return True
    else:
        return False
    
def delete_user_data(username):
    """
    Delete the images associated with a given user.
    
    Deletes the images that correspond to the given user,
    works if running the script by itself or as exexutable.
    Returns True if success, otherwise returns False.
    """
    # Get path
    if getattr(sys, 'frozen', False):
        image_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        image_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')
    image_dir = os.path.join(image_dir, f'{username}_Images')
    
    # Recursively delete directory at path
    if os.path.exists(image_dir):
        shutil.rmtree(image_dir)
        return True
    else:
        return False

def show_collage():
    """
    Display the collage image.
    
    Display the file ./collage.jpeg in the default image
    viewer. Works if running the script by itself or as executable.
    Returns True if success, otherwise reutrns False.
    """
    # Get path
    if getattr(sys, 'frozen', False):
        top_dir = (f'{os.path.dirname(sys.executable)}')
    else:
        top_dir = (f'{os.path.dirname(os.path.abspath(__file__))}')
    collage_dir = os.path.join(top_dir, 'collage.jpeg')

    # Open file at path in default image viewer
    if os.path.exists(collage_dir):
        subprocess.run(['open', collage_dir])
        return True
    else:
        return False

def main():
    """
    Run the main program.

    Allows the user to enter their public Discogs username
    and generate a collage of the releases in their collection.
    Only releases with a cover are included, and users can select
    filter and sort options to tune the collage to their liking.
    """
    # Used to store the user's Discogs username
    username = None 
    # Used to store the user's info retrieved from the Discogs API
    user_data = None
   
    while True:
        # Enter main menu
        print('\nWelcome to DiscArt, where you can visualize your Discogs collection for free!',
              '\nSimply enter your username and a collage of your collection will be generated and opened'
              '\n*Your Discogs account must be set to public'
              )

        # Retrive username
        # username = get_username(values[0])
        username = input('\nEnter your username: ')

        start = time.perf_counter()

        print('\n')

        # Make sure username meets minmum length requirements
        valid = string_validator(username)
        if valid is False:
            print('\nNot a valid Discogs username.')
            continue

        # Retrieve collection data
        try:
            user_data = get_account_info(username)
        except:
            print('\nUser not found. Make sure your account is public and try again.')
            continue

        # Download images and retrive new user data
        # where each release includes a local_path value
        user_data, no_cover = download_images(username, user_data[0], user_data[1])

        while True:
            working_user_data = copy.deepcopy(user_data)

            # Filter the user_data according the user_input
            while True:
                choice = input('Would you like to apply a filter? (Y/N): ')
                match choice:
                    case 'Y' | 'y':
                        while True:
                            print('\n1. Genre',
                                '\n2. Artist',
                                '\n3. Format',
                                '\n4. Year',
                                '\n5. Go back')
                            choice = input('\nPlease select one of the choices above: ')
                            match choice:
                                case '1':
                                    working_user_data = filter_data(working_user_data, 'Genre')
                                    break
                                case '2':
                                    working_user_data = filter_data(working_user_data, 'Artist')
                                    break
                                case '3':
                                    working_user_data = filter_data(working_user_data, 'Format')
                                    break
                                case '4':
                                    working_user_data = filter_data(working_user_data, 'Year')
                                    break
                                case '5':
                                    break
                                case _:
                                    print('\nNot a valid option. Please try again.')
                                    continue
                    case 'N' | 'n':
                        break
                    case _:
                        print('\nNot a valid option. Please try again.')
                        continue
                break

            # Sort the user_data according to user_input
            while True:
                choice = input('Would you like to sort your collage? (Y/N): ')
                match choice:
                    case 'Y' | 'y':
                        while True:
                            print('\n1. Artist',
                                '\n2. Title',
                                '\n3. Year',
                                '\n4. Go back')
                            choice = input('\nPlease select one of the choices above: ')
                            match choice:
                                case '1':
                                    working_user_data = sort_data(working_user_data, 'Artist')
                                    break
                                case '2': 
                                    working_user_data = sort_data(working_user_data, 'Title')
                                    break
                                case '3':
                                    working_user_data = sort_data(working_user_data, 'Year')
                                    break
                                case '4':
                                    break
                                case _:
                                    print('\nNot a valid option. Please try again.')
                                    continue
                    case 'N' | 'n':
                        break
                    case _:
                        print('\nNot a valid option. Please try again.')
                        continue
                break
            
            # Stitch the images into a collage located at ./collage.jpeg
            pic_stitch(username, working_user_data)

            end = time.perf_counter()
            elapsed = end - start

            print(f'\nYour collage has been generated! ({elapsed:.2f}s)')
            if no_cover == 1:
                print(f'{no_cover} release did not have a cover and has been omitted')
            elif no_cover > 1:
                print(f'{no_cover} releases did not have a cover and have been omitted')

            # For loop navigation later on
            leaving = True

            # Enter second menu
            while True:
                print('\n1. Open collage in default image viewer',
                      '\n2. Move your collage to your downloads folder',
                      '\n3. Choose different collage options',
                      '\n4. Retrieve new user data',
                      '\n5. Delete current user data',
                      '\n6. View fun facts'
                      '\n7. Exit DiscArt')
                choice = input('\nPlease select one of the choices above: ')
                match choice:
                    case '1':
                        result = show_collage()
                        if result is True:
                            print('\nDisplaying collage.')
                        else:
                            print('\nImage could not be located. It may have been moved.')
                        continue
                    case '2':
                        result = move_collage(username)
                        if result is True:
                            print('\nImage moved.')
                        else:
                            print('\nImage could not be located. It may already have been moved.')
                        continue
                    case '3':
                        choice = input('\nAre you sure? If you haven\'t moved your current collage to the Downloads folder, it will need to be regenerated in order to view it. (Y/N): ')
                        match choice:
                            case 'Y' | 'y':
                                leaving = False
                                start = time.perf_counter()
                                break
                            case 'N' | 'n':
                                continue
                            case _: 
                                print('Not a valid option. Aborting option change.')
                    case '4':
                        choice = input('\nAre you sure? If you haven\'t moved your current collage to the Downloads folder, it will need to be regenerated in order to view it. (Y/N): ')
                        match choice:
                            case 'Y' | 'y':
                                break
                            case 'N' | 'n':
                                continue
                            case _: 
                                print('Not a valid option. Aborting user switch.')
                    case '5':
                        choice = input('\nAre you sure? If you wish to regenerate your collage in the future, every cover will need to be downloaded again. (Y/N): ')
                        match choice:
                            case 'Y' | 'y':
                                result = delete_user_data(username)
                                if result is True:
                                    print('\nData deleted. Returning to main menu.')
                                    break
                                else:
                                    print('\nUser data not found. Returning to main menu.')
                                    break
                            case 'N' | 'n':
                                continue
                            case _: 
                                print('Not a valid option. Aborting data deletion.')
                    case '6':
                        longest = 0
                        title = ''
                        IDs = []
                        for item in working_user_data:
                            length = int(word_counter(item['basic_information']['title']))
                            if length > longest:
                                longest = length
                                title = item['basic_information']['title']
                            IDs.append(item['basic_information']['id'])
                        duplicates = duplicate_remover(IDs)

                        if duplicates > 1 or duplicates == 0:
                            print(f'\nYou have {duplicates} duplicates in your collection')
                        else:
                            print('\nYou have one duplicate in your collection')
                        print(f'\nThe longest title in your collection is \'{title}\'')

                        
                    case '7':
                        sys.exit()
                    case _:
                        print('\nNot a valid option. Please try again.')
                        continue
            if leaving is True:
                break
            else:
                continue

if __name__ == '__main__':
    main()
