import os
import traci
import sys
sys.path.append("D:/Program_WorkApplication/Eclipse/Sumo/tools")

# set the path of sumo binary
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "sumo.cfg"]

# start the simulation
traci.start(sumoCmd)

# get the list of emergency vehicles
emergency_vehicles = traci.vehicle.getIDList()
emergency_vehicles = [v for v in emergency_vehicles if v.startswith("emergency")]

# get the list of social vehicles
social_vehicles = traci.vehicle.getIDList()
social_vehicles = [v for v in social_vehicles if v.startswith("social")]

# set the simulation step length
step_length = 0.1

# run the simulation for 1000 steps
for i in range(1000):
    # advance the simulation by one step
    traci.simulationStep()

    # loop through all emergency vehicles
    for ev in emergency_vehicles:
        # get the current lane and position of the emergency vehicle
        ev_lane = traci.vehicle.getLaneID(ev)
        ev_pos = traci.vehicle.getLanePosition(ev)

        # loop through all social vehicles
        for sv in social_vehicles:
            # get the current lane and position of the social vehicle
            sv_lane = traci.vehicle.getLaneID(sv)
            sv_pos = traci.vehicle.getLanePosition(sv)

            # check if the social vehicle is on the same edge as the emergency vehicle
            if ev_lane.split("_")[0] == sv_lane.split("_")[0]:
                # check if the social vehicle is ahead of the emergency vehicle and within 50 meters
                if sv_pos > ev_pos and sv_pos - ev_pos < 50:
                    # check if the social vehicle is on the left lane of the emergency vehicle
                    if int(sv_lane.split("_")[1]) < int(ev_lane.split("_")[1]):
                        # try to change the lane of the social vehicle to the right
                        traci.vehicle.changeLane(sv, int(sv_lane.split("_")[1]) + 1, 5)
                    # check if the social vehicle is on the same lane as the emergency vehicle
                    elif int(sv_lane.split("_")[1]) == int(ev_lane.split("_")[1]):
                        # try to change the lane of the social vehicle to the left or right, depending on availability
                        if traci.vehicle.couldChangeLane(sv, -1):
                            traci.vehicle.changeLane(sv, int(sv_lane.split("_")[1]) - 1, 5)
                        elif traci.vehicle.couldChangeLane(sv, 1):
                            traci.vehicle.changeLane(sv, int(sv_lane.split("_")[1]) + 1, 5)

# close the simulation
traci.close()
