#Import Libraries
import pandas as pd
import datetime
import os


#Get Current time to be used to find run time at end of program
startTime = datetime.datetime.now()

#Import Premier League Results
prem_results_location = 'D:\\Football_Results_Downloads\\Historic_League_Results_E0_1993_2020.csv'
prem_results = pd.read_csv(prem_results_location,parse_dates=['Date'])

#Get max date array
max_date = [prem_results.Date.max()]
#Create dataframe
max_date = pd.DataFrame(max_date,columns = ['Date'])
#Convert to datetype
max_date = pd.to_datetime(max_date['Date'], format='%Y-%m-%d') 

#Create folder to download data to
directory ='D:\\Football_Results_Downloads\\'
if not os.path.exists(directory):
    os.makedirs(directory)
    
#Create dataframe to store results
combined_data = pd.DataFrame()

#E0 is premiership ,E1 is championship, E2 League 1, E3 League 2, EC is conference
division = 'E0'
#Enter start year of current_season
current_season_start_year = 2019

#Convert years entered above to datetimes
year_start = datetime.date(current_season_start_year, 1,1)
year_end = datetime.date(current_season_start_year+1, 1,1)
#Create String to be used in football_data_url below
season_string = year_start.strftime('%y') + year_end.strftime('%y')
football_data_url = 'https://www.football-data.co.uk/mmz4281/'+season_string+'/'+division+'.csv'
  
#Create list of columns, as some files have extra columns in rows that throw error
cols = (pd.read_csv(football_data_url, nrows=1)).columns.tolist()
#There are special characters in the file, so using encoding='latin1' below works
data = pd.read_csv(football_data_url, parse_dates=['Date'], dayfirst=True, usecols = cols,encoding='latin1')
#Create dataframes with 1 column to show season, season start year, season end year
season_df = pd.DataFrame([season_string]*len(data),columns = ['Season'])
season_start_year_df = pd.DataFrame([current_season_start_year]*len(data),columns = ['season_start_year'])
season_end_year_df = pd.DataFrame([current_season_start_year+1]*len(data),columns = ['season_end_year'])
#Concatenate these dataframes with data dataframe, so that there are columns to identify the season
data = pd.concat([data,season_df, season_start_year_df, season_end_year_df], axis=1)
#Filter data for greater than max date
data_latest = data[data.Date > max_date.iloc[0]]

#Concatenate data dataframe with combined_data dataframe to store all data
combined_data = pd.concat([combined_data, data_latest], axis=0, sort = False).reset_index(drop = True)


#Create copy of prem results dataframe
prem_results_copy = prem_results.copy()
#Create copy of original dataframe
copy_data = combined_data.copy()
#Concatenate prem data copy with copy data
prem_results_copy = pd.concat([prem_results_copy, copy_data], axis=0, sort = False).reset_index(drop = True)



#Find empty columns
empty_cols = [col for col in prem_results_copy.columns if prem_results_copy[col].isnull().all()]
#Drop empty columns
prem_results_copy.drop(empty_cols,
                       axis=1,
                       inplace=True)
#Drop unnamed column
prem_results_copy.drop(['Unnamed: 0'],axis=1,inplace=True)

#Remove rows where date is empty
prem_results_copy = prem_results_copy[pd.notnull(prem_results_copy['Date'])]
#Reset Index
prem_results_copy = prem_results_copy.reset_index(drop=True)


#Get first season start year
min_season = prem_results_copy['season_start_year'].min()
#Get last season end year
max_season = prem_results_copy['season_end_year'].max()  
#Get max file date
max_filedate = prem_results_copy['Date'].max().strftime('%Y-%m-%d')  
#Filename
file_name = 'Historic_League_Results_'+division+'_'+str(min_season)+'_'+str(max_season)+'_'+str(max_filedate)+'.csv'


#Save file to directory as csv
prem_results_copy.to_csv(directory+file_name)

#Get run time
run_time = datetime.datetime.now() - startTime
print(run_time)
