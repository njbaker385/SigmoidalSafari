#main python file --> essentially the home page

import streamlit as st


st.sidebar.title("Home Page")
st.sidebar.write("Choose a page to begin.")

st.title("Nick's Sigmoidal Safari")

st.write("""
This website can be used to generate sigmoidal current ramps for that can be run on the Squidstat&trade; potentiostats. 

### General Workflow 

1. Use the "FunctionFinder" page to find the parameters that you wish to use for the current ramp.
2. Take those values and then use the "ExperimentMaker" to cut off your ramp at either a specific time or amount of charge passed. Then simply download the files onto your computer. 
3. Open up the files inside of the squidstat software and resave them to a new name. 

   - Squidstat uses some sort of internal naming scheme that prevents manually generated JSON files from being named normally. Load the generated ramps **one at a time** into your "custom experiments" folder inside the "Admiral Instruments" folder on your computer. Open them inside the software, rename, then delete the original experiment and move the new experiment to a jumpdrive for transfer to the lab computer. 

""")
