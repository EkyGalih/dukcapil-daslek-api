# Dukcapil API - Desa Dasan Lekong

API untuk integrasi data kependudukan Desa Dasan Lekong dengan sistem web desa. 
API ini memungkinkan akses ke data kependudukan, pencatatan peristiwa penting, 
serta layanan administrasi desa yang terintegrasi dengan Dukcapil.

## 🚀 Fitur Utama

- Autentikasi API dengan Token
- Endpoint Data Kependudukan (Penduduk, Kartu Keluarga, dll)
- Endpoint Peristiwa Kependudukan (Kelahiran, Kematian, Pindah, Datang)
- Dokumentasi API dengan OpenAPI/Swagger
- Format response JSON yang konsisten

## 📦 Instalasi

1. Clone repositori API ini:
   ```bash
   git clone https://github.com/username/dukcapil-api-dasan-lekong.git
   cd dukcapil-api-dasan-lekong
   ```

2. Copy file `.env.example` menjadi `.env` dan sesuaikan konfigurasi:
   ```bash
   cp .env.example .env
   ```

3. Install dependencies:
   ```bash
   go mod tidy
   ```

4. Jalankan aplikasi:
   ```bash
   go run main.go
   ```

## 🔑 Autentikasi

Gunakan token Bearer untuk mengakses endpoint API. 
Token dapat diperoleh melalui admin sistem desa.

Contoh header:
```http
Authorization: Bearer <token_anda>
```

## 📖 Dokumentasi Endpoint

| Endpoint               | Method | Deskripsi                          |
|-------------------------|--------|------------------------------------|
| `/api/penduduk`        | GET    | Menampilkan daftar penduduk        |
| `/api/penduduk/:id`    | GET    | Menampilkan detail penduduk        |
| `/api/kk`              | GET    | Menampilkan daftar kartu keluarga  |
| `/api/kelahiran`       | POST   | Mencatat kelahiran                 |
| `/api/kematian`        | POST   | Mencatat kematian                  |
| `/api/pindah`          | POST   | Mencatat kepindahan                |
| `/api/datang`          | POST   | Mencatat kedatangan                |

## 📂 Struktur Proyek

```
dukcapil-api-dasan-lekong/
├── main.go
├── controllers/
├── models/
├── routes/
├── utils/
├── .env.example
└── README_API.md
```

## 🛠 Teknologi

- Golang (Gin/Echo Framework)
- PostgreSQL/MySQL (sesuaikan kebutuhan)
- JWT Authentication
- Swagger (OpenAPI Docs)

## 📜 Lisensi

MIT License © 2025 Desa Dasan Lekong
