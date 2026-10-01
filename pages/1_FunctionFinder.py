# page that allows users to mess around with the function parameters

import streamlit as st
from utils.function import sigmoidal_plot as sig

st.title("Sigmoidal Function Plotter")

st.write("""
### Equation

The sigmoidal current ramp is defined as:""")

st.write(r"""

$i(t) = \frac{A}{1 + e^{-k(t - t_0)}} + B$

Where:

- i is current in **µA**
- t is time in **minutes**

Use the sliders below to input the function parameters. The graph will automatically update. For more information on how these parameters change the plot, see the *Math Help Page*.
""")

#adding user inputs

st.header("Parameters")

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
    


# making plot
st.header("Electrochemical Ramp")

obj = sig(use_initial, start_val, A, k, t0, use_cutoff, end_val)
fig = obj.plotting()
st.pyplot(fig)	