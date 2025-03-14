import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analisis E-Commerce", layout="wide")
st.title("Dashboard Analisis E-Commerce")


DATA_PATH = "https://raw.githubusercontent.com/fiendess/dicoding-ecommerce-analysis/main/dashboard/all_data.csv"
merged_data = pd.read_csv(DATA_PATH)
merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])

st.sidebar.header("Filter Data")
selected_city = st.sidebar.selectbox("Pilih Kota", merged_data['customer_city'].unique(), index=0)
selected_year = st.sidebar.selectbox("Pilih Tahun", merged_data['order_purchase_timestamp'].dt.year.unique(), index=0)
selected_category = st.sidebar.selectbox("Pilih Kategori Produk", merged_data['product_category_name'].dropna().unique(), index=0)

filtered_data = merged_data[
    (merged_data['customer_city'] == selected_city) &
    (merged_data['order_purchase_timestamp'].dt.year == selected_year) &
    (merged_data['product_category_name'] == selected_category)
]

jumlah_pelanggan = filtered_data['customer_id'].nunique()
order_status_counts = filtered_data['order_status'].value_counts()
order_delivered = order_status_counts.get('delivered', 0)
order_cancelled = order_status_counts.get('canceled', 0)
order_shipped = order_status_counts.get('shipped', 0)


st.metric("Total Pelanggan di Kota " + selected_city, merged_data[merged_data['customer_city'] == selected_city]['customer_id'].nunique())

if jumlah_pelanggan > 0:
    st.metric("Pelanggan yang Membeli " + selected_category + " pada Tahun " + str(selected_year), jumlah_pelanggan)
    st.metric("Pesanan Terkirim", order_delivered)
    st.metric("Pesanan Dibatalkan", order_cancelled)
    st.metric("Pesanan dalam Proses Pengiriman", order_shipped)
else:
    st.warning(f"Tidak ada pelanggan yang membeli '{selected_category}' di '{selected_city}' pada tahun {selected_year}.")

st.subheader("Analisis Data")

# Distribusi Pelanggan berdasarkan Kota dan Kategori Produk
if jumlah_pelanggan > 0:
    labels = ['Total Pelanggan ' + selected_city, 'Pelanggan yang Membeli ' + selected_category]
    values = [merged_data[merged_data['customer_city'] == selected_city]['customer_id'].nunique(), jumlah_pelanggan]
    colors = ['lightblue', 'lightcoral']

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=labels, y=values, palette=colors, edgecolor='black', ax=ax)

    for i, v in enumerate(values):
        ax.text(i, v + 5, str(v), ha='center', fontsize=12, fontweight='bold')

    ax.set_title("Jumlah Pelanggan yang Membeli Produk " + selected_category + " (Tahun " + str(selected_year) + ")", fontsize=13, fontweight='bold')
    ax.set_ylabel("Jumlah Pelanggan", fontsize=11)
    ax.set_xticklabels(labels, fontsize=10)

    st.pyplot(fig)


    # Status Pengiriman Pesanan
    order_status_labels = ['Delivered', 'Shipped', 'Cancelled']
    order_status_values = [order_delivered, order_shipped, order_cancelled]
    colors_status = ['green', 'blue', 'red']

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(x=order_status_labels, y=order_status_values, palette=colors_status, edgecolor='black', ax=ax2)

    for i, v in enumerate(order_status_values):
        ax2.text(i, v + 5, str(v), ha='center', fontsize=12, fontweight='bold')

    ax2.set_title("Status Pengiriman Pesanan " + selected_category + " (Tahun " + str(selected_year) + ")", fontsize=13, fontweight='bold')
    ax2.set_ylabel("Jumlah Pesanan", fontsize=11)

    st.pyplot(fig2)


    # Distribusi waktu pembelian
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_data['order_purchase_timestamp'], bins=30, kde=True, color='purple', ax=ax3)

    ax3.set_title("Distribusi Waktu Pembelian " + selected_category + " (Tahun " + str(selected_year) + ")", fontsize=13, fontweight='bold')
    ax3.set_ylabel("Jumlah Pembelian", fontsize=11)
    ax3.set_xlabel("Tanggal Pembelian", fontsize=11)
    plt.xticks(rotation=45)

    st.pyplot(fig3)
else:
    st.warning("Tidak ada data yang tersedia untuk visualisasi berdasarkan filter yang dipilih.")
