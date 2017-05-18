# simulation of electric car charging station

import simpy
import statistics

# instantiate execution environment for simulation
environment = simpy.Environment()

# charging station resource
charging_station = simpy.Resource(environment, capacity=1)

# fixed interarrival and charging times
interarrival_times = [2, 8, 7, 2, 11, 3, 15, 9]
charging_times = [11, 8, 5, 8, 8, 5, 10, 12] 

# statistics initialization
waiting_times = []

# electric car process generator
def electric_car(environment, name, charging_station, arrival_time, charging_time):
     # trigger arrival event at charging station
     yield environment.timeout(arrival_time)

     # request charging bay resource
     print('%s arriving at %s' % (name, environment.now))
     with charging_station.request() as request:
         yield request

         waiting_time = environment.now - arrival_time
         print('%s waiting time %s' % (name, waiting_time))
         
         # charge car battery
         print('%s starting to charge at %s' % (name, environment.now))
         yield environment.timeout(charging_time)
         print('%s leaving at %s' % (name, environment.now))

         # collect waiting times
         waiting_times.append(waiting_time)

arrival_time = 0
# simulate car processes
for i in range(7):
     arrival_time += interarrival_times[i]
     charging_time = charging_times[i]
     environment.process(electric_car(environment, 'Car %d' % i, charging_station, arrival_time, charging_time))
     #print('%s waiting time = %s' % (i, waiting_time))

environment.run()
print('Waiting Times', waiting_times)
print ('Mean Waiting Time = ', statistics.mean(waiting_times))
print ('Variance of Waiting Time = ', statistics.variance(waiting_times))
