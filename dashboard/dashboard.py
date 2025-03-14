import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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
filtered_day_df = day_df[(day_df["date"] >= str(start_date)) & 
            (day_df["date"] <= str(end_date))]
    
filtered_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
            (hour_df["date"] <= str(end_date))]

# dataframe dengan season yang diinginkan pengguna
if selected_season and selected_season != "All Season":
  filtered_day_df = filtered_day_df[filtered_day_df['season'] == selected_season]
  filtered_hour_df = filtered_hour_df[filtered_hour_df['season'] == selected_season]

# dataframe dengan season yang diinginkan pengguna
if selected_weather and selected_weather != "All Weather":
  filtered_day_df = filtered_day_df[filtered_day_df['weather'] == selected_weather]
  filtered_hour_df = filtered_hour_df[filtered_hour_df['weather'] == selected_weather]

# mulai definisikan main content
with st.container():
  st.title(":orange[Bike Sharing Statistic]")
  
  day, hour = st.tabs(["Per Day", "Per Hour"])

  with day:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
      st.metric("Renter", f"{filtered_day_df['total'].sum():,}")

    with col2:
      st.metric("Registered", f"{filtered_day_df['registered'].sum():,}")
    
    with col3:
      st.metric("Casual", f"{filtered_day_df['casual'].sum():,}")

    with col4:
      st.metric("Data", f"{filtered_day_df.shape[0]:,}")
    
    st.write(not_normalized_day_df)

    with st.expander("About Dataset"):
      st.markdown("- Dataset menyajikan data penyewaan sepeda per hari, mencakup informasi seperti musim, cuaca, suhu, dan jumlah penyewa. Analisis dari dataset ini mengungkap pola musiman serta dampak faktor eksternal terhadap tren penyewaan.")
    
    st.divider()

    month_in_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
    weekday_in_order = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] 
    filtered_day_df['month'] = pd.Categorical(filtered_day_df['month'], categories=month_in_order, ordered=True) # Memperbaiki kesalahan, mengurutkan bulan sesuai dengan urutan
    filtered_day_df['weekday'] = pd.Categorical(filtered_day_df['weekday'], categories=weekday_in_order, ordered=True) 
    filtered_hour_df['month'] = pd.Categorical(filtered_hour_df['month'], categories=month_in_order, ordered=True) # Memperbaiki kesalahan, mengurutkan hari sesuai dengan urutan
    filtered_hour_df['weekday'] = pd.Categorical(filtered_hour_df['weekday'], categories=weekday_in_order, ordered=True)

    st.subheader("2011 VS 2012")
    day_monthly_rentals = filtered_day_df.groupby(['year', 'month'])['total'].sum().reset_index()
    day_monthly_pivot_df = day_monthly_rentals.pivot(index='month', columns='year', values='total')
    st.line_chart(day_monthly_pivot_df)

    with st.expander("Conclusion"):
      st.markdown("""
                  - Perbedaan jumlah penyewa sepeda pada tahun 2011 dan 2012 terlihat cukup signifikan dengan tahun 2012 memiliki penyewa sepeda yang lebih banyak di masing - masing bulannya dibanding tahun 2011. 
                  - Pada tahun 2011, jumlah penyewa mengalami peningkatan signifikan dari Januari hingga Mei, mencapai puncaknya di bulan Juni dengan sekitar 140 ribu penyewa, kemudian mengalami sedikit penurunan dan tetap stabil hingga Oktober sebelum menurun di akhir tahun. 
                  - Sementara itu, pada tahun 2012, jumlah penyewa secara keseluruhan lebih tinggi dibandingkan tahun sebelumnya.
                  """)
      
    with st.expander("Recommendations and Suggestions"):
      st.markdown("""
                  - Tingkatkan ketersediaan di bulan dengan permintaan tinggi. 
                  - Peningkatan infrastruktur, seperti menambah stasiun penyewaan dan layanan berbasis aplikasi, dapat meningkatkan aksesibilitas.
                  """)
    
    st.divider()

    st.markdown("### Weekday <span style='font-size:16px;'>(False)</span> VS Holiday <span style='font-size:16px;'>(True)</span> ", unsafe_allow_html=True)
    day_sum_rentals_per_month = filtered_day_df.groupby(['season', 'holiday'])['total'].sum().reset_index()
    # day_sum_rentals_per_month = day_sum_rentals_per_month['holiday'].map({True: 'Holiday', False: 'Weekday'}) # keadaaan bar menjadi terbalik jika ditambahkan
    day_sum_rentals_per_day_month = day_sum_rentals_per_month.groupby(['season', 'holiday'])['total'].sum().unstack()

    st.bar_chart(day_sum_rentals_per_day_month)

    with st.expander("Conclusion"):
      st.markdown("""
                  - Terdapat perbedaan pengguna sepeda di hari libur dan hari kerja tiap musimnya, jumlahnya sangat signifikan. 
                  - Grafik menunjukkan bahwa jumlah penyewaan sepeda pada hari kerja jauh lebih tinggi dibandingkan hari libur di setiap musim. 
                  - Musim gugur (fall) mencatat penyewaan tertinggi pada hari kerja, sementara musim panas (summer) dan musim dingin (winter) juga menunjukkan angka yang tinggi, meskipun sedikit lebih rendah. 
                  - Sebaliknya, jumlah penyewaan pada hari libur tetap rendah di semua musim, dengan perbedaan yang sangat mencolok dibandingkan hari kerja. 
                  """)
    
    with st.expander("Recommendations and Suggestions"):
      st.markdown("- Tingkatkan ketersediaan sepeda di hari kerja dan terapkan promo atau rute wisata khusus untuk meningkatkan penyewaan di hari libur.")

    st.divider()

    st.subheader("Correlation Between Feature")
    day_corr = filtered_day_df[['temperature', 'atemperature', 'humidity', 'windspeed']].corr()
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(day_corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
    st.pyplot(fig)

    with st.expander("Conclusion"):
      st.markdown("""
                  - Jumlah penyewaan sepeda setiap harinya besar dipengaruhi oleh temperatur yang dirasakan oleh penyewa seperti yang terlihat pada heatmap korelasi antar fitur. 
                  - Berdasarkan heatmap korelasi antar fitur, terdapat hubungan yang sangat kuat antara temperature dan atempature dengan nilai korelasi sebesar 0.99, yang menunjukkan bahwa kedua variabel ini hampir identik. 
                  - Korelasi antara humidity dan faktor lainnya relatif rendah, dengan nilai tertinggi sebesar 0.14 terhadap atempature. 
                  - Sementara itu, windspeed memiliki korelasi negatif dengan fitur lainnya, terutama dengan humidity -0.24 dan temperature -0.16.
                  """)
    with st.expander("Recommendations & Suggestions"):
      st.markdown("""
                  - Tingkatkan ketersedian sepeda di musim dengan permintaan tinggi (gugur & panas).
                  - Lakukan promosi di musim dengan permintaan rendah (semi & dingin). 
                  - Lakukan penelitian lebih lanjut untuk mencari daerah dengan penyewa sepeda terbanyak.
                  """)
      
    st.divider()

    with hour:
      col1, col2, col3, col4 = st.columns(4)

      with col1:
        st.metric("Renter", f"{filtered_hour_df['total'].sum():,}")

      with col2:
        st.metric("Registered", f"{filtered_hour_df['registered'].sum():,}")
      
      with col3:
        st.metric("Casual", f"{filtered_hour_df['casual'].sum():,}")

      with col4:
        st.metric("Data", f"{filtered_hour_df.shape[0]:,}")
      
      st.write(not_normalized_hour_df)

      with st.expander("About Dataset"):
        st.markdown("- Dataset ini menyajikan data penyewaan per jam, yang memberikan wawasan lebih rinci tentang pola penggunaan sepeda sepanjang hari. Dari hasil analisis, terlihat jam-jam tersibuk serta bagaimana kondisi cuaca memengaruhi jumlah penyewa dalam skala waktu yang lebih kecil.")
      
      st.divider()

      st.subheader("2011 versus 2012")
      hour_monthly_rentals = filtered_hour_df.groupby(['year', 'month'])['total'].sum().reset_index()
      pivot_df = hour_monthly_rentals.pivot(index='month', columns='year', values='total')
      st.line_chart(pivot_df)

      with st.expander("Conclusion"):
        st.markdown("""
                    - Perbedaan jumlah penyewa sepeda pada tahun 2011 dan 2012 terlihat cukup signifikan dengan tahun 2012 memiliki penyewa sepeda yang lebih banyak di masing - masing bulannya dibanding tahun 2011. 
                    - Pada tahun 2011, jumlah penyewa mengalami peningkatan signifikan dari Januari hingga Mei, mencapai puncaknya di bulan Juni dengan sekitar 140 ribu penyewa, kemudian mengalami sedikit penurunan dan tetap stabil hingga Oktober sebelum menurun di akhir tahun. 
                    - Sementara itu, pada tahun 2012, jumlah penyewa secara keseluruhan lebih tinggi dibandingkan tahun sebelumnya.
                    """)
    
      with st.expander("Recommendations and Suggestions"):
        st.markdown("""
                    - Tingkatkan ketersediaan di bulan dengan permintaan tinggi. 
                    - Peningkatan infrastruktur, seperti menambah stasiun penyewaan dan layanan berbasis aplikasi, dapat meningkatkan aksesibilitas.
                    """)

      st.divider()

      st.markdown("### Weekday <span style='font-size:16px;'>(False)</span> VS Holiday <span style='font-size:16px;'>(True)</span> ", unsafe_allow_html=True)
      sum_rentals_per_month = filtered_hour_df.groupby(['season', 'holiday'])['total'].sum().reset_index()
      # sum_rentals_per_month = sum_rentals_per_month['holiday'].map({True: 'Holiday', False: 'Weekday'}) # keadaaan bar menjadi terbalik jika ditambahkan
      hour_mean_rentals_per_day_month = sum_rentals_per_month.groupby(['season', 'holiday'])['total'].sum().unstack()
  
      st.bar_chart(hour_mean_rentals_per_day_month)
  
      with st.expander("Conclusion"):
        st.markdown("""
                    - Terdapat perbedaan pengguna sepeda di hari libur dan hari kerja tiap musimnya, jumlahnya sangat signifikan. 
                    - Grafik menunjukkan bahwa jumlah penyewaan sepeda pada hari kerja jauh lebih tinggi dibandingkan hari libur di setiap musim. 
                    - Musim gugur (fall) mencatat penyewaan tertinggi pada hari kerja, sementara musim panas (summer) dan musim dingin (winter) juga menunjukkan angka yang tinggi, meskipun sedikit lebih rendah. 
                    - Sebaliknya, jumlah penyewaan pada hari libur tetap rendah di semua musim, dengan perbedaan yang sangat mencolok dibandingkan hari kerja. 
                    """)
      
      with st.expander("Recommendations and Suggestions"):
        st.markdown("- Tingkatkan ketersediaan sepeda di hari kerja dan terapkan promo atau rute wisata khusus untuk meningkatkan penyewaan di hari libur.")
      
      st.divider()

      st.subheader("Correlation Between Feature")
      hour_corr = filtered_hour_df[['temperature', 'atemperature', 'humidity', 'windspeed']].corr()
      fig, ax = plt.subplots(figsize=(8, 6))
      sns.heatmap(hour_corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
      st.pyplot(fig)

      with st.expander("Conclusion"):
        st.markdown("""
                    - Jumlah penyewaan sepeda setiap harinya besar dipengaruhi oleh temperatur yang dirasakan oleh penyewa seperti yang terlihat pada heatmap korelasi antar fitur. 
                    - Berdasarkan heatmap korelasi antar fitur, terdapat hubungan yang sangat kuat antara temperature dan atempature dengan nilai korelasi sebesar 0.99, yang menunjukkan bahwa kedua variabel ini hampir identik. 
                    - Korelasi antara humidity dan faktor lainnya relatif rendah, dengan nilai tertinggi sebesar 0.14 terhadap atempature. 
                    - Sementara itu, windspeed memiliki korelasi negatif dengan fitur lainnya, terutama dengan humidity -0.24 dan temperature -0.16.
                    """)
      with st.expander("Recommendations & Suggestions"):
        st.markdown("""
                    - Tingkatkan ketersedian sepeda di musim dengan permintaan tinggi (gugur & panas).
                    - Lakukan promosi di musim dengan permintaan rendah (semi & dingin). 
                    - Lakukan penelitian lebih lanjut untuk mencari daerah dengan penyewa sepeda terbanyak.
                    """)

      st.divider()
      
  st.subheader("Renters According to Seasons")
  sum_rentals_per_weather = filtered_day_df.groupby('season')['total'].sum().reset_index()
  sum_rentals_per_weather.set_index('season', inplace=True)
  st.bar_chart(sum_rentals_per_weather)
  
  st.subheader("Renters According to Weather Conditions")
  sum_rentals_per_season = filtered_hour_df.groupby('weather')['total'].sum().reset_index()
  sum_rentals_per_season.set_index('weather', inplace=True)
  st.bar_chart(sum_rentals_per_season)

  st.subheader("Renters Per Month")
  sum_rentals_per_month = filtered_day_df.groupby('month')['total'].sum().reset_index()
  sum_rentals_per_month.set_index('month', inplace=True)
  st.bar_chart(sum_rentals_per_month)

  st.subheader("Renters Per Day")
  sum_rentals_per_day_weather = filtered_day_df.groupby(['weekday', 'weather'])['total'].sum().reset_index()
  sum_rentals_per_day_weather = sum_rentals_per_day_weather.groupby(['weekday', 'weather'])['total'].sum().unstack()
  st.bar_chart(sum_rentals_per_day_weather)

  st.subheader("Renters Per Hour")
  sum_rentals_per_hour_weather = filtered_hour_df.groupby(['hour', 'weather'])['total'].sum().reset_index()
  sum_rentals_per_hour_weather = sum_rentals_per_hour_weather.groupby(['hour', 'weather'])['total'].sum().unstack()
  st.bar_chart(sum_rentals_per_hour_weather)

  with st.expander("Conclusion"):
    st.markdown("""
                - Berdasarkan data penyewaan sepeda, musim gugur (fall) memiliki jumlah penyewa tertinggi dibandingkan musim lainnya, sementara musim semi (spring) memiliki jumlah penyewa terendah.
                - Dari segi kondisi cuaca, mayoritas penyewaan terjadi saat cuaca cerah, dengan penurunan signifikan saat hujan atau salju.
                - Secara bulanan, penyewaan meningkat dari Januari hingga mencapai puncaknya pada musim panas (Juni-Agustus) dan menurun kembali setelah Oktober.
                - Dari pola harian, jumlah penyewa relatif stabil sepanjang minggu dengan sedikit peningkatan pada hari kerja.
                - Penyewaan per jam menunjukkan lonjakan signifikan pada jam sibuk pagi (sekitar pukul 7-9) dan sore (16-18), menunjukkan penggunaan sepeda yang tinggi untuk keperluan transportasi harian.
                """)
  with st.expander("Recommendations & Suggestions"):
    st.markdown("""
                - Tingkatkan penyediaan sepeda terutama di musim gugur dan musim panas saat permintaan tinggi.
                - Memberikan promo diskon di musim semi yang memiliki penyewa terendah.
                - Sediakan fasilitas seperti shelter atau jas hujan dapat meningkatkan kenyamanan pengguna saat cuaca buruk. 
                - Optimalisasi jumlah sepeda di jam sibuk pagi dan sore juga penting untuk mengakomodasi lonjakan penyewa. 
                - Lakukan penelitian lebih lanjut untuk mendapatkan daerah dengan penyewa jam tertinggi pada jam - jam sibuk
                """)
  st.divider()

  st.caption("Copyright © 2025 Arya Ulya Krisna. All rights reserved.")

