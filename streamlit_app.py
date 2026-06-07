import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Evaluasi Baku Mutu Air Limbah", layout="wide")

st.title("🌿 Sistem Evaluasi Baku Mutu Air Limbah")

# =========================
# BAKU MUTU (contoh)
# =========================
baku_mutu = {
    "pH_min": 6,
    "pH_max": 9,
    "BOD": 50,
    "COD": 100,
    "TSS": 50,
    "NH3": 10
}

# =========================
# INIT SESSION STATE (RIWAYAT)
# =========================
if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# INPUT DATA
# =========================
st.subheader("📥 Input Data Pengujian")

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH", value=7.0)
    bod = st.number_input("BOD (mg/L)", value=0.0)
    cod = st.number_input("COD (mg/L)", value=0.0)

with col2:
    tss = st.number_input("TSS (mg/L)", value=0.0)
    nh3 = st.number_input("NH3-N (mg/L)", value=0.0)

tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# =========================
# EVALUASI
# =========================
def cek(parameter, nilai, batas):
    return nilai <= batas

hasil = {
    "pH": baku_mutu["pH_min"] <= ph <= baku_mutu["pH_max"],
    "BOD": cek("BOD", bod, baku_mutu["BOD"]),
    "COD": cek("COD", cod, baku_mutu["COD"]),
    "TSS": cek("TSS", tss, baku_mutu["TSS"]),
    "NH3": cek("NH3", nh3, baku_mutu["NH3"])
}

jumlah_memenuhi = sum(hasil.values())
total = len(hasil)

# =========================
# BUTTON PROSES
# =========================
if st.button("🔍 Analisis Data"):

    st.subheader("📊 Hasil Evaluasi")

    for k, v in hasil.items():
        if v:
            st.success(f"{k} → Memenuhi")
        else:
            st.error(f"{k} → Tidak Memenuhi")

    kepatuhan = (jumlah_memenuhi / total) * 100

    st.metric("Tingkat Kepatuhan", f"{kepatuhan:.1f}%")

    # =========================
    # SIMPAN KE RIWAYAT
    # =========================
    st.session_state.data.append({
        "Tanggal": tanggal,
        "pH": ph,
        "BOD": bod,
        "COD": cod,
        "TSS": tss,
        "NH3": nh3,
        "Kepatuhan (%)": kepatuhan
    })

# =========================
# RIWAYAT DATA
# =========================
st.subheader("📁 Riwayat Pengujian")

if len(st.session_state.data) > 0:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df, use_container_width=True)

    st.subheader("📈 Grafik Tren Kepatuhan")
    st.line_chart(df.set_index("Tanggal")["Kepatuhan (%)"])
else:
    st.info("Belum ada data pengujian.")
