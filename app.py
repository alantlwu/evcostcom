import streamlit as st

# 計算年度成本的函數
def calculate_annual_cost(mileage, cost_per_km, maintenance_cost, tax):
    return mileage * cost_per_km + maintenance_cost + tax

# 根據排氣量返回稅金
def get_gasoline_tax_and_fuel(cc):
    tax_table = [
        (500, 1620, 2160),
        (600, 2160, 2880),
        (1200, 4320, 4320),
        (1800, 7120, 4800),
        (2400, 11230, 6180),
        (3000, 15210, 7200),
        (3600, 28220, 8640),
        (4200, 28220, 9810),
        (4800, 46170, 11220),
        (5400, 46170, 12180),
        (6000, 69690, 13080),
        (6600, 69690, 13950),
        (7200, 111700, 14910),
        (7800, 111700, 15720),
        (float('inf'), 151200, 15720),
    ]
    for limit, tax, fuel_fee in tax_table:
        if cc <= limit:
            return tax, fuel_fee, tax + fuel_fee

# Streamlit 網頁介面
st.title("車輛持有成本比較")

# 共用輸入部分
mileage = st.number_input("每年行駛里程（公里）", min_value=1, value=10000)
st.caption("汽油車每公里以3元計算，電動車每公里以0.4元計算")

# 汽油車部分
st.header("汽油車資料")
cc = st.selectbox("選擇排氣量（c.c.）", [500, 600, 1200, 1800, 2400, 3000, 3600, 4200, 4800, 5400, 6000, 6600, 7200, 7800])
gas_tax, gas_fuel_fee, gas_total_tax_and_fuel = get_gasoline_tax_and_fuel(cc)
st.write(f"稅金總計：${gas_total_tax_and_fuel}")
gas_maintenance_cost = st.number_input("每年保養費用（$）", min_value=0, value=5000)

# 電動車部分
st.header("電動車資料")
ev_maintenance_cost = 2000  # 固定保養費用
st.write(f"每年保養費用：${ev_maintenance_cost}（雨刷，雨刷水，冷氣濾芯）")
ev_tax = 0  # 固定稅金成本
st.write(f"每年稅金成本：${ev_tax}")

# 持有年數
years = st.number_input("持有年數", min_value=1, value=5)

# 計算成本
if st.button("計算成本"):
    # 汽油車總成本
    gas_annual_cost = calculate_annual_cost(mileage, 3.0, gas_maintenance_cost, gas_total_tax_and_fuel)
    gas_total_cost = gas_annual_cost * years

    # 電動車總成本
    ev_annual_cost = calculate_annual_cost(mileage, 0.4, ev_maintenance_cost, ev_tax)
    ev_total_cost = ev_annual_cost * years

    # 成本差額
    total_savings = gas_total_cost - ev_total_cost
    monthly_savings = total_savings / (years * 12)
    annual_savings = total_savings / years

    # 顯示結果
    st.subheader("持有成本結果")
    st.write(f"汽油車總成本：${int(gas_total_cost)}")
    st.write(f"電動車總成本：${int(ev_total_cost)}")
    st.write(f"每月可省下：${int(monthly_savings)}")
    st.write(f"每年可省下：${int(annual_savings)}")
    st.write(f"持有成本差額：${int(total_savings)}")