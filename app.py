import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="Prediksi Risiko Dropout Siswa",
    page_icon="🎓",
    layout="centered"
)

@st.cache_resource
def load_artifacts():
    model = joblib.load('model/model_rf.pkl')
    scaler = joblib.load('model/scaler.pkl')
    label_encoder = joblib.load('model/label_encoder.pkl')
    return model, scaler, label_encoder

model, scaler, label_encoder = load_artifacts()

st.title("🎓 Prediksi Risiko Dropout Siswa")
st.markdown("""
Aplikasi ini membantu **Jaya Jaya Institut** memprediksi status siswa (Dropout, Enrolled, atau Graduate)
berdasarkan data akademik, demografis, dan sosial-ekonomi. Isi data siswa di bawah untuk mendapatkan prediksi.
""")

tab1, tab2, tab3, tab4 = st.tabs(["👤 Demografis", "💰 Finansial", "📚 Akademik (Awal)", "📊 Performa Semester"])

with tab1:
    st.subheader("Data Demografis")
    col1, col2 = st.columns(2)
    with col1:
        marital_status = st.selectbox("Status Pernikahan",
            options=[1, 2, 3, 4, 5, 6],
            format_func=lambda x: {1: "Single", 2: "Menikah", 3: "Duda/Janda", 4: "Cerai", 5: "Union", 6: "Pisah Hukum"}[x])
        gender = st.selectbox("Jenis Kelamin", options=[1, 0], format_func=lambda x: "Laki-laki" if x == 1 else "Perempuan")
        age_at_enrollment = st.number_input("Usia saat Mendaftar", min_value=17, max_value=70, value=20)
        nacionality = st.number_input("Kode Kewarganegaraan", min_value=1, value=1, help="1 = Portuguese (default)")
        international = st.selectbox("Mahasiswa Internasional?", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
    with col2:
        displaced = st.selectbox("Displaced Person?", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
        educational_special_needs = st.selectbox("Kebutuhan Khusus?", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
        mothers_occupation = st.number_input("Kode Pekerjaan Ibu", min_value=0, value=5)
        fathers_occupation = st.number_input("Kode Pekerjaan Ayah", min_value=0, value=5)
        mothers_qualification = st.number_input("Kode Pendidikan Ibu", min_value=1, value=19)
        fathers_qualification = st.number_input("Kode Pendidikan Ayah", min_value=1, value=19)

with tab2:
    st.subheader("Data Finansial")
    col1, col2 = st.columns(2)
    with col1:
        debtor = st.selectbox("Status Debtor", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")
        tuition_fees_up_to_date = st.selectbox("SPP Lunas/Up to Date?", options=[1, 0], format_func=lambda x: "Ya" if x == 1 else "Tidak")
    with col2:
        scholarship_holder = st.selectbox("Penerima Beasiswa?", options=[0, 1], format_func=lambda x: "Ya" if x == 1 else "Tidak")

    st.markdown("**Indikator Ekonomi (saat pendaftaran)**")
    col3, col4, col5 = st.columns(3)
    with col3:
        unemployment_rate = st.number_input("Unemployment Rate (%)", value=11.1, format="%.1f")
    with col4:
        inflation_rate = st.number_input("Inflation Rate (%)", value=1.4, format="%.1f")
    with col5:
        gdp = st.number_input("GDP", value=0.32, format="%.2f")

with tab3:
    st.subheader("Data Akademik Awal (Sebelum Kuliah)")
    col1, col2 = st.columns(2)
    with col1:
        application_mode = st.number_input("Kode Metode Aplikasi", min_value=1, value=1)
        application_order = st.number_input("Urutan Pilihan (0=pilihan pertama)", min_value=0, max_value=9, value=1)
        course = st.number_input("Kode Program Studi", min_value=1, value=9254)
        daytime_evening_attendance = st.selectbox("Kelas", options=[1, 0], format_func=lambda x: "Siang" if x == 1 else "Malam")
    with col2:
        previous_qualification = st.number_input("Kode Kualifikasi Sebelumnya", min_value=1, value=1)
        previous_qualification_grade = st.number_input("Nilai Kualifikasi Sebelumnya (0-200)", min_value=0.0, max_value=200.0, value=130.0)
        admission_grade = st.number_input("Nilai Admisi (0-200)", min_value=0.0, max_value=200.0, value=127.0)

with tab4:
    st.subheader("Performa Akademik Semester 1 & 2")
    st.markdown("**Semester 1**")
    col1, col2 = st.columns(2)
    with col1:
        cu_1st_credited = st.number_input("Mata Kuliah Credited (Sem 1)", min_value=0, value=0)
        cu_1st_enrolled = st.number_input("Mata Kuliah Enrolled (Sem 1)", min_value=0, value=6)
        cu_1st_evaluations = st.number_input("Mata Kuliah Evaluations (Sem 1)", min_value=0, value=8)
    with col2:
        cu_1st_approved = st.number_input("Mata Kuliah Approved (Sem 1)", min_value=0, value=5)
        cu_1st_grade = st.number_input("Rata-rata Nilai (Sem 1)", min_value=0.0, max_value=20.0, value=12.0)
        cu_1st_without_eval = st.number_input("Tanpa Evaluasi (Sem 1)", min_value=0, value=0)

    st.markdown("**Semester 2**")
    col3, col4 = st.columns(2)
    with col3:
        cu_2nd_credited = st.number_input("Mata Kuliah Credited (Sem 2)", min_value=0, value=0)
        cu_2nd_enrolled = st.number_input("Mata Kuliah Enrolled (Sem 2)", min_value=0, value=6)
        cu_2nd_evaluations = st.number_input("Mata Kuliah Evaluations (Sem 2)", min_value=0, value=8)
    with col4:
        cu_2nd_approved = st.number_input("Mata Kuliah Approved (Sem 2)", min_value=0, value=5)
        cu_2nd_grade = st.number_input("Rata-rata Nilai (Sem 2)", min_value=0.0, max_value=20.0, value=12.0)
        cu_2nd_without_eval = st.number_input("Tanpa Evaluasi (Sem 2)", min_value=0, value=0)

st.markdown("---")

if st.button("🔍 Prediksi Status Siswa", use_container_width=True, type="primary"):
    input_data = pd.DataFrame([{
        'Marital_status': marital_status,
        'Application_mode': application_mode,
        'Application_order': application_order,
        'Course': course,
        'Daytime_evening_attendance': daytime_evening_attendance,
        'Previous_qualification': previous_qualification,
        'Previous_qualification_grade': previous_qualification_grade,
        'Nacionality': nacionality,
        'Mothers_qualification': mothers_qualification,
        'Fathers_qualification': fathers_qualification,
        'Mothers_occupation': mothers_occupation,
        'Fathers_occupation': fathers_occupation,
        'Admission_grade': admission_grade,
        'Displaced': displaced,
        'Educational_special_needs': educational_special_needs,
        'Debtor': debtor,
        'Tuition_fees_up_to_date': tuition_fees_up_to_date,
        'Gender': gender,
        'Scholarship_holder': scholarship_holder,
        'Age_at_enrollment': age_at_enrollment,
        'International': international,
        'Curricular_units_1st_sem_credited': cu_1st_credited,
        'Curricular_units_1st_sem_enrolled': cu_1st_enrolled,
        'Curricular_units_1st_sem_evaluations': cu_1st_evaluations,
        'Curricular_units_1st_sem_approved': cu_1st_approved,
        'Curricular_units_1st_sem_grade': cu_1st_grade,
        'Curricular_units_1st_sem_without_evaluations': cu_1st_without_eval,
        'Curricular_units_2nd_sem_credited': cu_2nd_credited,
        'Curricular_units_2nd_sem_enrolled': cu_2nd_enrolled,
        'Curricular_units_2nd_sem_evaluations': cu_2nd_evaluations,
        'Curricular_units_2nd_sem_approved': cu_2nd_approved,
        'Curricular_units_2nd_sem_grade': cu_2nd_grade,
        'Curricular_units_2nd_sem_without_evaluations': cu_2nd_without_eval,
        'Unemployment_rate': unemployment_rate,
        'Inflation_rate': inflation_rate,
        'GDP': gdp,
    }])

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    prediction_proba = model.predict_proba(input_scaled)[0]
    predicted_label = label_encoder.inverse_transform([prediction])[0]

    st.markdown("## Hasil Prediksi")

    if predicted_label == "Dropout":
        st.error(f"⚠️ **Status Prediksi: {predicted_label}**")
        st.markdown("Siswa ini terindikasi **berisiko tinggi untuk dropout**. Disarankan segera diberikan bimbingan khusus.")
    elif predicted_label == "Enrolled":
        st.warning(f"📘 **Status Prediksi: {predicted_label}**")
        st.markdown("Siswa ini diprediksi **masih aktif berkuliah**, namun tetap perlu dipantau performanya.")
    else:
        st.success(f"🎓 **Status Prediksi: {predicted_label}**")
        st.markdown("Siswa ini diprediksi memiliki **peluang baik untuk lulus (Graduate)**.")

    st.markdown("### Detail Probabilitas per Kelas")
    proba_df = pd.DataFrame({
        'Status': label_encoder.classes_,
        'Probabilitas': prediction_proba
    }).sort_values('Probabilitas', ascending=False)

    for _, row in proba_df.iterrows():
        st.write(f"**{row['Status']}**")
        st.progress(float(row['Probabilitas']))
        st.caption(f"{row['Probabilitas']*100:.1f}%")
