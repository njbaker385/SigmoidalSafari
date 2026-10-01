# page that uses time to generate squidstat file

import streamlit as st
from utils.function import sigmoidal_plot as sig
from utils.squidstat_maker import squid


st.title("Sigmoidal Current Ramp Maker")

st.header("Sigmoidal Current Ramp Maker")
st.write("Use this page to generate the squidstat file.")

use_initial = st.toggle("Use initial current density instead of B")
use_cutoff = st.toggle("Use charge passed instead of time")

A = st.slider("A (µA)", 0.0, 100.0, 25.0)
k = st.slider("k", 0.001, 5.0, 2.0)
t0 = st.slider("t₀ (min)", 0.0, 10.0, 2.0)

if use_initial:
	start_val = st.number_input("Initial Current Density (µA)", value=-30.0)
	
else:
	start_val = st.number_input("B Value (µA)", value=-30.0)


if use_cutoff:
	end_val = st.number_input("Final Charge Passed (mC)", value=3.0)
	
else:
	end_val = st.number_input("Final Time (min)", 1.0, 30.0, 5.0)

n = st.slider("Number of Linear Sweeps", 10,100,50,1)
name = st.text_input("Enter Experiment Title")


obj_plot = sig(use_initial, start_val, A, k, t0, use_cutoff, end_val)
obj_exp_mkr = squid(obj_plot.A, obj_plot.B,obj_plot.k, obj_plot.t0, obj_plot.tf, n, name) 

fig = obj_exp_mkr.plotting()

# making plot
st.header("Electrochemical Ramp")
st.pyplot(fig)


# When Calculate is pressed, generate files and store them
if st.button("Calculate"):
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



