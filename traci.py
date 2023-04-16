import os
import traci
import matplotlib.pyplot as plt
import sys
sys.path.append("D:/Program_WorkApplication/Eclipse/Sumo/tools")

# set the path of sumo binary
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "sumo.cfg"]

# start the simulation
traci.start(sumoCmd)

# get the list of all vehicles
all_vehicles = traci.vehicle.getIDList()

# create empty dictionaries to store the speed, acceleration and position of each vehicle
speed_dict = {}
accel_dict = {}
pos_dict = {}

# initialize the dictionaries with empty lists for each vehicle
for v in all_vehicles:
    speed_dict[v] = []
    accel_dict[v] = []
    pos_dict[v] = []

# set the simulation step length
step_length = 0.1

# run the simulation for 1000 steps
for i in range(1000):
    # advance the simulation by one step
    traci.simulationStep()

    # loop through all vehicles
    for v in all_vehicles:
        # get the current speed, acceleration and position of the vehicle
        speed = traci.vehicle.getSpeed(v)
        accel = traci.vehicle.getAcceleration(v)
        pos = traci.vehicle.getPosition(v)

        # append the values to the corresponding lists in the dictionaries
        speed_dict[v].append(speed)
        accel_dict[v].append(accel)
        pos_dict[v].append(pos)

# close the simulation
traci.close()

# create a folder to store the output files
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# loop through all vehicles
for v in all_vehicles:
    # plot the speed, acceleration and position of the vehicle over time
    plt.figure(figsize=(10, 10))
    plt.subplot(3, 1, 1)
    plt.plot(speed_dict[v])
    plt.xlabel("Time (s)")
    plt.ylabel("Speed (m/s)")
    plt.title(f"Speed of vehicle {v}")

    plt.subplot(3, 1, 2)
    plt.plot(accel_dict[v])
    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s^2)")
    plt.title(f"Acceleration of vehicle {v}")

    plt.subplot(3, 1, 3)
    plt.plot([p[0] for p in pos_dict[v]], [p[1] for p in pos_dict[v]])
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title(f"Position of vehicle {v}")

    # save the plot as an image file in the output folder
    plt.savefig(os.path.join(output_folder, f"{v}.png"))