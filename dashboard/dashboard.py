import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import altair as alt

day_df = pd.read_csv("./dashboard/main_day_data.csv")
hour_df = pd.read_csv("./dashboard/main_hour_data.csv")

# mengubah kembali data yang dinormalisasi
not_normalized_day_df = day_df.drop('instant', axis=1)
not_normalized_day_df['temperature'] = not_normalized_day_df['temperature'] * 41
not_normalized_day_df['atemperature'] = not_normalized_day_df['atemperature'] * 50
not_normalized_day_df['humidity'] = not_normalized_day_df['humidity'] * 100
not_normalized_day_df['windspeed'] = not_normalized_day_df['windspeed'] * 67

# mengubah kembali data yang dinormalisasi
not_normalized_hour_df = hour_df.drop('instant', axis=1)
not_normalized_hour_df['temperature'] = not_normalized_hour_df['temperature'] * 41
not_normalized_hour_df['atemperature'] = not_normalized_hour_df['atemperature'] * 50
not_normalized_hour_df['humidity'] = not_normalized_hour_df['humidity'] * 100
not_normalized_hour_df['windspeed'] = not_normalized_hour_df['windspeed'] * 67

with st.sidebar:
  st.header("📊 Graph Filter")

  # mengambil tanggal paling besar dan paling kecil
  min_date = day_df["date"].min()
  max_date = day_df["date"].max()

  try:

    start_date = st.date_input(label='Start Date', min_value=min_date, max_value=max_date, value=min_date)
    
    if not start_date:
      st.warning("Please choose the correct date to show graphs")
      start_date = min_date
    
    end_date = st.date_input(label='End Date', min_value=min_date, max_value=max_date, value=max_date)

    if not end_date:
      st.warning("Please choose the correct date to show graphs")
      end_date = max_date
    
    if start_date > end_date: start_date, end_date = end_date, start_date

  except Exception as err:
    st.error(f"Sorry, it looks like our sistem having problem reading date: {err}")

  # filter musim
  all_season = pd.concat([day_df['season'], hour_df['season']]).unique() # mengambil semua nilai unik dari kolom musim di kedua dataframe
  selected_season = st.selectbox(
    "Season",
    ["All Season"] + list(all_season), # menggunakan nilai unik tersebut
  )

  all_weather = pd.concat([day_df['weather'], hour_df['weather']]).unique() # mengambil semua nilai unik dari kolom musim di kedua dataframe
  selected_weather = st.selectbox(
    "Weather",
    ["All Weather"] + list(all_weather), # menggunakan nilai unik tersebut
  )

# dataframe dengan rentang waktu yang diinginkan pengguna
filter_day_df = day_df[(day_df["date"] >= str(start_date)) & 
            (day_df["date"] <= str(end_date))]
    
filter_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
            (hour_df["date"] <= str(end_date))]

# dataframe dengan season yang diinginkan pengguna
if selected_season and selected_season != "All Season":
  filter_day_df = filter_day_df[filter_day_df['season'] == selected_season]
  filter_hour_df = filter_hour_df[filter_hour_df['season'] == selected_season]

# dataframe dengan season yang diinginkan pengguna
if selected_weather and selected_weather != "All Weather":
  filter_day_df = filter_day_df[filter_day_df['weather'] == selected_weather]
  filter_hour_df = filter_hour_df[filter_hour_df['weather'] == selected_weather]

