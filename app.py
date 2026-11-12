import streamlit as st
import pandas as pd
import os

# Konfigurasi Halaman (Wide Mode agar layar penuh ke samping)
st.set_page_config(page_title="PT Protobion - LabSales Database", layout="wide")

# --- KUSTOMISASI FONT & TAMPILAN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-title {
        font-weight: 700;
        color: #1E293B;
        margin-top: 10px;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #64748B;
        font-size: 16px;
        margin-bottom: 20px;
    }
    
    /* Memperbaiki jarak logo di sidebar */
    [data-testid="stSidebar"] img {
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEM LOGIN / KEAMANAN ---
def check_password():
    """Mengembalikan True jika pengguna memasukkan password yang benar."""
    
    def password_entered():
        if st.session_state["username"] == "admin" and st.session_state["password"] == "protobion123":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center;'>🔐 Login Sistem Internal PT Protobion</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>Silakan masukkan kredensial akun untuk mengakses database penjualan.</p>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.button("Masuk Aplikasi", on_click=password_entered)
        return False
    
    elif not st.session_state["password_correct"]:
        st.markdown("<h2 style='text-align: center;'>🔐 Login Sistem Internal PT Protobion</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.button("Masuk Aplikasi", on_click=password_entered)
            st.error("😕 Username atau password salah. Silakan coba lagi.")
        return False
    else:
        return True

# Jika belum login, hentikan eksekusi di sini
if not check_password():
    st.stop()

# ==========================================
# APLIKASI UTAMA (Hanya tampil setelah login benar)
# ==========================================

DB_FILE = "database_sales_lab.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        df = pd.DataFrame(columns=[
            "Nama Klien / Institusi", 
            "Sektor", 
            "Nama PIC / Narahubung", 
            "Jabatan", 
            "No. WhatsApp", 
            "Email", 
            "Catatan / Alat Lab yang Diminati",
            "Status Prospek"
        ])
        df.to_csv(DB_FILE, index=False)
        return df

df = load_data()

# --- MANAJEMEN BILAH SAMPING (SIDEBAR) ---
with st.sidebar:
    # 1. MENAMPILKAN "logo.jpeg" DI ATAS SIDEBAR
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", use_container_width=True)
    elif os.path.exists("logo.jpg"): 
        st.image("logo.jpg", use_container_width=True)
    else:
        st.warning("⚠️ File 'logo.jpeg' tidak ditemukan di folder proyek Anda.")

    st.markdown("---")

    # Menu "➕ Tambah Klien / PIC Baru"
    st.header("➕ Tambah Klien / PIC Baru")
    with st.form("form_tambah", clear_on_submit=True):
        nama_klien = st.text_input("Nama Klien / Institusi")
        sektor = st.selectbox("Sektor", ["Universitas/Kampus", "Rumah Sakit", "Laboratorium Swasta/Komersial", "Pemerintahan/BRIN"])
        nama_pic = st.text_input("Nama Narahubung (PIC)")
        jabatan = st.text_input("Jabatan")
        wa = st.text_input("No. WhatsApp")
        email = st.text_input("Email")
        catatan = st.text_area("Catatan / Alat Lab yang Diminati")
        status = st.selectbox("Status Prospek", ["Cold", "Warm", "Hot", "Pelanggan Aktif"])
        
        submit_button = st.form_submit_button(label="Simpan Data")
        
        if submit_button:
            if nama_klien and nama_pic:
                data_baru = pd.DataFrame({
                    "Nama Klien / Institusi": [nama_klien],
                    "Sektor": [sektor],
                    "Nama PIC / Narahubung": [nama_pic],
                    "Jabatan": [jabatan],
                    "No. WhatsApp": [wa],
                    "Email": [email],
                    "Catatan / Alat Lab yang Diminati": [catatan],
                    "Status Prospek": [status]
                })
                df = pd.concat([df, data_baru], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success("Data berhasil disimpan!")
                st.rerun()
            else:
                st.error("Nama Klien dan Nama PIC wajib diisi!")

    # Menu Hapus Data
    if not df.empty:
        st.markdown("---")
        st.subheader("🗑️ Hapus Data Klien")
        pilihan_klien = [f"{row['Nama Klien / Institusi']} (PIC: {row['Nama PIC / Narahubung']})" for index, row in df.iterrows()]
        klien_terpilih = st.sidebar.selectbox("Pilih Klien yang ingin dihapus:", pilihan_klien, key="hapus_selectbox")
        
        if st.sidebar.button("Hapus Data Terpilih"):
            index_terpilih = pilihan_klien.index(klien_terpilih)
            df = df.drop(index_terpilih).reset_index(drop=True)
            df.to_csv(DB_FILE, index=False)
            st.success("Data klien berhasil dihapus!")
            st.rerun()

    # Tombol Logout
    st.markdown("---")
    if st.button("🔒 Keluar (Logout)"):
        st.session_state["password_correct"] = False
        st.rerun()

# --- HALAMAN UTAMA ---

# 2. MENAMPILKAN "gambar.jpeg" MEMANJANG DI ATAS JUDUL
if os.path.exists("gambar.jpeg"):
    st.image("gambar.jpeg", use_container_width=True)
elif os.path.exists("gambar.jpg"):
    st.image("gambar.jpg", use_container_width=True)
else:
    st.warning("⚠️ File 'gambar.jpeg' (untuk halaman utama) tidak ditemukan di folder proyek Anda.")

# Judul dan Deskripsi Formal
st.markdown("<h2 class='main-title'>Database penjualan & Narahubung Customer</h2>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Sistem Manajemen Customer — Protobion</p>", unsafe_allow_html=True)

st.markdown("---")

# Tampilan Tabel
st.subheader("📋 Daftar Database Klien & Narahubung")

search_query = st.text_input("🔍 Cari berdasarkan Nama Klien, PIC, atau Alat yang Diminati:")

if search_query:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
    filtered_df = df[mask]
else:
    filtered_df = df

edited_df = st.data_editor(
    filtered_df, 
    use_container_width=True, 
    num_rows="dynamic",
    key="tabel_database"
)

# Tombol Simpan Perubahan ke CSV
if st.button("💾 Simpan Perubahan Tabel"):
    if search_query:
        df.loc[mask] = edited_df
    else:
        df = edited_df
    df.to_csv(DB_FILE, index=False)
    st.success("Perubahan data berhasil disimpan!")
    st.rerun()

st.info(f"Total data tersimpan: {len(df)} narahubung")