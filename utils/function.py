# backend logic for generating sigmoidal plot from known inputs --> no time or charge limit
# will make the plot class and return a figure --> for importing into the streamlit python pagesQ

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from scipy.optimize import brentq



class sigmoidal_plot:

	def __init__(self, start_switch, start_val, A, k, t0, end_switch, end_val):
		#defining inputs within the class 
		self.A = A
		self.k = k 
		self.t0= t0

		self.B = self.B_finder(start_switch, start_val) 
		self.tf = self.finalt_finder(end_switch, end_val)
		

		#making line
		self.times = np.linspace(0,self.tf,1000)
		self.line = self.sigmoidal_function(self.times)
		self.charges = self.charge_finder(self.times)

		self.finalTime = self.times[-1]
		self.finali = self.line[-1]
		self.finalQ = self.charges[-1]
		


	def B_finder(self, switch, start):
		if not switch:
			return start #start is the B value
		else:
			#start is initial current density 
			frac = self.A/(1+np.exp(self.k*self.t0))
			return start - frac

	def finalt_finder(self, switch, val):
		
		if not switch:
			return val
		else:
			#value passed into class is mC of charge --> need to calculate time
			#think of value like the target: Going to use root finding method F(t) = Q(t) - targetQ	

			F = lambda t: self.charge_finder(t) - val
			
			return brentq(F, 0, 10*self.t0 + 10)


	def sigmoidal_function(self, t):
		exponent = -self.k*(t-self.t0)
		denom = np.exp(exponent)
		frac = self.A / (1+denom)

		return (frac + self.B)

	def charge_finder(self, tf):
		term_f = (tf - self.t0) + np.log(1 + np.exp(-self.k*(tf - self.t0)))
		term_0 = (-self.t0) + np.log(1 + np.exp(self.k*self.t0))

		return abs(((self.A/self.k)*(term_f - term_0) + self.B*tf)*0.06) #should return mC

	def plotting(self):
		fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,8))
		
		ax1.plot(self.times, self.line, linewidth=4, label = "Current", color="tab:blue")		
		ax1.set_xlabel("Time (min)", fontsize=14)
		ax1.set_ylabel("Current Density (μA)", fontsize=14)
		ax1.set_title("Sigmoidal Current Ramp", fontsize=16)
		ax1.grid(axis='x', color='grey', linestyle = "--", linewidth=0.5)
		ax1.tick_params(axis='both', which='major', labelsize=12) 
		ax1.legend(title=f"A = {self.A} \nB = {self.B:.4f} \nk = {self.k} \nt0 = {self.t0} \nFinal Time = {self.finalTime:.4f}min \nFinal Current = {self.finali:.4f}μA", title_fontsize=14, fontsize=12)

		ax2.plot(self.times, self.charges, linewidth=4, label="Charge", color="tab:red")		
		ax2.set_xlabel("Time (min)", fontsize=14)
		ax2.set_ylabel("Charge Passed (mC)", fontsize=14)
		ax2.set_title("Sigmoidal Current Ramp - Charge Passed", fontsize=16)
		ax2.grid(axis='x', color='grey', linestyle = "--", linewidth=0.5)
		ax2.tick_params(axis='both', which='major', labelsize=12) 
		ax2.legend(title=f"Final Q passed = {self.finalQ:.4f} mC", title_fontsize=14, fontsize=12)

		return fig 