# mulai definisikan main content
with st.container():
  st.title(":orange[Bike Sharing Statistic]")
  
  day, hour = st.tabs(["Per Day", "Per Hour"])

  with day:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("Renter", f"{filter_day_df['total'].sum():,}")

    with col2:
      st.metric("Registered", f"{filter_day_df['registered'].sum():,}")
    
    with col3:
      st.metric("Casual", f"{filter_day_df['casual'].sum():,}")

    with col4:
      st.metric("Data", f"{filter_day_df.shape[0]:,}")
    
    st.write(not_normalized_day_df)

    st.subheader("2011 versus 2012")
    day_monthly_rentals = filter_day_df.groupby(['year', 'month'])['total'].mean().reset_index()
    day_monthly_pivot_df = day_monthly_rentals.pivot(index='month', columns='year', values='total')
    st.line_chart(day_monthly_pivot_df)

    st.subheader("Correlation Between Feature")
    day_corr = filter_day_df[['temperature', 'atemperature', 'humidity', 'windspeed']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(day_corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
    st.pyplot(fig)

    st.subheader("Renters According to Seasons")
    day_mean_rentals_per_season = filter_day_df.groupby('season')['total'].mean().reset_index()
    day_mean_rentals_per_season.set_index('season', inplace=True)
    st.bar_chart(day_mean_rentals_per_season)

    st.subheader("Renters According to Weather Conditions")
    day_mean_rentals_per_weather = filter_day_df.groupby('weather')['total'].mean().reset_index()
    day_mean_rentals_per_weather.set_index('weather', inplace=True)
    st.bar_chart(day_mean_rentals_per_weather)

    st.subheader("Renters Per Month")
    day_mean_rentals_per_month = filter_day_df.groupby('month')['total'].mean().reset_index()
    day_mean_rentals_per_month.set_index('month', inplace=True)
    st.bar_chart(day_mean_rentals_per_month)

    st.subheader("Renters Per Day")
    day_mean_rentals_per_day_weather = filter_day_df.groupby(['weekday', 'weather'])['total'].mean().reset_index()
    day_mean_rentals_per_day_weather = day_mean_rentals_per_day_weather.groupby(['weekday', 'weather'])['total'].mean().unstack()
    st.bar_chart(day_mean_rentals_per_day_weather)

    with hour:
      col1, col2, col3, col4 = st.columns(4)

      with col1:
        st.metric("Renter", f"{filter_hour_df['total'].sum():,}")

      with col2:
        st.metric("Registered", f"{filter_hour_df['registered'].sum():,}")
      
      with col3:
        st.metric("Casual", f"{filter_hour_df['casual'].sum():,}")

      with col4:
        st.metric("Data", f"{filter_hour_df.shape[0]:,}")
      
      st.write(not_normalized_hour_df)

      st.subheader("2011 versus 2012")
      hour_monthly_rentals = filter_hour_df.groupby(['year', 'month'])['total'].mean().reset_index()
      pivot_df = hour_monthly_rentals.pivot(index='month', columns='year', values='total')
      st.line_chart(pivot_df)

      st.subheader("Correlation Between Feature")
      hour_corr = filter_hour_df[['temperature', 'atemperature', 'humidity', 'windspeed']].corr()
      fig, ax = plt.subplots(figsize=(8, 6))
      sns.heatmap(hour_corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
      st.pyplot(fig)
      
      st.subheader("Renters According to Seasons")
      hour_mean_rentals_per_weather = filter_hour_df.groupby('season')['total'].mean().reset_index()
      hour_mean_rentals_per_weather.set_index('season', inplace=True)
      st.bar_chart(hour_mean_rentals_per_weather)

      st.subheader("Renters Per Month")
      hour_mean_rentals_per_month = filter_hour_df.groupby('month')['total'].mean().reset_index()
      hour_mean_rentals_per_month.set_index('month', inplace=True)
      st.bar_chart(hour_mean_rentals_per_month)

      st.subheader("Renters According to Weather Conditions")
      hour_mean_rentals_per_season = filter_hour_df.groupby('weather')['total'].mean().reset_index()
      hour_mean_rentals_per_season.set_index('weather', inplace=True)
      st.bar_chart(hour_mean_rentals_per_season)

      st.subheader("Renters Per Hour")
      hour_mean_rentals_per_hour_weather = filter_hour_df.groupby(['hour', 'weather'])['total'].mean().reset_index()
      hour_mean_rentals_per_hour_weather = hour_mean_rentals_per_hour_weather.groupby(['hour', 'weather'])['total'].mean().unstack()
      st.bar_chart(hour_mean_rentals_per_hour_weather)

  st.caption("Copyright © 2025 Arya Ulya Krisna. All rights reserved.")

