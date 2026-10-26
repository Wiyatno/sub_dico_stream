# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi
Proyek ini merupakan submission proyek akhir untuk kelas Analisis Data. 
Proyek ini bertujuan untuk menganalisis data penyewaan sepeda (*Bike Sharing Dataset*) untuk menganalisis pola penggunaan berdasarkan kondisi cuaca, musim, dan tipe pengguna (*casual*/belum terdaftar vs *registered*/sudah terdaftar), 
serta menampilkan hasilnya melalui dashboard Streamlit.

## Dibuat Oleh
- **Nama**: Toyo Wiyatno
- **Email**: toyo.pmc@gmail.com
- **ID Dicoding**: https://www.dicoding.com/users/toyowiyatno

## Struktur Direktori
```text
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   └───day.csv
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Cara Menjalankan Dashboard Streamlit

### 1. Persiapan Lingkungan (Setup Environment)
Buka terminal / command prompt dan jalankan perintah berikut:

```bash
# Pindah ke direktori submission
cd submission

# (Opsional) Buat virtual environment
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
# venv\Scripts\activate   # Untuk Windows

# Install dependensi
pip install -r requirements.txt
```

### 2. Menjalankan Dashboard
Jalankan perintah berikut pada terminal:

```bash
streamlit run dashboard/dashboard.py
```

Dashboard interaktif akan terbuka secara otomatis pada browser Anda di `http://localhost:8501`.

note; jangan runing langsung dari IDE/klik langsung file *.py* karena akan reror