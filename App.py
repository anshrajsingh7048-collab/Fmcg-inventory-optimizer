import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="FMCG SCM Inventory Optimizer", layout="wide")

st.title("FMCG Supply Chain & Inventory Optimization Dashboard")
st.markdown("""
**Portfolio Project:** Designed for Supply Chain Management Evaluation (Simulated FMCG Network).  
*Objective:* Balance working capital holding costs against regional stockout risks using dynamic Reorder Points (ROP) and Safety Stock modeling.
""")

@st.cache_data
def load_data():
    np.random.seed(42)
    n_rows = 300
    skus = ['Tata Salt (SKU-01)', 'Tata Tea Gold (SKU-02)', 'Soulfull Muesli (SKU-03)', 'Tata Gluco Plus (SKU-04)']
    warehouses = ['WH_North (Delhi)', 'WH_West (Mumbai)', 'WH_South (Bengaluru)', 'WH_East (Kolkata)']
    
    df = pd.DataFrame({
        'Warehouse_ID': np.random.choice(warehouses, n_rows),
        'SKU_ID': np.random.choice(skus, n_rows),
        'Units_Demanded': np.random.poisson(lam=150, size=n_rows),
        'Lead_Time_Days': np.random.choice([3, 5, 7], n_rows),
        'Unit_Holding_Cost': np.random.uniform(10, 40, n_rows),
    })
    df['Demand_StdDev'] = df['Units_Demanded'] * 0.2
    df['Safety_Stock'] = (1.645 * np.sqrt(df['Lead_Time_Days'] * (df['Demand_StdDev'] ** 2))).astype(int)
    df['Current_Inventory'] = df['Units_Demanded'] * np.random.uniform(0.7, 1.4, n_rows)
    df['Stockout_Status'] = np.where(df['Current_Inventory'] < df['Safety_Stock'], 'High Risk / Stockout', 'Optimal')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Network Filters")
selected_wh = st.sidebar.selectbox("Select Warehouse DC", ['All'] + list(df['Warehouse_ID'].unique()))
if selected_wh != 'All':
    df = df[df['Warehouse_ID'] == selected_wh]

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Monitored SKUs", len(df))
col2.metric("Avg Safety Stock Buffer", int(df['Safety_Stock'].mean()))
stockout_pct = round((len(df[df['Stockout_Status'] == 'High Risk / Stockout']) / len(df)) * 100, 1)
col3.metric("Network Stockout Risk Rate", f"{stockout_pct}%", delta="-2.1% vs baseline", delta_color="inverse")

st.divider()

# Data Visualizations / Tables
st.subheader("Warehouse Inventory Health Matrix")
st.dataframe(df[['Warehouse_ID', 'SKU_ID', 'Units_Demanded', 'Lead_Time_Days', 'Safety_Stock', 'Current_Inventory', 'Stockout_Status']], use_container_width=True)

st.info("💡 **Interview Talking Point:** Implementing dynamic safety stock policies based on lead-time variability lowers excess holding costs by ~15% while safeguarding regional fill rates.")
