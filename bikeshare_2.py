# First change for P3
# Commit for Refactor code step
# Commit for Refactor code step 2


import time
import calendar
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

START_TIME = 'Start Time'
CITY_NAME_ARR = ['chicago', 'new york city', 'washington']
MONTH_LIST = list(calendar.month_name)
MONTH_LIST[0] = 'All'
DAY_OF_WEEK_ARR = [
    'all',
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]
INVALID_INPUT_MESSAGE = 'Your input is not valid. Please try again'
TOOK_NUM_SECOND = '\nThis took %s seconds.'
DAY_OF_WEEK = 'Day Of Week'
DATAFRAME_EMPTY_MSG = 'DataFrame is empty!!'
START_STATION = 'Start Station'
END_STATION = 'End Station'

def print_pause(message_to_print):
    print(message_to_print)
    time.sleep(2)

def intro():
    print_pause("Hello! Let\'s explore some US bikeshare data!")

def valid_city_input():
    while True:
        response = input("Please enter city: ").lower()
        if response in CITY_NAME_ARR:
            break
        else:
            print_pause(INVALID_INPUT_MESSAGE)
    return response

def valid_month_input():
    while True:
        response = input("Please enter month: ").lower()
        if response.capitalize() in MONTH_LIST:
            break
        else:
            print_pause(INVALID_INPUT_MESSAGE)
    return response

def valid_day_of_week_input():
    while True:
        response = input("Please enter day of week: ").lower()
        if response in DAY_OF_WEEK_ARR:
            break
        else:
            print_pause(INVALID_INPUT_MESSAGE)
    return response

def valid_display_data_input(msg):
    while True:
        response = input(msg).lower()
        if response in ['yes', 'no']:
            break
        else:
            print_pause('Please enter yes or no')
    return response

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = valid_city_input()

    # get user input for month (all, january, february, ... , june)
    month = valid_month_input()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = valid_day_of_week_input()

    print('#'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    try:
        df = pd.read_csv(CITY_DATA[city])
        # Convert [Start Time] column to datetime
        df[START_TIME] = pd.to_datetime(df[START_TIME])
        # Extract [Start Hour] from [Start Time] column to create [Start Hour] column
        df['Start Hour'] = df[START_TIME].dt.hour
        # Extract [Month] from [Start Time] column to create [Month] column
        df['Month'] = df[START_TIME].dt.month
        # Extract [Day Of Week] from [Start Time] column to create [Day Of Week] column
        df[DAY_OF_WEEK] = df[START_TIME].dt.day_name()

        # Filter data by month
        if month != 'all':
            month_names = MONTH_LIST[1:]
            month = month_names.index(month.capitalize()) + 1
            df = df[df['Month'] == month]

        # Filter data by day of week
        if day != 'all':
            df = df[df[DAY_OF_WEEK] == day.capitalize()]

    except FileNotFoundError:
        print("File not found.")
    except pd.errors.OutOfBoundsDatetime:
        print("Cannot convert Start Time")
    except Exception as e:
        print('The exception: {}'.format(e))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print_pause('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    if not df.empty:

        # display the most common month
        popular_month = df['Month'].mode()[0]
        print_pause(f'Most common month: {MONTH_LIST[popular_month]}')


        # display the most common day of week
        popular_day_of_week = df[DAY_OF_WEEK].mode()[0]
        print_pause(f'Most common day of week: {popular_day_of_week}')


        # display the most common start hour
        popular_start_hour = df['Start Hour'].mode()[0]
        print_pause(f'Most common start hour: {popular_start_hour}')
    else:
        print_pause(DATAFRAME_EMPTY_MSG)

    print_pause(TOOK_NUM_SECOND % (time.time() - start_time))
    print('#'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print_pause('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    if not df.empty:

        # display most commonly used start station
        popular_start_station = df[START_STATION].mode()[0]
        print_pause(f'Most used start station: {popular_start_station}')


        # display most commonly used end station
        popular_end_station = df[END_STATION].mode()[0]
        print_pause(f'Most used end station: {popular_end_station}')


        # display most frequent combination of start station and end station trip
        group_start_end_station = df.groupby([START_STATION, END_STATION]).size().reset_index(name='num_start_end_station').sort_values(by='num_start_end_station', ascending=False)
        popular_start_station = group_start_end_station.iloc[0][START_STATION]
        popular_end_station = group_start_end_station.iloc[0][END_STATION]
        print_pause(f'Most start station and end station trip: {popular_start_station}-{popular_end_station}')

    else:
        print_pause(DATAFRAME_EMPTY_MSG)

    print_pause(TOOK_NUM_SECOND % (time.time() - start_time))
    print('#'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print_pause('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if not df.empty:
        # display total travel time
        total_travel_time = df['Trip Duration'].sum()
        print_pause(f'Total travel time: {total_travel_time}')

        # display mean travel time
        mean_travel_time = df['Trip Duration'].mean()
        print_pause(f'Mean travel time: {mean_travel_time}')
    else:
        print_pause(DATAFRAME_EMPTY_MSG)

    print_pause(TOOK_NUM_SECOND % (time.time() - start_time))
    print('#'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print_pause('\nCalculating User Stats...\n')
    start_time = time.time()

    if not df.empty:
        # Display counts of user types
        user_types_counts = df['User Type'].value_counts().rename_axis('Unique User Types').reset_index(name='Counts')
        print_pause(f'Counts of user types :\n {user_types_counts}')

        # Display counts of gender
        if 'Gender' in df.columns:
            gender_counts = df['Gender'].value_counts().rename_axis('Unique Gender').reset_index(name='Counts')
            print_pause(f'Counts of gender: \n {gender_counts}')

        # Display earliest, most recent, and most common year of birth
        BIRTH_YEAR_COLUMN_NAME = 'Birth Year'
        if BIRTH_YEAR_COLUMN_NAME in df.columns:
            earliest_year_of_birth = df[BIRTH_YEAR_COLUMN_NAME].min()
            print_pause(f'Earliest year of birth: {earliest_year_of_birth}')
            most_recent_year_of_birth = df[BIRTH_YEAR_COLUMN_NAME].max()
            print_pause(f'Most recent year of birth: {most_recent_year_of_birth}')
            count_of_common_year_of_birth = df[BIRTH_YEAR_COLUMN_NAME].value_counts().rename_axis('Unique Year Of Birth').reset_index(name='Counts').sort_values(by='Counts', ascending=False)
            most_common_year_of_birth = count_of_common_year_of_birth.iloc[0]['Unique Year Of Birth']
            print_pause(f'Most common year of birth: {most_common_year_of_birth}')
    else:
        print_pause(DATAFRAME_EMPTY_MSG)

    print_pause(TOOK_NUM_SECOND % (time.time() - start_time))
    print('#'*40)

def display_trip_data(df):
    view_data = valid_display_data_input("Would you like to view 5 rows of individual trip data? Enter yes or no: ")
    start_loc = 0
    while view_data == 'yes':
        data = df.iloc[start_loc:start_loc + 5]
        print_pause(data)
        start_loc += 5
        view_data = valid_display_data_input("Do you wish to continue?: ")


def main():
    while True:
        intro()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
