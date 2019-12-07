#Import Libraries
import pandas as pd
import datetime
import os

#Create folder to download data to
directory ='D:\\Football_Results_Downloads\\'
if not os.path.exists(directory):
    os.makedirs(directory)
    
#Create dataframe to store results
combined_data = pd.DataFrame()

#E0 is premiership ,E1 is championship, E2 League 1, E3 League 2, EC is conference
division = 'E0'
#Enter start year of first season to download (first season is 1993)
first_season_start_year = 1993
#Enter start year of last season to download
last_season_start_year = 2019

while first_season_start_year <= last_season_start_year:
    
    #Convert years entered above to datetimes
    year_start = datetime.date(first_season_start_year, 1,1)
    year_end = datetime.date(first_season_start_year+1, 1,1)
    #Create String to be used in football_data_url below
    season_string = year_start.strftime('%y') + year_end.strftime('%y')
    football_data_url = 'https://www.football-data.co.uk/mmz4281/'+season_string+'/'+division+'.csv'
  
    #Create list of columns, as some files have extra columns in rows that throw error
    cols = (pd.read_csv(football_data_url, nrows=1)).columns.tolist()
    #There are special characters in the file, so using encoding='latin1' below works
    data = pd.read_csv(football_data_url, parse_dates=['Date'], dayfirst=True, usecols = cols,encoding='latin1')
    #Create dataframes with 1 column to show season, season start year, season end year
    season_df = pd.DataFrame([season_string]*len(data),columns = ['Season'])
    season_start_year_df = pd.DataFrame([first_season_start_year]*len(data),columns = ['season_start_year'])
    season_end_year_df = pd.DataFrame([first_season_start_year+1]*len(data),columns = ['season_end_year'])
    #Concatenate these dataframes with data dataframe, so that there are columns to identify the season
    data = pd.concat([data,season_df, season_start_year_df, season_end_year_df], axis=1)
    #Concatenate data dataframe with combined_data dataframe to store all data
    combined_data = pd.concat([combined_data, data], axis=0, sort = False).reset_index(drop = True)
    #Increment by a year so that while loop starts again until no data left to grab
    first_season_start_year = first_season_start_year + 1

#Create copy of original dataframe
copy_data = combined_data.copy()  
#Find empty columns
empty_cols = [col for col in copy_data.columns if copy_data[col].isnull().all()]
#Drop empty columns
copy_data.drop(empty_cols,
                       axis=1,
                       inplace=True)
#Remove rows where date is empty
copy_data = copy_data[pd.notnull(copy_data['Date'])]
#Reset Index
copy_data = copy_data.reset_index(drop=True)
#Get first season start year
min_season = copy_data['season_start_year'].min()
#Get last season end year
max_season = copy_data['season_end_year'].max()     
#Filename
file_name = 'Historic_League_Results_'+division+'_'+str(min_season)+'_'+str(max_season)+'.csv'
#Save file to directory as csv
copy_data.to_csv(directory+file_name)
