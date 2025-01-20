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
st.caption("汽油車每公里以實際油耗計算，電動車每公里以0.4元計算")

# 汽油車部分
st.header("汽油車資料")
cc_range = st.selectbox("選擇排氣量區間（c.c.）", ["500以下", "500~600", "600~1200", "1200~1800", "1800~2400", "2400~3000", "3000~3600", "3600~4200", "4200~4800", "4800~5400", "5400~6000", "6000~6600", "6600~7200", "7200~7800", "7800以上"])

# 將區間轉換為最大排氣量
cc_limits = {
    "500以下": 500,
    "500~600": 600,
    "600~1200": 1200,
    "1200~1800": 1800,
    "1800~2400": 2400,
    "2400~3000": 3000,
    "3000~3600": 3600,
    "3600~4200": 4200,
    "4200~4800": 4800,
    "4800~5400": 5400,
    "5400~6000": 6000,
    "6000~6600": 6600,
    "6600~7200": 7200,
    "7200~7800": 7800,
    "7800以上": float('inf'),
}
cc = cc_limits[cc_range]
gas_tax, gas_fuel_fee, gas_total_tax_and_fuel = get_gasoline_tax_and_fuel(cc)
st.write(f"稅金總計：${gas_total_tax_and_fuel}")
gas_maintenance_cost = st.number_input("每年保養費用（$）", min_value=0, value=5000)

# 新增汽油規格與油價
fuel_type = st.selectbox("選擇汽油規格", ["92無鉛汽油", "95無鉛汽油", "98無鉛汽油"])
fuel_prices = {"92無鉛汽油": 29.19, "95無鉛汽油": 30.69, "98無鉛汽油": 32.69}
fuel_price = fuel_prices[fuel_type]
st.write(f"目前選擇的汽油價格：${fuel_price} 每公升")
st.write(f"資料參考經濟部能源署2024年對全台加油站油價抽樣採集之平均")

# 新增平均油耗輸入
gas_fuel_efficiency = st.number_input("汽油車平均油耗（1公升/公里）", min_value=0.1, value=12.0)

# 電動車部分
st.header("電動車資料")
ev_maintenance_cost = 2000  # 固定保養費用
st.write(f"每年保養費用：${ev_maintenance_cost}（雨刷，雨刷水，冷氣濾芯）")
ev_tax = 0  # 固定稅金成本
st.write(f"每年稅金成本：${ev_tax}")
st.write(f"電價資料參考台灣電力公司2024年發佈的台灣平均電價統計資料")

# 持有年數
years = st.number_input("持有年數", min_value=1, value=5)

# 計算成本
if st.button("計算成本"):
    # 汽油車總成本
    gas_cost_per_km = fuel_price / gas_fuel_efficiency
    gas_annual_cost = calculate_annual_cost(mileage, gas_cost_per_km, gas_maintenance_cost, gas_total_tax_and_fuel)
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

    # 新增敘述
    st.subheader("成本分析")
    st.write(f"相比傳統燃油汽車，電動車的燃料費用較為便宜。以平均每年行駛約 {mileage} 公里計算，")
    st.write(f"一年的汽油開支約為${int(mileage * gas_cost_per_km)}。相較之下，電動車行駛同等里數所耗電力只需其約六分之一的費用。")
    st.write(f"以車輛持有 {years} 年換車周期計算，一共可節省約${int(total_savings)}。\n\n")
    st.write(f"*我們假設同等級燃油車每1公升汽油可行駛 {gas_fuel_efficiency} 公里。")
    st.write(f"*我們假設平均每千瓦小時的住宅電費為\$2.8，以及汽油價格為每公升\${fuel_price}。")

    st.write(f"油價參考:https://www2.moeaea.gov.tw/oil111/Gasoline/NationwideAvg")
    st.write(f"電價參考:https://www.taipower.com.tw/2289/2363/2388/2389/10734/normalPost")
