import streamlit as st

st.set_page_config(page_title="T-Account System", layout="wide")

# Initialize session state
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

def format_entry(i, entry):
    amount, name = entry
    return f"[{i}] {amount:+.2f}  {name}"

# Agent naming
st.markdown("### Name the agents")
col1, col2 = st.columns(2)
with col1:
    st.session_state.agent_a_name = st.text_input("Agent A Name", st.session_state.agent_a_name)
with col2:
    st.session_state.agent_b_name = st.text_input("Agent B Name", st.session_state.agent_b_name)

# Add entries
st.markdown("### Add Entries")
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"#### {st.session_state.agent_a_name} Entries")
    st.text_input("Asset Amount (A)", key="a_asset_amt")
    st.text_input("Asset Name (A)", key="a_asset_name")
    if st.button("Add Asset A"):
        amt = st.session_state.get("a_asset_amt", "")
        name = st.session_state.get("a_asset_name", "")
        add_entry(st.session_state.agent_a_assets, amt, name, "Unnamed Asset")
        st.session_state["a_asset_amt"] = ""
        st.session_state["a_asset_name"] = ""
        st.experimental_rerun()

    st.text_input("Liability Amount (A)", key="a_liab_amt")
    st.text_input("Liability Name (A)", key="a_liab_name")
    if st.button("Add Liability A"):
        amt = st.session_state.get("a_liab_amt", "")
        name = st.session_state.get("a_liab_name", "")
        add_entry(st.session_state.agent_a_liabilities, amt, name, "Unnamed Liability")
        st.session_state["a_liab_amt"] = ""
        st.session_state["a_liab_name"] = ""
        st.experimental_rerun()

with col2:
    st.markdown(f"#### {st.session_state.agent_b_name} Entries")
    st.text_input("Asset Amount (B)", key="b_asset_amt")
    st.text_input("Asset Name (B)", key="b_asset_name")
    if st.button("Add Asset B"):
        amt = st.session_state.get("b_asset_amt", "")
        name = st.session_state.get("b_asset_name", "")
        add_entry(st.session_state.agent_b_assets, amt, name, "Unnamed Asset")
        st.session_state["b_asset_amt"] = ""
        st.session_state["b_asset_name"] = ""
        st.experimental_rerun()

    st.text_input("Liability Amount (B)", key="b_liab_amt")
    st.text_input("Liability Name (B)", key="b_liab_name")
    if st.button("Add Liability B"):
        amt = st.session_state.get("b_liab_amt", "")
        name = st.session_state.get("b_liab_name", "")
        add_entry(st.session_state.agent_b_liabilities, amt, name, "Unnamed Liability")
        st.session_state["b_liab_amt"] = ""
        st.session_state["b_liab_name"] = ""
        st.experimental_rerun()

if st.button("Reset All"):
    reset_all()

# Visual T-Accounts
st.markdown("---")
st.markdown("## T-Account View")

a_assets = st.session_state.agent_a_assets
a_liabs = st.session_state.agent_a_liabilities
b_assets = st.session_state.agent_b_assets
b_liabs = st.session_state.agent_b_liabilities

a_col, gap, b_col = st.columns([1.5, 0.2, 1.5])

with a_col:
    st.markdown(f"### {st.session_state.agent_a_name}")
    lcol, rcol = st.columns(2)
    with lcol:
        st.markdown("#### Assets")
        for i, entry in enumerate(a_assets):
            st.text(format_entry(i, entry))
    with rcol:
        st.markdown("#### Liabilities")
        for i, entry in enumerate(a_liabs):
            st.text(format_entry(i, entry))

with b_col:
    st.markdown(f"### {st.session_state.agent_b_name}")
    lcol, rcol = st.columns(2)
    with lcol:
        st.markdown("#### Assets")
        for i, entry in enumerate(b_assets):
            st.text(format_entry(i, entry))
    with rcol:
        st.markdown("#### Liabilities")
        for i, entry in enumerate(b_liabs):
            st.text(format_entry(i, entry))

# Balance check
def sum_entries(entries): return sum(x[0] for x in entries)

ta_assets = sum_entries(a_assets)
ta_liabs = sum_entries(a_liabs)
tb_assets = sum_entries(b_assets)
tb_liabs = sum_entries(b_liabs)
total_assets = ta_assets + tb_assets
total_liabs = ta_liabs + tb_liabs

st.markdown("---")
st.markdown("## Balance Check")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"**{st.session_state.agent_a_name}**")
    st.markdown(f"Assets: {ta_assets:.2f}")
    st.markdown(f"Liabilities: {ta_liabs:.2f}")
    st.markdown("✅ Balanced" if ta_assets == ta_liabs else "❌ Not Balanced")

with col2:
    st.markdown(f"**{st.session_state.agent_b_name}**")
    st.markdown(f"Assets: {tb_assets:.2f}")
    st.markdown(f"Liabilities: {tb_liabs:.2f}")
    st.markdown("✅ Balanced" if tb_assets == tb_liabs else "❌ Not Balanced")

with col3:
    st.markdown("**System**")
    st.markdown(f"Total Assets: {total_assets:.2f}")
    st.markdown(f"Total Liabilities: {total_liabs:.2f}")
    st.markdown("✅ System Balanced" if total_assets == total_liabs else "❌ System Not Balanced")

# Delete Entry
st.markdown("---")
st.markdown("## Delete Entry")

account_map = {
    f"{st.session_state.agent_a_name} - Assets": st.session_state.agent_a_assets,
    f"{st.session_state.agent_a_name} - Liabilities": st.session_state.agent_a_liabilities,
    f"{st.session_state.agent_b_name} - Assets": st.session_state.agent_b_assets,
    f"{st.session_state.agent_b_name} - Liabilities": st.session_state.agent_b_liabilities,
}

col1, col2 = st.columns(2)
selected_account = col1.se_
