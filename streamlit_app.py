import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Evaluasi Baku Mutu Air Limbah", layout="wide")

st.title("🌿 Sistem Evaluasi Baku Mutu Air Limbah")

# =========================
# BAKU MUTU (contoh)
# =========================
baku_mutu = {
    "pH_min": 6,
    "pH_max": 9,
    "BOD": 30,
    "COD": 100,
    "TSS": 30,
    "NH3": 10
}

# =========================
# INIT SESSION STATE
# =========================
if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# INPUT DATA
# =========================
st.subheader("📥 Informasi Sampel")

col1, col2, col3 = st.columns(3)

with col1:
    jenis_sampel = st.text_input("Jenis Sampel")

with col2:
    nama_penyampling = st.text_input("Nama Penyampling")

with col3:
    tanggal = st.date_input("Tanggal Pengambilan Sampel", value=date.today())

st.subheader("📊 Data Hasil Analisis")

col1, col2 = st.columns(2)

with col1:
    ph = st.number_input("pH", value=7.0)
    bod = st.number_input("BOD (mg/L)", value=0.0)
    cod = st.number_input("COD (mg/L)", value=0.0)

with col2:
    tss = st.number_input("TSS (mg/L)", value=0.0)
    nh3 = st.number_input("NH3-N (mg/L)", value=0.0)

# =========================
# EVALUASI
# =========================
hasil = {
    "pH": baku_mutu["pH_min"] <= ph <= baku_mutu["pH_max"],
    "BOD": bod <= baku_mutu["BOD"],
    "COD": cod <= baku_mutu["COD"],
    "TSS": tss <= baku_mutu["TSS"],
    "NH3": nh3 <= baku_mutu["NH3"]
}

# =========================
# BUTTON ANALISIS
# =========================
if st.button("🔍 Analisis Data"):

    st.subheader("📊 Hasil Evaluasi")

    parameter_tidak_memenuhi = []

    for k, v in hasil.items():
        if v:
            st.success(f"{k} → Memenuhi")
        else:
            st.error(f"{k} → Tidak Memenuhi")
            parameter_tidak_memenuhi.append(k)

    # Status
    if len(parameter_tidak_memenuhi) == 0:
        status = "Memenuhi Baku Mutu"
        st.success("✅ STATUS: MEMENUHI BAKU MUTU")
    else:
        status = "Tidak Memenuhi Baku Mutu"
        st.error("❌ STATUS: TIDAK MEMENUHI BAKU MUTU")

        st.write("### ⚠ Parameter yang Melampaui Batas:")
        for p in parameter_tidak_memenuhi:
            st.write(f"- {p}")

    # Persentase pelanggaran
    persentase = (len(parameter_tidak_memenuhi) / len(hasil)) * 100
    st.metric("Persentase Pelanggaran", f"{persentase:.1f}%")

    # =========================
    # SIMPAN RIWAYAT
    # =========================
    st.session_state.data.append({
        "Tanggal": tanggal,
        "Jenis Sampel": jenis_sampel,
        "Nama Penyampling": nama_penyampling,
        "pH": ph,
        "BOD": bod,
        "COD": cod,
        "TSS": tss,
        "NH3": nh3,
        "Status": status,
        "Pelanggaran (%)": round(persentase, 1)
    })

# =========================
# RIWAYAT
# =========================
st.subheader("📁 Riwayat Pengujian")

if len(st.session_state.data) > 0:
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data pengujian.") 
