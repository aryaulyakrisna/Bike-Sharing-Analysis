import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Import dataset
day_df = pd.read_csv("main_day_data.csv")
hour_df = pd.read_csv("main_hour_data.csv")

# Sidebar
with st.sidebar:
    st.title("_Bar Analysis_ 🚲")

    min_date = day_df["date"].min()
    max_date = day_df["date"].max()
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    main_day_df = day_df[(day_df["date"] >= str(start_date)) & 
                (day_df["date"] <= str(end_date))]
    
    main_hour_df = hour_df[(hour_df["date"] >= str(start_date)) & 
                (hour_df["date"] <= str(end_date))]

# Main Content
with st.container():
    st.title("_Bike Sharing Analysis_ 🚲")
    st.subheader('Selamat Datang 👋')

    st.divider()

    st.subheader("Perbandingan jumlah penyewa sepeda pada tahun 2011 sengan tahun 2012")

    monthly_rentals = day_df.groupby(['year', 'month'])['total'].mean().reset_index()

    pivot_rentals = monthly_rentals.pivot(index='month', columns='year', values='total')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=pivot_rentals, marker='o', ax=ax)
    ax.set_title('Perbandingan Rata-rata Penyewa Sepeda per Bulan (2011 vs 2012)')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.grid(True)
    ax.legend(title='Tahun')

    st.pyplot(fig)

    st.divider()

    col1, col2 = st.columns(2)

    casual = day_df['casual'].sum()
    registered = day_df['registered'].sum()
    total = day_df['total'].sum()

    with col1:
        st.metric("Tahun", "2011-2012", border=True)

    with col2:
        st.metric("Tidak Mendaftar", value=f"{casual:,}", border=True)

    with col1:
        st.metric("Terdaftar", value=f"{registered:,}", border=True)

    with col2:
        st.metric("Total", value=f"{total:,}", border=True)
    
    st.divider()

    st.markdown("1. Apakah terdapat perbedaan yang signifikan dalam jumlah penyewaan sepeda antara hari kerja dan hari libur pada musim tertentu?")

    data = main_day_df.groupby(['season', 'holiday']).agg({
        "total": ["mean"]
    }).reset_index()

    data.columns = ['season', 'holiday', 'mean']

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=data, x='season', y='mean', hue='holiday', palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda per Musim (Hari Kerja vs Hari Libur)')
    ax.set_xlabel('Musim')
    ax.set_ylabel('Rata-rata Penyewaan Sepeda')
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles=handles, labels=['Hari Kerja', 'Hari Libur'])
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    st.divider()

    st.markdown("2. Faktor apa saja yang paling memengaruhi jumlah penyewaan sepeda setiap harinya?")

    corr = main_day_df[['temperature', 'atemperature', 'humidity', 'windspeed']].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Heatmap Korelasi Antar Fitur')

    st.pyplot(fig)

    st.divider()

    st.markdown("3. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda pada jam sibuk?")

    mean_rentals_per_hour = hour_df.groupby('hour')['total'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x='hour', y='total', data=mean_rentals_per_hour, hue='hour', palette='coolwarm', legend=False, ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_xticks(range(0, 24))

    st.pyplot(fig)

    mean_rentals_per_weather = main_hour_df.groupby('weather')['total'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weather', y='total', data=mean_rentals_per_weather, hue='weather', palette="coolwarm", dodge=False, legend=False, ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
    ax.set_xlabel('Kondisi Cuaca')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    st.pyplot(fig)

    mean_rentals_per_hour_weather = main_hour_df.groupby(['hour', 'weather'])['total'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.barplot(x='hour', y='total', hue='weather', data=mean_rentals_per_hour_weather, palette='coolwarm', ax=ax)
    ax.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Jam dan Kondisi Cuaca')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.legend(title='Kondisi Cuaca')

    st.pyplot(fig)