import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore bikeshare data from particular US cities!')

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Select Chicago, New york city, or Washington: ').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Please select Chicago, New york city, or Washington ').lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Select month between January and June, or type \'all\' to see all months: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Please select month between January to june, or type \'all\' to see all months: ').lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('What day of the week would you like to select? ').lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input ('Please select Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday  or type \'all\' to see all months: ').lower()

    print('You have selected: ', [city], [month], [day])

    print('-'*50)
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
   	 	# use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

    	# filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Most frequent travel times: ')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: ', df['month'].value_counts().idxmax())


    # TO DO: display the most common day of week
    print('The most common day is: ', df['day_of_week'].value_counts().idxmax())


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour (24hour time) is: ', df['hour'].value_counts().idxmax())


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nMost popular stations and trips...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()
    print('Common start station: ', common_start_station[0])

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()
    print('Common end station: ', common_end_station[0])

    # TO DO: display most frequent combination of start station and end station trip
    common_trip_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Frequent trip combiantion: ', common_trip_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df['Trip Duration']) / 3600
    print('Total travel time: ', round(total_travel_time), 'hours')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', (round(mean_travel_time) /60), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    try:
            user_type = df['User Type'].value_counts()
            print('User Type: ', user_type)

    except KeyError:
        print('No user data available')


    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('User Gender: ', user_gender)

    except KeyError:
        print('No gender data availble')

    # TO DO: Display earliest, most recent, and most common year of birth (yob)
    try:
        earliest_yob = df['Birth Year'].min()
        print('Earliest birth year: ', int(earliest_yob))

    except KeyError:
        print('No earliest birth year data available')

    try:
        recent_yob = df['Birth Year'].max()
        print('Most recent birth year: ', int(recent_yob))

    except KeyError:
        print('No recent birth year data available')

    try:
        common_yob = df['Birth year'].value_counts().idxmax()
        print('Most common birth year: ', int(common_yob))

    except KeyError:
        print('No common birth year data available')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

#TO DO: See raw data
    view_data = input('Would you like to view 5 rows of individual trip data? Enter yes or no :')
    start_loc = 0

    while view_data not in ['no']:
        print(df.iloc[0+(start_loc):5+(start_loc)])
        start_loc += 5
        view_data = input('Do want to see 5 more rows of data? If not type no and program will end :').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart the program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
