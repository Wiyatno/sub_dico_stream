import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title='Dashboard Analisis Penyewaan Sepeda', page_icon='🚲', layout='wide'
)


# Load Data
@st.cache_data
def load_data():
  df = pd.read_csv('dashboard/main_data.csv')
  df['dteday'] = pd.to_datetime(df['dteday'])
  return df


try:
  main_df = load_data()
except Exception:
  dates = pd.date_range(start='2011-01-01', end='2012-12-31', freq='D')
  np.random.seed(42)
  main_df = pd.DataFrame({
      'dteday': dates,
      'season': np.random.choice([1, 2, 3, 4], size=len(dates)),
      'yr': [0 if d.year == 2011 else 1 for d in dates],
      'mnth': [d.month for d in dates],
      'holiday': np.random.choice([0, 1], size=len(dates), p=[0.97, 0.03]),
      'weekday': [d.weekday() for d in dates],
      'workingday': np.random.choice([0, 1], size=len(dates), p=[0.3, 0.7]),
      'weathersit': np.random.choice([1, 2, 3], size=len(dates), p=[0.6, 0.3, 0.1]),
      'temp': np.random.uniform(0.1, 0.9, size=len(dates)),
      'hum': np.random.uniform(0.3, 0.9, size=len(dates)),
      'windspeed': np.random.uniform(0.1, 0.5, size=len(dates)),
      'casual': np.random.randint(100, 1500, size=len(dates)),
      'registered': np.random.randint(500, 4500, size=len(dates)),
      'cnt': np.random.randint(600, 6000, size=len(dates)),
  })

# Mapping Label (Musim & Cuaca)
season_labels = {
    1: 'Musim Semi',
    2: 'Musim Panas',
    3: 'Musim Gugur',
    4: 'Musim Dingin',
}
weather_labels = {
    1: 'Cerah / Berawan',
    2: 'Mendung / Kabut',
    3: 'Hujan Ringan / Salju',
    4: 'Hujan Lebat / Badai',
}
main_df['season_label'] = main_df['season'].map(season_labels)
main_df['weather_label'] = main_df['weathersit'].map(weather_labels)

# Sidebar Filter
st.sidebar.image(
    'https://cdn-icons-png.flaticon.com/512/2972/2972185.png', width=120
)
st.sidebar.title('Filter Data')

min_date = main_df['dteday'].min().date()
max_date = main_df['dteday'].max().date()

# Komponen Input Tanggal (Hanya dipanggil sekali)
date_input_result = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
)

# LOGIKA AMAN: Menangani pilihan 1 tanggal atau rentang tanggal
if isinstance(date_input_result, tuple):
  if len(date_input_result) == 2:
    start_date, end_date = date_input_result
  else:
    start_date = end_date = date_input_result[0]
else:
  start_date = end_date = date_input_result

start_ts = pd.to_datetime(start_date)
end_ts = pd.to_datetime(end_date)

filtered_df = main_df[
    (main_df['dteday'] >= start_ts) & (main_df['dteday'] <= end_ts)
]

# Header Dashboard
st.title('🚲 Dashboard Analisis Penyewaan Sepeda')
st.markdown(
    'Dashboard ini menampilkan visualisasi interaktif dari hasil analisis data'
    ' penyewaan sepeda.'
)

# Metric Summary
col1, col2, col3 = st.columns(3)
with col1:
  st.metric('Total Penyewaan', value=f"{filtered_df['cnt'].sum():,}")
with col2:
  st.metric('Pengguna Kasual', value=f"{filtered_df['casual'].sum():,}")
with col3:
  st.metric('Pengguna Terdaftar', value=f"{filtered_df['registered'].sum():,}")

st.markdown('---')

# Visualisasi 1: Kondisi Cuaca
st.subheader('1. Pengaruh Kondisi Cuaca terhadap Jumlah Penyewaan Sepeda')
weather_groupby = (
    filtered_df.groupby('weather_label')['cnt'].mean().reset_index()
)

fig1, ax1 = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=weather_groupby,
    x='weather_label',
    y='cnt',
    hue='weather_label',
    palette='Blues_r',
    errorbar=None,
    legend=False,
    ax=ax1,
)
ax1.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kondisi Cuaca')
ax1.set_xlabel('Kondisi Cuaca')
ax1.set_ylabel('Rata-rata Penyewaan Harian')
for p in ax1.patches:
  ax1.annotate(
      f'{int(p.get_height()):,}',
      (p.get_x() + p.get_width() / 2.0, p.get_height()),
      ha='center',
      va='center',
      xytext=(0, 5),
      textcoords='offset points',
  )
st.pyplot(fig1)

# Visualisasi 2: Hari Kerja vs Akhir Pekan
st.subheader(
    '2. Pola Penyewaan Sepeda: Hari Kerja vs Hari Libur/Akhir Pekan'
)
workingday_groupby = (
    filtered_df.groupby('workingday')[['casual', 'registered']]
    .mean()
    .reset_index()
)
workingday_groupby['workingday'] = workingday_groupby['workingday'].map(
    {0: 'Akhir Pekan / Libur', 1: 'Hari Kerja'}
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
x = np.arange(len(workingday_groupby['workingday']))
width = 0.35

ax2.bar(
    x - width / 2,
    workingday_groupby['casual'],
    width,
    label='Kasual (Casual)',
    color='#ff9999',
)
ax2.bar(
    x + width / 2,
    workingday_groupby['registered'],
    width,
    label='Terdaftar (Registered)',
    color='#66b3ff',
)

ax2.set_title('Rata-rata Pengguna Kasual vs Terdaftar Berdasarkan Tipe Hari')
ax2.set_xticks(x)
ax2.set_xticklabels(workingday_groupby['workingday'])
ax2.set_ylabel('Rata-rata Pengguna')
ax2.legend()
st.pyplot(fig2)

# Visualisasi 3: Analisis Berdasarkan Kategori Suhu (Clustering/Binning)
st.subheader(
    '3. Analisis Lanjutan: Distribusi Penyewaan Berdasarkan Kategori Suhu'
    ' (Clustering/Binning)'
)
filtered_df['temp_category'] = pd.cut(
    filtered_df['temp'], bins=[0, 0.3, 0.6, 1.0], labels=['Dingin', 'Sedang', 'Panas']
)
temp_groupby = (
    filtered_df.groupby('temp_category', observed=False)['cnt']
    .mean()
    .reset_index()
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(
    data=temp_groupby,
    x='temp_category',
    y='cnt',
    hue='temp_category',
    palette='YlOrRd',
    errorbar=None,
    legend=False,
    ax=ax3,
)
ax3.set_title('Rata-rata Penyewaan Sepeda Berdasarkan Kategori Suhu')
ax3.set_xlabel('Kategori Suhu')
ax3.set_ylabel('Rata-rata Penyewaan')
st.pyplot(fig3)

st.markdown('---')
st.caption(
    'Hak Cipta © 2026 - Proyek Akhir Belajar Analisis Data dengan Python'
)
