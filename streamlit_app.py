import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st

st.set_page_config(page_title="Evaluasi Baku Mutu Air Limbah")

st.title("💧 Sistem Evaluasi Baku Mutu Air Limbah")

st.write("Masukkan hasil analisis laboratorium:")

# Input data
bod = st.number_input("BOD (mg/L)", min_value=0.0, value=30.0)
cod = st.number_input("COD (mg/L)", min_value=0.0, value=100.0)
tss = st.number_input("TSS (mg/L)", min_value=0.0, value=30.0)
nh3 = st.number_input("NH₃ (mg/L)", min_value=0.0, value=5.0)
ph = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0)

# Baku mutu (dapat disesuaikan)
baku_mutu = {
    "BOD": 30,
    "COD": 100,
    "TSS": 30,
    "NH₃": 10,
    "pH_min": 6,
    "pH_max": 9
}

if st.button("Evaluasi"):

    pelanggaran = []

    if bod > baku_mutu["BOD"]:
        pelanggaran.append("BOD")

    if cod > baku_mutu["COD"]:
        pelanggaran.append("COD")

    if tss > baku_mutu["TSS"]:
        pelanggaran.append("TSS")

    if nh3 > baku_mutu["NH₃"]:
        pelanggaran.append("NH₃")

    if ph < baku_mutu["pH_min"] or ph > baku_mutu["pH_max"]:
        pelanggaran.append("pH")

    total_parameter = 5
    persentase = (len(pelanggaran) / total_parameter) * 100

    st.subheader("Hasil Evaluasi")

    if len(pelanggaran) == 0:
        st.success("✅ Memenuhi Baku Mutu")
    else:
        st.error("❌ Tidak Memenuhi Baku Mutu")

        st.write("**Parameter yang melampaui batas:**")
        for p in pelanggaran:
            st.write(f"- {p}")

    st.write(f"**Persentase Pelanggaran: {persentase:.2f}%**")

    # Tabel ringkasan
    st.subheader("Ringkasan Data")

    data = {
        "Parameter": ["BOD", "COD", "TSS", "NH₃", "pH"],
        "Nilai": [bod, cod, tss, nh3, ph],
        "Baku Mutu": [
            baku_mutu["BOD"],
            baku_mutu["COD"],
            baku_mutu["TSS"],
            baku_mutu["NH₃"],
            f'{baku_mutu["pH_min"]}-{baku_mutu["pH_max"]}'
        ]
    }

    st.table(data)
