
import streamlit as st

st.set_page_config(page_title="T-Account System", layout="wide")

# Session state init
if 'agent_a_assets' not in st.session_state:
    st.session_state.agent_a_assets = []
    st.session_state.agent_a_liabilities = []
    st.session_state.agent_b_assets = []
    st.session_state.agent_b_liabilities = []
    st.session_state.agent_a_name = "Agent A"
    st.session_state.agent_b_name = "Agent B"

def parse_amount(text):
    try:
        return float(text.strip())
    except:
        return None

def reset_all():
    st.session_state.agent_a_assets.clear()
    st.session_state.agent_a_liabilities.clear()
    st.session_state.agent_b_assets.clear()
    st.session_state.agent_b_liabilities.clear()

def add_entry(store, amount_text, name_text, default_label):
    amount = parse_amount(amount_text)
    name = name_text.strip() if name_text.strip() else default_label
    if amount is not None:
        store.append((amount, name))

def format_entry(entry):
    amount, name = entry
    return f"{amount:+.2f} {name}"

# Agent name inputs
col1, col2 = st.columns(2)
with col1:
    st.session_state.agent_a_name = st.text_input("Agent A Name", st.session_state.agent_a_name)
with col2:
    st.session_state.agent_b_name = st.text_input("Agent B Name", st.session_state.agent_b_name)

st.markdown("## Add Entries")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### {st.session_state.agent_a_name}")
    a_asset_amt = st.text_input("Asset Amount (A)", key="a_asset_amt")
    a_asset_name = st.text_input("Asset Name (A)", key="a_asset_name")
    if st.button("Add Asset A"):
        add_entry(st.session_state.agent_a_assets, a_asset_amt, a_asset_name, "Unnamed Asset")
    a_liab_amt = st.text_input("Liability Amount (A)", key="a_liab_amt")
    a_liab_name = st.text_input("Liability Name (A)", key="a_liab_name")
    if st.button("Add Liability A"):
        add_entry(st.session_state.agent_a_liabilities, a_liab_amt, a_liab_name, "Unnamed Liability")

with col2:
    st.markdown(f"#### {st.session_state.agent_b_name}")
    b_asset_amt = st.text_input("Asset Amount (B)", key="b_asset_amt")
    b_asset_name = st.text_input("Asset Name (B)", key="b_asset_name")
    if st.button("Add Asset B"):
        add_entry(st.session_state.agent_b_assets, b_asset_amt, b_asset_name, "Unnamed Asset")
    b_liab_amt = st.text_input("Liability Amount (B)", key="b_liab_amt")
    b_liab_name = st.text_input("Liability Name (B)", key="b_liab_name")
    if st.button("Add Liability B"):
        add_entry(st.session_state.agent_b_liabilities, b_liab_amt, b_liab_name, "Unnamed Liability")

if st.button("Reset All"):
    reset_all()

st.markdown("---")
st.markdown("## T-Accounts")

# Display table
def sum_side(entries): return sum(x[0] for x in entries)

a_assets = st.session_state.agent_a_assets
a_liabs = st.session_state.agent_a_liabilities
b_assets = st.session_state.agent_b_assets
b_liabs = st.session_state.agent_b_liabilities

max_len = max(len(a_assets), len(a_liabs), len(b_assets), len(b_liabs), 1)

headers = f"| Idx | {st.session_state.agent_a_name} Assets | {st.session_state.agent_a_name} Liabilities | {st.session_state.agent_b_name} Assets | {st.session_state.agent_b_name} Liabilities |"
st.markdown(headers)
st.markdown("|-----|---------------------|-------------------------|----------------------|---------------------------|")

for i in range(max_len):
    a_asset = format_entry(a_assets[i]) if i < len(a_assets) else ""
    a_liab = format_entry(a_liabs[i]) if i < len(a_liabs) else ""
    b_asset = format_entry(b_assets[i]) if i < len(b_assets) else ""
    b_liab = format_entry(b_liabs[i]) if i < len(b_liabs) else ""
    st.markdown(f"| {i} | {a_asset} | {a_liab} | {b_asset} | {b_liab} |")

ta_assets = sum_side(a_assets)
ta_liabs = sum_side(a_liabs)
tb_assets = sum_side(b_assets)
tb_liabs = sum_side(b_liabs)

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**{st.session_state.agent_a_name}**: Assets = {ta_assets:.2f}, Liabilities = {ta_liabs:.2f}")
    st.markdown("✅ Balanced" if ta_assets == ta_liabs else "❌ Not Balanced")
with col2:
    st.markdown(f"**{st.session_state.agent_b_name}**: Assets = {tb_assets:.2f}, Liabilities = {tb_liabs:.2f}")
    st.markdown("✅ Balanced" if tb_assets == tb_liabs else "❌ Not Balanced")
with col3:
    total_assets = ta_assets + tb_assets
    total_liabs = ta_liabs + tb_liabs
    st.markdown(f"**System**: Assets = {total_assets:.2f}, Liabilities = {total_liabs:.2f}")
    st.markdown("✅ System Balanced" if total_assets == total_liabs else "❌ System Not Balanced")
