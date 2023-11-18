def filter_unique_values(input_str):
    # Split the input string into a list
    values_list = input_str.split('-')

    # Use a set to keep track of unique values while maintaining order
    unique_values_set = set()
    unique_values_list = []

    # Iterate through the list and add unique values to the set and list
    for value in values_list:
        if value not in unique_values_set:
            unique_values_set.add(value)
            unique_values_list.append(value)

    # Join the unique values back into a string
    result_str = '-'.join(unique_values_list)

    return result_str

def remove_page_duplicates(df,col='user_journey'):
    # This function takes a datframe, cleans the user journey duplicate values, and returns a new dataframe
        
    new_df = df.copy()
    new_df["user_journey_clean"] = df[col].apply(filter_unique_values)
    new_df = new_df.drop(col,axis=1)
    new_df  = new_df.rename(columns={"user_journey_clean":"user_journey"}) #rename the column
    return new_df

def group_by(data, group_column='user_id', target_column='user_journey', sessions='All', count_from='last'):
    # Make a copy of the original data to avoid modifying the supplied one
    grouped_data = data.copy()

    # If sessions is an integer, filter the required number of sessions
    if isinstance(sessions, int):
        if count_from == 'first':
            grouped_data = grouped_data.groupby(group_column).head(sessions)
        elif count_from == 'last':
            grouped_data = grouped_data.groupby(group_column).tail(sessions)

    # Group the data by the specified column and concatenate the strings
    grouped_data = grouped_data.groupby(group_column)[target_column].agg(lambda x: '-'.join(x)).reset_index()

    return grouped_data


def remove_pages(data, pages=['Log in'], target_column='user_journey'):
    # Make a copy of the original data to avoid modifying the supplied one
    cleaned_data = data.copy()

    # Remove specified pages from the target column
    cleaned_data[target_column] = cleaned_data[target_column].apply(lambda x: '-'.join([page for page in x.split('-') if page not in pages]))

    return cleaned_data
