import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import random

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Lab Diskon & Persentase",
    page_icon="🏷️",
    layout="wide"
)

# --- CSS untuk Tampilan Kasir ---
st.markdown("""
<style>
    .harga-box {
        background-color: #d4efdf;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #27ae60;
    }
    .diskon-box {
        background-color: #fadbd8;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #c0392b;
    }
    .big-text { font-size: 24px; font-weight: bold; }
    .small-text { font-size: 14px; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- Helper Function: Format Rupiah ---
def format_rupiah(angka):
    return f"Rp {int(angka):,}".replace(",", ".")

# --- Judul ---
st.title("🏷️ Laboratorium Virtual: Diskon & Persentase")
st.caption("Belajar matematika lewat simulasi belanja di Toko Virtual!")

# --- Tabs Navigasi ---
tab1, tab2, tab3 = st.tabs(["🛍️ Simulasi Diskon", "⚠️ Diskon Ganda (50%+20%)", "🛒 Tantangan Kasir"])

# ==========================================
# TAB 1: SIMULASI DISKON TUNGGAL
# ==========================================
with tab1:
    st.header("Simulasi Belanja Sederhana")
    
    col_input, col_vis = st.columns([1, 1.5])
    
    with col_input:
        st.subheader("⚙️ Atur Harga")
        harga_awal = st.number_input("Harga Barang (Rp)", min_value=1000, value=100000, step=5000)
        persen_diskon = st.slider("Besar Diskon (%)", 0, 100, 25)
        
        # Perhitungan
        nilai_hemat = harga_awal * (persen_diskon / 100)
        harga_akhir = harga_awal - nilai_hemat
        
        st.markdown("---")
        # Menampilkan Box Hasil
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div class="diskon-box">
                <div class="small-text">Kamu Hemat</div>
                <div class="big-text">{format_rupiah(nilai_hemat)}</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="harga-box">
                <div class="small-text">Harus Bayar</div>
                <div class="big-text">{format_rupiah(harga_akhir)}</div>
            </div>
            """, unsafe_allow_html=True)

    with col_vis:
        st.subheader("📊 Visualisasi Potongan")
        
        # Donut Chart untuk menunjukkan porsi bayar vs hemat
        labels = ['Harus Dibayar', 'Uang Dihemat (Diskon)']
        values = [harga_akhir, nilai_hemat]
        colors = ['#2ecc71', '#e74c3c'] # Hijau bayar, Merah hemat

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker=dict(colors=colors))])
        fig.update_layout(title_text=f"Proporsi Harga Barang (Diskon {persen_diskon}%)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Analogi Sederhana
        if nilai_hemat > 0:
            st.info(f"💡 **Tahukah kamu?** Uang yang kamu hemat ({format_rupiah(nilai_hemat)}) bisa dipakai untuk membeli **{int(nilai_hemat/5000)} bungkus** cilok seharga Rp 5.000!")

# ==========================================
# TAB 2: DISKON GANDA (Miskonsepsi)
# ==========================================
with tab2:
    st.header("Misteri Diskon Bertingkat (50% + 20%)")
    st.markdown("""
    Banyak orang berpikir **Diskon 50% + 20%** itu sama dengan **Diskon 70%**. 
    **Itu SALAH!** ❌ Mari kita buktikan kenapa.
    """)
    
    harga_barang_ganda = st.number_input("Harga Awal Barang", value=200000, step=10000, key="ganda_input")
    
    col_kiri, col_kanan = st.columns(2)
    
    # Skenario SALAH
    with col_kiri:
        st.error("❌ Cara Berpikir Salah (50+20 = 70%)")
        diskon_salah = 70
        hemat_salah = harga_barang_ganda * (diskon_salah/100)
        bayar_salah = harga_barang_ganda - hemat_salah
        
        st.metric("Diskon Dianggap", "70%")
        st.metric("Harga Akhir (Salah)", format_rupiah(bayar_salah))
        
    # Skenario BENAR
    with col_kanan:
        st.success("✅ Cara Hitung Benar (Bertingkat)")
        
        # Tahap 1
        st.write("1️⃣ **Diskon Pertama (50%)**")
        hemat_1 = harga_barang_ganda * 0.5
        harga_sisa_1 = harga_barang_ganda - hemat_1
        st.write(f"Harga menjadi: {format_rupiah(harga_sisa_1)}")
        
        # Tahap 2
        st.write("2️⃣ **Diskon Kedua (20% dari sisa)**")
        st.caption("Diskon 20% diambil dari harga sisa, bukan harga awal!")
        hemat_2 = harga_sisa_1 * 0.2
        harga_final = harga_sisa_1 - hemat_2
        
        total_diskon_persen = ((harga_barang_ganda - harga_final) / harga_barang_ganda) * 100
        
        st.metric("Total Diskon Asli", f"{total_diskon_persen:.0f}%")
        st.metric("Harga Akhir (Benar)", format_rupiah(harga_final))

    st.warning(f"**Kesimpulan:** Toko memberi diskon total **{total_diskon_persen:.0f}%**, bukan 70%. Selisih harganya adalah **{format_rupiah(bayar_salah - harga_final)}**.")

# ==========================================
# TAB 3: KUIS TANTANGAN
# ==========================================
with tab3:
    st.header("🛒 Tantangan Kasir Cilik")
    
    if 'score_shop' not in st.session_state:
        st.session_state.score_shop = 0
        st.session_state.quiz_price = 50000
        st.session_state.quiz_disc = 10
    
    st.metric("Skor Kasir", f"{st.session_state.score_shop} 🌟")
    
    st.markdown(f"""
    ### Soal:
    Sebuah baju harganya **{format_rupiah(st.session_state.quiz_price)}**. 
    Hari ini ada diskon **{st.session_state.quiz_disc}%**.
    Berapa harga yang harus dibayar pelanggan?
    """)
    
    jawaban_user = st.number_input("Masukkan jawabanmu (Rp):", min_value=0, step=1000, key="jawaban_kuis")
    
    if st.button("Cek Jawaban"):
        hemat_kuis = st.session_state.quiz_price * (st.session_state.quiz_disc / 100)
        kunci_jawaban = st.session_state.quiz_price - hemat_kuis
        
        if jawaban_user == kunci_jawaban:
            st.balloons()
            st.success(f"🎉 Benar! Harganya {format_rupiah(kunci_jawaban)}")
            st.session_state.score_shop += 10
        else:
            st.error(f"❌ Kurang tepat. Yang benar adalah {format_rupiah(kunci_jawaban)}")
            
    st.markdown("---")
    if st.button("Soal Berikutnya ➡️"):
        # Randomize soal baru
        st.session_state.quiz_price = random.choice([20000, 50000, 75000, 100000, 150000, 200000])
        st.session_state.quiz_disc = random.choice([10, 20, 25, 50, 75])
        st.rerun()
