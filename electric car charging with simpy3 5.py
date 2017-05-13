# simulation of electric car charging station with simpy3

import simpy
import statistics
from random import Random,expovariate

simulation_time = 500
monte_carlo = False
num_iterations = 100
charging_bays=1

# exponential or uniform
distribution_type = 'exponential'


# execution environment for event-based simulation
environment = simpy.Environment()

# charging station resource
charging_station = simpy.Resource(environment, capacity=charging_bays)

# event times
interarrival_times = [2, 8, 7, 2, 11, 3, 15, 9] #random.uniform(2, 15)
charging_times = [11, 8, 5, 8, 8, 5, 10, 12] #random.uniform(5, 15)

# list of waiting times
waiting_times = []
average_waiting_times = []

cars_served = 0

# statistics initialization
global charger_in_use, queue_length
charger_in_use = False
queue_length = 0

if monte_carlo == False: num_iterations = 1


# electric car process generator
def electric_car(environment, name, charging_station, arrival_time, charging_time):
     global charger_in_use, queue_length
     # trigger arrival event at charging station
     yield environment.timeout(arrival_time)
     if monte_carlo == False: print('%s arriving at %s' % (name, environment.now))

     # request charging bay resource

     with charging_station.request() as request:
         if charger_in_use == True: queue_length +=1
         yield request
         charger_in_use = True

         waiting_time = environment.now - arrival_time
         if monte_carlo == False: print('%s waiting time %s' % (name, waiting_time))
         
         # charge car battery
         if monte_carlo == False: print('%s starting to charge at %s' % (name, environment.now))
         yield environment.timeout(charging_time)
         cars_served +1
         charger_in_use = False
         if queue_length > 0: queue_length -=1
         if monte_carlo == False: print('%s leaving at %s' % (name, environment.now))

         waiting_times.append(waiting_time)  # collect waiting times



# simulate car processes
for iteration in range(num_iterations):
     arrival_time = 0
     for car in range(200):
         # process the events
         #arrival_time += interarrival_times[i]
         #charging_time = charging_times[i]
         if distribution_type == 'exponential': arrival_time += random.expovariate(0.16)
         if distribution_type == 'uniform': arrival_time += random.uniform(2, 15)
         if distribution_type == 'exponential': charging_time = random.expovariate(0.2)
    
         if distribution_type == 'uniform': charging_time = random.uniform(5, 15)
         
         if monte_carlo == False: print('%d of %d slots are allocated.' % (charging_station.count, charging_station.capacity))
    
         environment.process(electric_car(environment, 'Car %d' % car, charging_station, arrival_time, charging_time))
         if monte_carlo == False: print('%d of %d slots are allocated.' % (charging_station.count, charging_station.capacity))
              #print('%s waiting time = %s' % (car, waiting_time))

     environment.run(until=simulation_time)
     average_waiting_times.append(statistics.mean(waiting_times))
     if monte_carlo == False: print('Waiting times', waiting_times)
     if monte_carlo == False: print ('Mean waiting time,', statistics.mean(waiting_times))
     #print (statistics.mean(waiting_times))
     if monte_carlo == False: print ('Variance of waiting time = ', statistics.variance(waiting_times))
     environment = simpy.Environment()
     charging_station = simpy.Resource(environment, capacity=charging_bays)
     waiting_times = []
     charger_in_use = False
     queue_length = 0

if monte_carlo == True: print ('M-C mean waiting time = ', statistics.mean(average_waiting_times))
if monte_carlo == True: print ('M-C variance of waiting time = ', statistics.variance(average_waiting_times))