# backend logic for if we are using time to stop the sigmoidal current ramp
# will generate data object and have methods for different things like generating files 
# will use function python class to feed in the parameters and final time 

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import random, json, string


class squid:

	def __init__(self,A,B,t0,k,tf,n,name): #n passed in as integer
		self.A, self.B, self.t0, self.k, self.tf = A,B,t0,k,tf 
		self.n = n # number of linear sweeps used in the experiment
		self.name = name # used for file titles later

		self.slope_threshold = 0.015#µA/sec

		#making lists for the calculated values
		self.time_points = np.linspace(0,self.tf,self.n)
		self.current_points = [self.ramp(t) for t in self.time_points]

		self.making_linear_sweeps()
		
		self.charges = [0]
		for i in range(len(self.actual_time_points)-1):
			q = self.trap_charge(self.actual_time_points[i],
			                     self.actual_current_points[i],
			                     self.actual_time_points[i+1],
								 self.actual_current_points[i+1])

			self.charges.append(q)

		self.cummcharges = np.cumsum(self.charges).tolist()

		self.finalTime = self.actual_time_points[-1]
		self.finali = self.actual_current_points[-1]
		self.finalQ = self.cummcharges[-1]


	def ramp(self,t):
		exponent = -self.k*(t-self.t0)
		denom = np.exp(exponent)
		frac = self.A / (1+denom)

		return (frac + self.B) 

	def trap_charge(self,t1,i1,t2,i2):
		# calculating the expected charge from the individual linear sweeps
		h = (t2 - t1)
		area = (abs(i1)+abs(i2))*h/2 #trap area 
		q = area * 6e-5 #µA*min -->A*sec
	
		return q*1000 #should return mC


	def making_csv(self):
		self.df = pd.DataFrame({
			"Time(min)": self.actual_time_points,
			"Current(uA)": self.actual_current_points,
			"CumulativeCharge(mC)": self.cummcharges
		})

		return self.df


	def calculate_slope(self, i_start, i_end, t_start, t_end):
		return ((i_end - i_start) / ((t_end - t_start)*60))
	
	def generate_random_string(self, length):
		characters = string.ascii_letters + string.digits
		random_string = ''.join(random.choices(characters, k=length))
		return random_string

	def unique(self):
			#generating unique random experiment ID
			a = self.generate_random_string(8)
			b = self.generate_random_string(4)
			c = self.generate_random_string(4)
			d = self.generate_random_string(4)
			e = self.generate_random_string(12)
			unique_id_val = "{"+a+"-"+b+"-"+c+"-"+d+"-"+e+"}"

			return unique_id_val

		
	def making_linear_sweeps(self):
		self.actual_time_points = [0]
		self.actual_current_points = [self.ramp(0)]
		self.actual_ramp_slopes = []

		i = 0
		num_points = len(self.time_points)

		while i < num_points - 1:
			t_i = self.time_points[i]
			t_f = self.time_points[i + 1]

			curr_i = self.current_points[i]
			curr_f = self.current_points[i + 1]

			ramp_rate = self.calculate_slope(
				curr_i, curr_f, t_i, t_f
			)

			# Before t0, skip intervals that do not meet
			# the minimum allowed slope.
			if t_i < self.t0 and ramp_rate < self.slope_threshold:

				j = i + 1

				while j < num_points:
					new_slope = self.calculate_slope(
						self.current_points[i],
						self.current_points[j],
						self.time_points[i],
						self.time_points[j]
					)

					if new_slope >= self.slope_threshold:
						break

					j += 1

				# No suitable endpoint was found.
				if j >= num_points:
					break

				# Add the endpoint of the combined sweep.
				self.actual_time_points.append(self.time_points[j])
				self.actual_current_points.append(self.current_points[j])
				self.actual_ramp_slopes.append(new_slope)

				i = j

			# After t0, a negative slope means the
			# current-ramp algorithm needs another strategy.
			elif t_i >= self.t0 and ramp_rate < self.slope_threshold:
				break

			else:
				# Keep the original interval, but append
				# its ENDPOINT, not its starting point.
				self.actual_time_points.append(t_f)
				self.actual_current_points.append(curr_f)
				self.actual_ramp_slopes.append(ramp_rate)

				i += 1




	def making_json(self):
		unique_id_val = self.unique()
		
		experiment_start = {
			"custom-tile-usage": False,
			"description": "This is a custom experiment.",
			"elements": {
				"elements": [
					{
						"plugin-name": "Open Circuit Potential",
						"repeats": 1,
						"type": "element",
						"user-input": {
							"append--data-to-csv-file-checkbox": "Yes",
							"dvdt-minimum": "",
							"dvdt-minimum-units": "mV/s",
							"experiment-duration": "30",
							"experiment-duration-units": "s",
							"maximum-voltage": "",
							"maximum-voltage-units": "V",
							"minimum-voltage": "",
							"minimum-voltage-units": "V",
							"sampling-interval": "0.005",
							"sampling-interval-units": "s"
						}
					}
				],
				"repeats": 1,
				"type": "set"
			},
			"name": self.name,
			"uuid": unique_id_val
		}

		experiment_elements = []

		for i in range(len(self.actual_time_points) - 1):

			json_bit = {
				"plugin-name": "DC Current Linear Sweep",
				"repeats": 1,
				"type": "element",
				"user-input": {
					"Maximum-voltage": "",
					"Maximum-voltage-units": "V",
					"Minimum-voltage": "",
					"Minimum-voltage-units": "V",
					"alpha-factor": "100",
					"append--data-to-csv-file-checkbox": "Yes",
					"ending-current": f"{float(self.actual_current_points[i+1]):.12f}",
					"ending-current-units": "uA",
					"quiet-sampling-interval": "",
					"quiet-sampling-interval-units": "s",
					"quiet-time": "",
					"quiet-time-units": "s",
					"sampling-interval": "0.005",
					"sampling-interval-units": "s",
					"starting-current": f"{float(self.actual_current_points[i]):.12f}",
					"starting-current-units": "uA",
					"sweep-rate": f"{float(self.actual_ramp_slopes[i]):.12f}",
					"sweep-rate-units": "uA/s"
				}
			}
			experiment_elements.append(json_bit)

		experiment_start["elements"]["elements"].extend(experiment_elements)

		return json.dumps(experiment_start, indent=4)

	
	def plotting(self):
		fig, (ax1, ax2) = plt.subplots(1,2, figsize=(12,8))
				
		ax1.plot(self.actual_time_points, self.actual_current_points, linewidth=3, label = "Current", 
		         color="tab:blue", alpha=0.8, zorder=0)		
		ax1.scatter(self.actual_time_points, self.actual_current_points, s=30, label = "Linear Sweep Points", 
		         color="tab:blue", zorder=1)
		ax1.set_xlabel("Time (min)", fontsize=14)
		ax1.set_ylabel("Current Density (μA)", fontsize=14)
		ax1.set_title("Sigmoidal Current Ramp", fontsize=16)
		ax1.grid(axis='x', color='grey', linestyle = "--", linewidth=0.5)
		ax1.tick_params(axis='both', which='major', labelsize=12) 
		ax1.legend(title=f"A = {self.A} \nB = {self.B:.4f} \nk = {self.k} \nt0 = {self.t0} \nFinal Time = {self.finalTime:.4f}min \nFinal Current = {self.finali:.4f}μA \nNumber of Sweeps (adjusted) = {len(self.actual_time_points)-1}", title_fontsize=12, fontsize=10)

		ax2.plot(self.actual_time_points, self.cummcharges, linewidth=3, label="Charge", color="tab:red",
		         alpha=0.8, zorder=0)
		ax2.scatter(self.actual_time_points, self.cummcharges, s=30, label="Linear Sweep Points",
		            color="tab:red", zorder=1)		
		ax2.set_xlabel("Time (min)", fontsize=14)
		ax2.set_ylabel("Charge Passed (mC)", fontsize=14)
		ax2.set_title("Sigmoidal Current Ramp - Charge Passed", fontsize=16)
		ax2.grid(axis='x', color='grey', linestyle = "--", linewidth=0.5)
		ax2.tick_params(axis='both', which='major', labelsize=12) 
		ax2.legend(title=f"Final Q passed = {self.finalQ:.4f} mC", title_fontsize=14, fontsize=12)

		return fig 
	
	


# obj = squid(25,-30,1.4,1.73,5,50,"example")
# fig = obj.plotting()
# plt.show()