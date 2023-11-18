import pandas as pd
from collections import defaultdict

def page_count(data, target_column='user_journey'):
    
    # Split the strings in the target column and create a list of pages
    
    pages_list = []
    for journey in data[target_column].str.split('-'):
        for page in journey:
            if pd.notna(page) and page != '':
                pages_list.append(page)

    # Count the occurrences of each page
    page_counts = pd.Series(pages_list).value_counts()

    return page_counts


def page_presence(data, target_column='user_journey'):
    # Initialize an empty set to store unique pages
    unique_pages = set()

    # Iterate through each journey and add unique pages to the set
    data[target_column].str.split('-').apply(lambda x: unique_pages.update(x))

    # Convert the set of unique pages to a list
    unique_pages_list = list(unique_pages)

    # Create a DataFrame with columns as unique pages
    presence_df = pd.DataFrame(0, index=data.index, columns=unique_pages_list)

    # Update the DataFrame based on the presence of each page in the journey
    for page in unique_pages_list:
        presence_df[page] = data[target_column].apply(lambda x: page in x.split('-')).astype(int)

    return presence_df


def page_destination(data, target_column='user_journey'):
    # Initialize an empty dictionary to store the page destinations
    page_destinations = {}

    # Iterate through each journey
    for journey in data[target_column].str.split('-'):
        # Iterate through each page in the journey
        for i, page in enumerate(journey[:-1]):
            current_page = page.strip()
            next_page = journey[i + 1].strip()

            # Check if the current page is already in the dictionary
            if current_page in page_destinations:
                # If yes, update the list of destinations for the current page
                page_destinations[current_page].append(next_page)
            else:
                # If no, create a new entry for the current page in the dictionary
                page_destinations[current_page] = [next_page]

    # Count the occurrences of each page as a destination
    page_destination_counts = {page: pd.Series(destinations).value_counts() for page, destinations in page_destinations.items()}

    return page_destination_counts



def page_dest(data, target_column='user_journey'):
    # Initialize an empty dictionary to store the page destinations
    page_destinations = defaultdict(list)

    # Iterate through each journey
    for journey in data[target_column].str.split('-'):
        journey = [page.strip() for page in journey]
        
        # Iterate through each page in the journey
        for i in range(len(journey) - 1):
            current_page = journey[i]
            next_page = journey[i + 1]
            
            # Update the list of destinations for the current page
            page_destinations[current_page].append(next_page)

    # Count the occurrences of each page as a destination
    page_destination_counts = {page: defaultdict(int) for page in page_destinations}
    for page, destinations in page_destinations.items():
        for destination in destinations:
            page_destination_counts[page][destination] += 1

    return page_destination_counts


def avg_journey_length(data, user_column='user_id' ,target_column='user_journey'):
    
    # journey_df = pd.DataFrame()
    journey  = data[target_column].str.split('-')    
    journey_length = journey.apply(len)
    
    result_df = pd.DataFrame(
        {
            user_column: data[user_column],
            "Average_Journey" : journey_length
        })
    
    return result_df.groupby(user_column)["Average_Journey"].mean().reset_index()       
    