import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

day_df = pd.read_csv("https://raw.githubusercontent.com/SandiYunus/submision_analisis_data/main/dashboard/day.csv")
day_df.head()

drop_col = ['dteday', 'instant', 'yr', 'mnth', 'hr', 'weathersit', 'temp', 'atemp', 'weekday']

for i in day_df.columns:
  if i in drop_col:
    day_df.drop(labels=i, axis=1, inplace=True)
    
day_df.rename(columns={
    'hum': 'humidity',
    'cnt': 'count'
}, inplace=True)

day_df['holiday'] = day_df.holiday.astype('category')
day_df['workingday'] = day_df.workingday.astype('category')

def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

def create_humidity_rent_df(df):
    humidity_rent_df = df.groupby(by='humidity').agg({
        'count': 'sum'
    }).reset_index()
    return humidity_rent_df

def create_windspeed_rent_df(df):
    windspeed_rent_df = df.groupby(by='windspeed').agg({
        'count': 'sum'
    }).reset_index()
    return windspeed_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

main_df = day_df

holiday_rent_df = create_holiday_rent_df(main_df)
workingday_rent_df  = create_workingday_rent_df(main_df)
humidity_rent_df = create_humidity_rent_df(main_df)
windspeed_rent_df = create_windspeed_rent_df(main_df)
season_rent_df = create_season_rent_df(day_df)

st.set_page_config(page_title="Bike Rental Dashboard", layout="wide")

st.markdown("<h1 style='text-align: center;'>Bike Rental Dashboard</h1>", unsafe_allow_html=True)

st.subheader('Workingday, and Holiday Rentals')

col1, col2 = st.columns(2)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 10), gridspec_kw={'wspace': 0.4})
sns.barplot(
    x='holiday',
    y='count',
    data=day_df,
    ax=axes[0],
    palette='pastel'
)
axes[0].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Libur')
axes[0].set_xlabel('Hari Libur')
axes[0].set_ylabel('Jumlah Pengguna Sepeda')

sns.barplot(
    x='workingday',
    y='count',
    data=day_df,
    ax=axes[1],
    palette='Set2'
)
axes[1].set_title('Jumlah Pengguna Sepeda berdasarkan Hari Kerja')
axes[1].set_xlabel('Hari Kerja')
axes[1].set_ylabel('Jumlah Pengguna Sepeda')

plt.tight_layout()

col1.pyplot(fig)

st.subheader('Seasonal Rentals')

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='lightblue'
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='lightcoral'
)

plt.xlabel('Season')
plt.ylabel('Total Rentals')
plt.title('Seasonal Bike Rental Analysis')
plt.legend()
st.pyplot(fig)

col3, col4 = st.columns(2)

col3.subheader('Humidity Rentals')
col3.line_chart(humidity_rent_df.set_index('humidity'))

col4.subheader('Windspeed Rentals')
col4.line_chart(windspeed_rent_df.set_index('windspeed'))

