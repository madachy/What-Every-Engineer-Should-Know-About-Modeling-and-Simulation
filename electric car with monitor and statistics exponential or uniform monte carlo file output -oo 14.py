# https://repl.it/FPxV/68

from SimPy.Simulation import *
from random import Random,expovariate

import statistics
import math

class Electric_Car(Process):
  def __init__(self,name,charging_time):
     Process.__init__(self,name=name)
     self.charging_time = charging_time

  def visit_station(self):
     global cars_served
     if monte_carlo == False: print ("%4.1f  %3s Arriving at station" % (now(), self.name))
     arrive = now()
     yield request,self,charging_station
     if monte_carlo == False: print ("%4.1f  %3s Entering a charging bay" % (now(), self.name))
     waiting_time = now()-arrive
     car_monitor.observe(waiting_time)
     yield hold,self,self.charging_time
     yield release,self,charging_station
     cars_served += 1
     if monte_carlo == False: print ("%4.1f  %3s Charged and leaving" % (now(), self.name))

simulation_time = 720
#monte_carlo = True
monte_carlo = False
MC_run_summaries = False
num_iterations = 1000
if monte_carlo == False: num_iterations = 1

# exponential or uniform
distribution_type = 'uniform'
charging_bays=1

global cars_served

average_waiting_times = []

output_file_name = '../'+distribution_type+str(num_iterations)+'_'+str(simulation_time)+'min_capacity'+str(charging_bays)+'.txt'

output_file = open(output_file_name, 'w')
#output_file.write(distribution_type+str(num_iterations)+'_60min_capacity1.txt' + '\n')
output_file.write("iteration average_wait utilization" + '\n')
  

interarrival_times = [2, 8, 7, 2, 11, 3, 15, 9] #random.uniform(2, 15)
charging_times = [11, 8, 5, 8, 8, 5, 10, 12] #random.uniform(5, 15)



#exponential distribution
mean_interarrival_time = 6.0
mean_charging_time = 5.0

if (monte_carlo == True and MC_run_summaries == True): print ("cars_served Mean Waiting Time Utilization Average Queue Length")


for iteration in range(num_iterations):
  initialize()
  car_monitor = Monitor() 

  charging_station = Resource(capacity=charging_bays,
                      name='charging_station',unitName='charging bay',monitored=True, monitorType=Monitor)
  arrival_time = 0
  cars_served = 0

  if monte_carlo == False: print ('Time  Event')
  
  # continue loop until events meet simulation time
  for i in range(200):
       if distribution_type == 'exponential': 
           arrival_time += random.expovariate(0.16)
           charging_time = random.expovariate(0.2)
       if distribution_type == 'uniform': 
           arrival_time += random.uniform(2, 15)
           charging_time = random.uniform(5, 15)
       this_car_name = "Car "+str(i+1)
       this_car =  Electric_Car(this_car_name,charging_time)
       activate(this_car,this_car.visit_station( ),at=arrival_time) 

  simulate(until=simulation_time)

  average_waiting_times.append(car_monitor.mean())
  if monte_carlo == False:
      print("\nCars Entered = %3.0f" % car_monitor.count())
      print("Cars Served = %3.0f" % cars_served)
      print ("Mean Waiting Time = %3.1f minutes" % car_monitor.mean())
      print ("Waiting Time σ = %3.1f minutes" % car_monitor.var()**.5)
      print ('Utilization = %3.1f ' % charging_station.actMon.timeAverage())
      # print ('(Number) Average no. waiting:',charging_station.waitMon.mean())
      low = car_monitor.mean() - 1.96*car_monitor.var()**.5/(cars_served**.5)
      high = car_monitor.mean() + 1.96*car_monitor.var()**.5/(cars_served**.5)
      print ('95%% Confidence Interval = %3.1f - %3.1f' % (low, high))
      print ('Average Queue Length = %4.1f ' % charging_station.waitMon.timeAverage())
      output_file.write("%2.0f %6.2f %6.2f" % (iteration, car_monitor.mean(), charging_station.actMon.timeAverage()) + '\n')

  if monte_carlo == True: 
      output_file.write("%2.0f %6.3f %6.3f" % (iteration, car_monitor.mean(), charging_station.actMon.timeAverage()) + '\n')
      if MC_run_summaries == True: print ("%3d %3.1f %3.1f %3.1f" % (cars_served, car_monitor.mean(), charging_station.actMon.timeAverage(), charging_station.waitMon.timeAverage()) )
    
output_file.close()

if monte_carlo == True: 
    print ('M-C mean waiting time = %4.3f ' % statistics.mean(average_waiting_times))
    #print ('M-C max waiting time = ', statistics.maximum(average_waiting_times))
    print ('M-C variance of waiting time = %4.3f ' % statistics.variance(average_waiting_times))
    
