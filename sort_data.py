# Drew Schlabach
# schlabad@oregonstate.edu
# CS 361
# Assignment 5
# 11/3/25
# This program takes a user's Discogs
# data and sorts it based on given criteria


def sort_data(user_data, method):
    """
    Sort Discogs data.

    Goes through a menu that allows users to 
    sort their discogs data by Artist, Title
    or Year. Returns the new dataset.
    """
    match method:
        case 'Artist':
            for item in user_data:
                if (item['basic_information']['title'].lower()).startswith('the '):
                    item['alphabet_title'] = item['basic_information']['title'][4:]
                else:
                    item['alphabet_title'] = item['basic_information']['title']
                if (item['basic_information']['artists'][0]['name'].lower()).startswith('the '):
                    item['alphabet_name'] = item['basic_information']['artists'][0]['name'][4:]
                else:
                    item['alphabet_name'] = item['basic_information']['artists'][0]['name']
            user_data = (sorted(user_data, key=lambda x: (x['alphabet_name'].lower(), x['alphabet_title'].lower())))
        case 'Title':
            for item in user_data:
                if (item['basic_information']['title'].lower()).startswith('the '):
                    item['alphabet_title'] = item['basic_information']['title'][4:]
                else:
                    item['alphabet_title'] = item['basic_information']['title']
            user_data = (sorted(user_data, key=lambda x: x['alphabet_title'].lower()))
        case 'Year':
            user_data = (sorted(user_data, key=lambda x: x['basic_information']['year']))
    
    return user_data
