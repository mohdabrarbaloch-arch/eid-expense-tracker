import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="🎉 Eid Expense Tracker Ultimate",
    page_icon="🌙",
    layout="centered"
)

# ---- HEADER WITH EID THEME ----
st.markdown("""
<div style="
    background: linear-gradient(to right, #FFD700, #32CD32); 
    padding: 20px; 
    border-radius: 15px; 
    text-align:center;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
">
<h1 style="color:#FF4500; font-family: 'Comic Sans MS', cursive;">🌙 Eid Expense Tracker 🎊</h1>
<p style="color:#228B22; font-size:18px; font-family: 'Comic Sans MS', cursive;">
Track your Eid spending with fun & style! 🎁✨
</p>
</div>
""", unsafe_allow_html=True)

# ---- FLOATING STARS / EID BACKGROUND ----
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #FFF8DC, #FFE4B5);
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)

# ---- SESSION STATE ----
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

# ---- BUDGET INPUT ----
st.subheader("💵 Set Your Eid Budget")
budget = st.number_input("Enter total Eid Budget:", min_value=0, step=100, help="Example: 5000")

# ---- ADD EXPENSE FORM ----
with st.expander("➕ Add Eid Expense 🎁"):
    category = st.text_input("Category (Clothes, Food, Eidi)")
    amount = st.number_input("Amount Spent:", min_value=0, step=50)
    description = st.text_input("Description (Optional)")
    if st.button("Add Expense 🌙"):
        new_entry = pd.DataFrame([[
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            category.title(),
            amount,
            description
        ]], columns=["Date", "Category", "Amount", "Description"])
        st.session_state.data = pd.concat([st.session_state.data, new_entry], ignore_index=True)
        st.balloons()  # Confetti celebration 🎉
        st.success("🎊 Expense Added! Eid Mubarak 🌙✨")

# ---- TOTALS & STATUS ----
total = st.session_state.data["Amount"].sum() if not st.session_state.data.empty else 0
percent = int((total / budget) * 100) if budget > 0 else 0

st.subheader("💸 Eid Spending Summary")
st.progress(percent)
st.write(f"**Total Spent:** {total} 💰")
st.write(f"**Budget:** {budget} 🌙")
if budget > 0 and total > budget:
    st.error(f"🚨 Budget Exceeded by {total-budget}! 🎇🎆")
else:
    st.success(f"✅ Within budget ({percent}% used) ✨")

# ---- TOP 3 EXPENSES ----
if not st.session_state.data.empty:
    st.subheader("🏆 Top 3 Eid Expenses 🎁")
    top3 = st.session_state.data.sort_values(by="Amount", ascending=False).head(3)
    st.table(top3[["Date","Category","Amount","Description"]])

# ---- 3D CATEGORY CHART ----
if not st.session_state.data.empty:
    st.subheader("📊 3D Spending by Category")
    chart_data = st.session_state.data.groupby("Category")["Amount"].sum().reset_index()
    fig = px.bar(
        chart_data, x="Category", y="Amount", color="Category",
        text="Amount", title="🎉 Eid Spending 3D",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig.update_traces(marker_line_width=1.5, marker_line_color="black", textposition='outside')
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.1)')
    st.plotly_chart(fig, use_container_width=True)

# ---- FUN QUOTE ----
st.markdown("<h3 style='text-align:center; color:#FF69B4;'>“Eid Mubarak! 🎁 Spend wisely & enjoy 🌟”</h3>", unsafe_allow_html=True)
