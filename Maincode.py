import streamlit as st
import math

# --- Page Configuration ---
st.set_page_config(
    page_title="Pipe & Cistern Calculator",
    page_icon="🚰",
    layout="wide"
)

# --- App Title and Description ---
st.title("🚰 Pipe and Cistern Calculator")
st.markdown("""
This app helps you solve classic pipe and cistern problems. You define the time each pipe takes to fill or empty the tank, and the app calculates the rest.

- **Tank Capacity:** Calculated as the Least Common Multiple (LCM) of the times taken by each pipe. This ensures that efficiencies are whole numbers.
- **Pipe Efficiency:** The rate at which a pipe works. It's positive for an **inlet** (fills water) and negative for an **outlet** (removes water).
""")
st.latex(r"\text{Efficiency} = \frac{\text{Total Capacity}}{\text{Time Taken}}")

st.divider()

# --- User Inputs ---
st.header("Pipe Configuration")
st.write("Enter the details for each of the three pipes.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Pipe A")
    type_a = st.radio("Type A", ["Inlet", "Outlet"], key="a_type", horizontal=True)
    time_a = st.number_input("Time taken by Pipe A (hours)", min_value=1, value=10, step=1, key="a_time")

with col2:
    st.subheader("Pipe B")
    type_b = st.radio("Type B", ["Inlet", "Outlet"], key="b_type", horizontal=True)
    time_b = st.number_input("Time taken by Pipe B (hours)", min_value=1, value=12, step=1, key="b_time")

with col3:
    st.subheader("Pipe C")
    type_c = st.radio("Type C", ["Inlet", "Outlet"], key="c_type", horizontal=True)
    time_c = st.number_input("Time taken by Pipe C (hours)", min_value=1, value=15, step=1, key="c_time")

st.divider()

# --- Calculation and Display ---
if st.button("Calculate Results", type="primary", use_container_width=True):
    
    # 1. Calculate Tank Capacity (LCM of times)
    capacity = math.lcm(time_a, time_b, time_c)
    
    # 2. Calculate Individual Efficiencies
    eff_a_base = capacity // time_a
    eff_b_base = capacity // time_b
    eff_c_base = capacity // time_c
    
    # Adjust efficiency based on pipe type (inlet/outlet)
    eff_a = eff_a_base if type_a == "Inlet" else -eff_a_base
    eff_b = eff_b_base if type_b == "Inlet" else -eff_b_base
    eff_c = eff_c_base if type_c == "Inlet" else -eff_c_base
    
    # 3. Calculate Combined Efficiency
    total_efficiency = eff_a + eff_b + eff_c

    # --- Display Results ---
    st.header("📊 Calculated Results")
    
    # Display Tank Capacity
    st.metric(label="Total Tank Capacity (Units)", value=f"{capacity}")
    st.info(f"The capacity is the LCM of the input times ({time_a}, {time_b}, {time_c}) to ensure efficiencies are integers.")

    # Display Individual Pipe Efficiencies
    res_col1, res_col2, res_col3 = st.columns(3)
    with res_col1:
        st.metric(label="Pipe A Efficiency (Units/hr)", value=f"{eff_a}", 
                  delta="Fills" if eff_a > 0 else "Empties")
    with res_col2:
        st.metric(label="Pipe B Efficiency (Units/hr)", value=f"{eff_b}", 
                  delta="Fills" if eff_b > 0 else "Empties")
    with res_col3:
        st.metric(label="Pipe C Efficiency (Units/hr)", value=f"{eff_c}", 
                  delta="Fills" if eff_c > 0 else "Empties")

    st.divider()

    # --- Display Combined Performance ---
    st.subheader("Combined Performance")
    
    if total_efficiency == 0:
        st.warning("The combined efficiency is 0. The water level in the tank will not change when all pipes are open.")
    else:
        time_to_complete = abs(capacity / total_efficiency)
        
        if total_efficiency > 0:
            st.success(f"Combined efficiency is **{total_efficiency} units/hour**. The tank will **fill**.")
            st.metric(label="Time to Fill the Tank (All Pipes Open)", value=f"{time_to_complete:.2f} hours")
        else: # total_efficiency < 0
            st.error(f"Combined efficiency is **{total_efficiency} units/hour**. The tank will **empty**.")
            st.metric(label="Time to Empty the Tank (All Pipes Open)", value=f"{time_to_complete:.2f} hours")
