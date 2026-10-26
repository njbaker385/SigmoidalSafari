# page that uses time to generate squidstat file

import streamlit as st
from utils.function import sigmoidal_plot as sig
from utils.squidstat_maker import squid


st.title("Sigmoidal Current Ramp Maker")

st.header("Sigmoidal Current Ramp Maker")
st.write("Use this page to generate the squidstat file.")

use_cutoff = st.toggle("Use charge passed instead of time")
name = st.text_input("Enter Experiment Title")
k = st.number_input("k", value = 3.3, step=1e-6, format="%.6f")
t0 = st.number_input("t₀ (min)",value =  1.4, step=1e-6, format="%.6f")
start_current = st.number_input("Initial Current Density (µA)", value=-30.0,
                                step=1e-6, format="%.6f")
end_current = st.number_input("Final Current Density - Asymptote (µA)", value=-5.0,
                              step=1e-6, format="%.6f")

if use_cutoff:
	end_val = st.number_input("Final Charge Passed (mC)", value=3.0,
                              step=1e-6, format="%.6f")
	
else:
	end_val = st.number_input("Final Time (min)", value = 5.0,
                              step=1e-6, format="%.6f")

n = st.number_input("Number of Intended Linear Sweeps", value = 35)



obj_plot = sig(start_current, end_current, k, t0, use_cutoff, end_val)
obj_exp_mkr = squid(obj_plot.A, obj_plot.B, obj_plot.t0, obj_plot.k, obj_plot.tf, int(n), name) 


fig = obj_exp_mkr.plotting()

# making plot
st.header("Electrochemical Ramp")
st.pyplot(fig)


# When Calculate is pressed, generate files and store them
if st.button("Calculate"):
    #print(f"A = {obj_plot.A} \n B = {obj_plot.B} \n t0 = {obj_plot.t0} \n k = {obj_plot.k} \n tf = {obj_plot.tf}")

    df = obj_exp_mkr.making_csv()
    st.session_state["csv_bytes"] = df.to_csv(index=False).encode("utf-8")
    st.session_state["json_file"] = obj_exp_mkr.making_json()
    st.session_state["name"] = name
    st.success("Files Generated...")


# If files exist in session_state, show download buttons
if "csv_bytes" in st.session_state and "json_file" in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Download csv file",
            data=st.session_state["csv_bytes"],
            file_name=f"{st.session_state['name']}_linear_sweep_points.csv",
            mime="text/csv")
    with col2:
        st.download_button(
            label="Download Squidstat File",
            data=st.session_state["json_file"],
            file_name=f"{st.session_state['name']}_SquidStatExp.json",
            mime="application/json")



