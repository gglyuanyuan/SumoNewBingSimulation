import traci
import traci.constants as tc
import sys
sys.path.append("D:/Program_WorkApplication/Eclipse/Sumo/tools")

# start sumo with gui and load the network and route files
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "sumo.cfg"]
traci.start(sumoCmd)

# subscribe to the emergency vehicles and get their ids
traci.vehicle.subscribeContext("emergency_flow", tc.CMD_GET_VEHICLE_VARIABLE, 100, [tc.VAR_SPEED])
emergency_ids = traci.vehicle.getContextSubscriptionResults("emergency_flow")

# loop until the simulation ends
while traci.simulation.getMinExpectedNumber() > 0:
    # advance the simulation by one step
    traci.simulationStep()
    
    # get the current time
    time = traci.simulation.getTime()
    
    # loop over the emergency vehicles
    for eid in emergency_ids:
        # get the speed of the emergency vehicle
        espeed = traci.vehicle.getSubscriptionResults(eid)[tc.VAR_SPEED]
        
        # get the surrounding vehicles within 100 meters
        neighbors = traci.vehicle.getContextSubscriptionResults(eid)
        
        # loop over the surrounding vehicles
        for nid in neighbors:
            # get the speed of the neighbor vehicle
            nspeed = neighbors[nid]  
            # if the neighbor vehicle is a social vehicle and is slower than the emergency vehicle
            if nid.startswith("social") and nspeed < espeed:
                # get the lane index of the neighbor vehicle
                nlane = traci.vehicle.getLaneIndex(nid)
                
                # if the neighbor vehicle is on the leftmost lane
                if nlane == 0:
                    # change its lane to the right
                    traci.vehicle.changeLane(nid, 1, 10)
                
                # if the neighbor vehicle is on the middle lane
                elif nlane == 1:
                    # get the right lane vehicles
                    rlane_vehicles = traci.lane.getLastStepVehicleIDs("e1_2")
                    
                    # if there is no vehicle on the right lane or the gap is large enough
                    if len(rlane_vehicles) == 0 or traci.vehicle.getLeader(nid, 2.5)[1] > 10:
                        # change its lane to the right
                        traci.vehicle.changeLane(nid, 2, 10)
                
                # if the neighbor vehicle is on the rightmost lane
                else:
                    # slow down to let the emergency vehicle pass
                    traci.vehicle.slowDown(nid, nspeed - 5, 5)

# close the connection to sumo
traci.close()
