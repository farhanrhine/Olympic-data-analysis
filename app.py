import streamlit as st
import pandas as pd
from helpers import *


# --- Simple Authentication ---
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "frhn":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()
# --- End Authentication ---

# ...existing code...





summer,winter = data_preprocessor()

# st.dataframe(summer)
# st.dataframe(winter)
st.write('Before')
st.write(summer.shape)
st.write(winter.shape)

summer,winter = duplicate_rows_remover(summer,winter)

summer.dropna(subset=['region'], inplace=True)
winter.dropna(subset=['region'], inplace=True)

st.write('After')
st.write(summer.shape)
st.write(winter.shape)

#create interface
st.sidebar.title('MENU')
season = st.sidebar.radio('Choose Season: ', ('summer','winter'))
options = st.sidebar.radio('options',('Medal-Tally','Country-Wise','Year-Wise','Year-Wise Progress'))

# 1. medal - tally
if season=='summer' and options=='Medal-Tally':
    st.subheader('SUMMER OLYMPICS MEDAL TALLY')
    medal_pivot_summer = medal_tally_calculator(summer)
    medal_pivot_summer= medal_pivot_summer.sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    st.dataframe(medal_pivot_summer, width=700)

elif season=='winter' and options=='Medal-Tally':
    st.subheader('WINTER OLYMPICS MEDAL TALLY')
    medal_pivot_winter = medal_tally_calculator(winter)
    medal_pivot_winter= medal_pivot_winter.sort_values(by=['Gold','Silver','Bronze'],ascending=False)
    st.dataframe(medal_pivot_winter, width=700)



## 2. country- wise tally
# for summer
elif season=='summer' and options=='Country-Wise':
    st.subheader('SUMMER COUNTRY-WISE SEARCH')
    medal_pivot_summer = medal_tally_calculator(summer)
    noc = st.selectbox("Select NOC: ", medal_pivot_summer.index.tolist())
    details = country_wise_search(noc,medal_pivot_summer)
    table = pd.DataFrame.from_dict(details, orient='index', columns=['value'])
    st.dataframe(table)

# for winter
elif season=='winter' and options=='Country-Wise':
    st.subheader('WINTER COUNTRY-WISE SEARCH')
    medal_pivot_winter = medal_tally_calculator(winter)
    noc = st.selectbox("Select NOC: ", medal_pivot_winter.index.tolist())
    details = country_wise_search(noc,medal_pivot_winter)
    table = pd.DataFrame.from_dict(details, orient='index', columns=['value'])
    st.dataframe(table)


### 3. year wise

# for summer
elif season =='summer' and options=='Year-Wise':
    st.subheader('SUMMER YEAR-WISE SEARCH')
    
    years = sorted(summer["Year"].unique())
    selected_year = st.selectbox('Select Year',years)

    countries = sorted(summer[summer['Year']==selected_year]['region'].unique())
    selected_country = st.selectbox('select country: ' ,countries)

    plot_medals(selected_year,selected_country,summer)

# for winter

elif season =='winter' and options=='Year-Wise':
    st.subheader('WINTER YEAR-WISE SEARCH')
    
    years = sorted(winter["Year"].unique())
    selected_year = st.selectbox('Select Year',years)

    countries = sorted(winter[winter['Year']==selected_year]['region'].unique())
    selected_country = st.selectbox('select country: ' ,countries)

    plot_medals(selected_year,selected_country,winter)

#### 4. year - wise country progress
# for summer 
elif season=="summer" and options=="Year-Wise Progress":
    st.subheader("OVERALL ANALYSIS OF A COUNTRY")

    countries = sorted(summer['region'].unique())
    selected_country = st.selectbox('Choose Country: ', countries)
    #ploting
    year_analysis(selected_country,summer)

# for winter
elif season=="winter" and options=="Year-Wise Progress":
    st.subheader("OVERALL ANALYSIS OF A COUNTRY")

    countries = sorted(winter['region'].unique())
    selected_country = st.selectbox('Choose Country: ', countries)
    #ploting
    year_analysis(selected_country,winter)
    
    
