import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday','tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    global city
    city = input('Please provide a city:')
    city = city.lower()
    while city not in (CITY_DATA):
        city = input('try: chicago, new york city, washington: ')
        city = city.lower()
   
    # TO DO: get user input for month (all, january, february, ... , june)
    
    month = input('Please provide a month:')
    month = month.lower()
    while month not in (months) and month != 'all':
        month = input('try: all, january, february, ... , june: ')
        month = month.lower()
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    day = input('Please provide a day:')
    day = day.lower()
    while day not in (days) and day !='all':
                   
        day = input('try: all, monday, tuesday, ..., sunday: ')
        day = day.lower()
    
    print('-'*40)
    return (city, month, day)
 


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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    
    # filtering only works if a month was selected. in case of all, these 2 steps will be skipped
    if month in months:
       month = months.index(month) + 1
       df = df[df['month'] == month]
    
    if day in days:
       day = days.index(day) + 1
       df = df[df['day'] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mcmonth = df['month'].mode()[0]
    print('Most common month is: ', months[mcmonth - 1].capitalize())
    
    # TO DO: display the most common day of week
    mcday= df['day'].mode()[0]
    print('Most common day is: ', days[mcday - 1].capitalize())
    
    # TO DO: display the most common start hour
    # create hour in df
    df['hour'] = df['Start Time'].dt.hour
    mchour = df['day'].mode()[0]
    print('Most common hour is: ', mchour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mcstation = df['Start Station'].mode()[0]
    print('Most common start station is: ', mcstation)


    # TO DO: display most commonly used end station
    mcestation = df['End Station'].mode()[0]
    print('Most common end station is: ', mcestation)

    # TO DO: display most frequent combination of start station and end station trip
    df['startend'] = df['Start Station'] + ' - ' + df['End Station']
    mccomb = df['startend'].mode()[0]
    print('Most frequent combination of start station and end station is: ', mccomb)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

 

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    #convert to number first
    
    totaltime = df['Trip Duration'].sum()
    # divide by 3600 to get value in hours
    totaltime = totaltime/3600
    print('Total Trip Duration is: ', totaltime, ' hours.')
    
    # TO DO: display mean travel time
    meantime = df['Trip Duration'].mean()
    
    #this time get value in minutes - makes more sense for a smaller expected value
    meantime = meantime/60
    print('Mean trip time is: ', meantime, ' minutes.')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())
    
    if city == 'washington':
        print('\nSorry, Gender and year of birth data is not available for Washington\n')
    else:
        # TO DO: Display counts of gender
        print(df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        earliest = earliest.astype(int)
        
        print('Earliest year of birth is: ', earliest)

        #most recent : first get by .loc, strip to get value only, then convert to integer
        last_hire = df.loc[df['Start Time'] == df['Start Time'].max(), 'Birth Year'].values[0]
        last_hire = last_hire.astype(int)
        print('Most recent customer\'s date of birth is: ', last_hire)
        #most common
        mc_dob = df['Birth Year'].mode()[0]
        mc_dob = mc_dob.astype(int)
        print('Most common year of birth is: ', mc_dob)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    
    # check if user wants to see raw data
    
    if input("\nWould you like to see raw data? (yes/no) \n") == 'yes':
        print(df.head())
        #if they want more, create a counter i and then use iloc to slice the correct rows. increment i by 5 at the end
        i = 5
        while input("\nWould you like to see more?") == 'yes':
            print(df.iloc[i:i+5])
            i += 5
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
user_stats(load_data('chicago','all','all'))  