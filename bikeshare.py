import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['chicago', 'new york', 'washington']

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s work on some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
       city = input('Which city do you want to explore Chicago, New York or Washington? \n> ').lower()
       if city in CITIES:
           break

    # get user input if they want to filter by momth or day
    filter = input("Would you like to filter the data by \'month\', \'day\', \'both\' or \'all\' for no filter?")
    if filter == "month":
    # get user input for month (all, january, february, ... , june)
        while True:
            month = input('Please enter the month which you will like to filter by. \n(e.g. january, february, march, april, may, june) \n> ').lower()
            if month in MONTHS:
                break
        day = 'all'
    # get user input for day of week (all, monday, tuesday, ... sunday)
    elif filter == "day":
        while True:
            day = input('Please enter the day which you will like to filter by. \n(e.g. monday, tuesday, wednesday, thursday, friday, saturday, sunday) \n> ').lower()
            if day in DAYS:
                break
        month = 'all'
    elif filter == "both":
        while True:
            month = input('Please enter the month which you will like to filter by. \n(e.g. january, february, march, april, may, june) \n> ').lower()
            if month in MONTHS:
                break
        while True:
            day = input('Please enter the day which you will like to filter by. \n(e.g. monday, tuesday, wednesday, thursday, friday, saturday, sunday) \n> ').lower()
            if day in DAYS:
                break
    else:
        month = 'all'
        day = 'all'

    print('-'*40)
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
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is :", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("The most common day of week is :", most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("The most common start hour is :", most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is :", most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is :", most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_start_end_station = df[['Start Station', 'End Station']].mode().loc[0]
    print("The most commonly used start station and end station : {}, {}"\
            .format(most_common_start_end_station[0], most_common_start_end_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is:", total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is:", mean_travel_time)

    # display max travel time
    max_travel_time = df['Trip Duration'].max()
    print("The max travel time is:", max_travel_time)

    # display the total trip duration for each user type
    print("Travel time for each user type:\n")
    group_by_user_trip = df.groupby(['User Type']).sum()['Trip Duration']
    for index, user_trip in enumerate(group_by_user_trip):
        print("  {}: {}".format(group_by_user_trip.index[index], user_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:\n")
    for index, user_count in enumerate(user_types):
        print("  {}: {}".format(user_types.index[index], user_count))

    print()

    # Display counts of gender
    if 'Gender' in df.columns:
        print("Counts of gender:\n")
        gender_counts = df['Gender'].value_counts()
        for index,gender_count   in enumerate(gender_counts):
            print("  {}: {}".format(gender_counts.index[index], gender_count))

        print()

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        #birth_year = df['Birth Year']
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print("The most common year of birth is:", most_common_year_of_birth)

        most_recent_birth_year = df['Birth Year'].max()
        print("The most recent year of birth is:", most_recent_birth_year)

        earliest_birth_year = df['Birth Year'].min()
        print("The earliest year of birth is:", earliest_birth_year)

        print()


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    # Get input and display details of each trip in steps of 5
    view_data = input("Would you like to view 5 rows of individual trip data? Please enter yes or no?").lower()
    start_loc = 0
    while (view_data == "yes"):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display == "no":
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
