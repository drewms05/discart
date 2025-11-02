# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program takes a user's Discogs
# data and filters it based on given criteria


def filter_data(user_data, method):
    """
    Filter Discogs data.

    Goes through a menu that allows users to 
    filter their discogs data by Genre, Artist,
    Format, or Year. Returns the new dataset.
    """
    match method:
        case 'Genre':
            genres = []
            new_data = []
            for item in user_data:
                for genre_name in item['basic_information']['genres']:
                    if genre_name in genres:
                        pass
                    else:
                        genres.append(genre_name)

            for name in genres:
                print(name)
            
            while True:
                choice = input('\nPlease choose an option from the list above: ')
                if choice in genres:
                    for item in user_data:
                        for genre_name in item['basic_information']['genres']:
                            if genre_name == choice:
                                new_data.append(item)
                            else:
                                pass
                    break
                else:
                    print('\nNot a valid option. Please try again.')


        case 'Artist':
            artists = []
            new_data = []
            for item in user_data:
                for artist_name in item['basic_information']['artists']:
                    if artist_name['name'] in artists:
                        pass
                    else:
                        artists.append(artist_name['name'])

            artists.sort()
            for name in artists:
                print(name)
            
            while True:
                choice = input('\nPlease choose an option from the list above: ')
                if choice in artists:
                    for item in user_data:
                        for artist_name in item['basic_information']['artists']:
                            if artist_name['name'] == choice:
                                new_data.append(item)
                            else:
                                pass
                    break
                else:
                    print('\nNot a valid option. Please try again.')

        case 'Format':
            formats = []
            new_data = []
            for item in user_data:
                format = item['basic_information']['formats'][0]['name']
                if format in formats:
                    pass
                else:
                    formats.append(format)

            for format in formats:
                print(format)

            while True:
                choice = input('\nPlease choose an option from the list above: ')
                if choice in formats:
                    for item in user_data:
                        format = item['basic_information']['formats'][0]['name']
                        if format == choice:
                            new_data.append(item)
                        else:
                            pass
                    break
                else:
                    print('\nNot a valid option. Please try again.')

        case 'Year':
            years = []
            new_data = []
            for item in user_data:
                year = item['basic_information']['year']
                if year in years:
                    pass
                else:
                    years.append(year)

            years.sort()
            for year in years:
                print(year)

            while True:
                choice = int((input('\nPlease choose an option from the list above: ')))
                if choice in years:
                    for item in user_data:
                        year = item['basic_information']['year']
                        if year == choice:
                            new_data.append(item)
                        else:
                            pass
                    break
                else:
                    print('\nNot a valid option. Please try again.')
    
    return new_data
