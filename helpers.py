import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

athlete = pd.read_csv('olympics dataset/athlete_events.csv')
region = pd.read_csv('olympics dataset/noc_regions.csv')

def data_preprocessor():
    global athlete,region
    df = pd.merge(athlete,region, on='NOC')
    df.drop_duplicates(inplace=True)
    df['Medal'].fillna('No_Medal', inplace=True)
    summer =  df[df['Season'] == 'Summer']
    winter = df[df['Season'] ==  'Winter']
    return summer, winter

def duplicate_rows_remover(df1,df2):
    df1 = df1.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event'])
    df2 = df2.drop_duplicates(subset=['Team','NOC','Games','Year','Season','City','Sport','Event'])
    return df1, df2

def medal_tally_calculator(df):
    medal_count= df.groupby(['NOC','Medal']).size().reset_index(name='count') # because geneal term used kiya hai so, yahi both season kai liye used karu gaa
    medal_pivot = medal_count.pivot(index='NOC', columns='Medal', values='count').fillna(0)
    medal_pivot = medal_pivot.astype(int)

    if "NO_Medal" in medal_pivot.columns:
        medal_pivot.drop(columns="No_Medal", inplace=True)

    medal_pivot['Total_medal']= medal_pivot[['Gold','Silver','Bronze']].sum(axis=1)
    return medal_pivot


# 2. country-wise tally
def country_wise_search(noc,pivot_table): # here i only change function name
    if noc in pivot_table.index:
        details={
            'Gold': pivot_table.loc[noc,'Gold'], # left hand side labalhai main kuch bhi likh sakta hu, just eg. insted of gold, i can write go but right hand side is a column name from data set so its must be correct.
            'Silver': pivot_table.loc[noc,'Silver'],
            'Bronze': pivot_table.loc[noc,'Bronze'],
            'Total_medal': int(pivot_table.loc[noc,'Total_medal'])
        }
        # Convert all values to Python int in one line
        details = {k: int(v) for k, v in details.items()}
        return details
    else:
        print('no NOC exist')



# year wise tally

def plot_medals(year,country, df):

    medal_count  = df.groupby(['Year','region','Medal']).size().unstack(fill_value=0)
    medal_count = medal_count.reset_index()
    medal_count['Total_Medal']= medal_count['Gold']+ medal_count['Silver']+medal_count['Bronze']








    filter_df = medal_count[(medal_count['Year']==year)  & (medal_count['region']==country)]
    gold = filter_df['Gold'].values[0]
    silver = filter_df['Silver'].values[0]
    bronze = filter_df['Bronze'].values[0]
    total_medal = filter_df['Total_Medal'].values[0]
# graph
    fig,ax = plt.subplots(figsize=(10,10))
    medals=['Gold','Silver','Bronze','Total_Medals']
    counts = [gold,silver,bronze,total_medal]
    ax.bar(medals,counts,color=['gold','silver','brown','green'])
    st.pyplot(fig)



#### 4. Year- size country Progress
def year_analysis(country,df):

    medal_count  = df.groupby(['Year','region','Medal']).size().unstack(fill_value=0)
    medal_count = medal_count.reset_index()
    medal_count['Total_Medal']= medal_count['Gold']+ medal_count['Silver']+medal_count['Bronze']

 
    filtered_df = medal_count[medal_count["region"]==country]
    fig,ax = plt.subplots()
    ax.plot(filtered_df["Year"],filtered_df['Gold'],color='gold',label='GOLD', marker='o',linestyle='-')
    ax.plot(filtered_df['Year'],filtered_df['Silver'],color='silver',label='SILVER', marker='o',linestyle='-')
    ax.plot(filtered_df['Year'],filtered_df['Bronze'],color='brown',label='BRONZE', marker='o',linestyle='-')
    ax.plot(filtered_df['Year'],filtered_df['Total_Medal'],color='green',label='TOTAL MEDALS', marker='o',linestyle='-')
    ax.legend()
    st.pyplot(fig)





