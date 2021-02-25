#!/usr/bin/env python3
#
# Copyright (c) 2019-2020 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

from environs import Env
import lgsvl

env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), env.int("LGSVL__SIMULATOR_PORT", 8181))
if sim.current_scene == "BorregasAve":
    sim.reset()
else:
    sim.load("BorregasAve", 42)

spawns = sim.get_spawn()

state = lgsvl.AgentState()
forward = lgsvl.utils.transform_to_forward(spawns[0])
state.transform = spawns[0]
state.transform.position = spawns[0].position + 20 * forward
sim.add_agent(env.str("LGSVL__VEHICLE_0", "Lincoln2017MKZ (Apollo 5.0)"), lgsvl.AgentType.EGO, state)

print("Python API Quickstart #27: How to Control Traffic Light")

# # Get a list of controllable objects
controllables = sim.get_controllables("signal")
print("\n# List of controllable objects in {} scene:".format("BorregasAve"))
for c in controllables:
    print(c)

signal = sim.get_controllable(lgsvl.Vector(15.5, 4.7, -23.9), "signal")
print("\n# Signal of interest:")
print(signal)

# Get current controllable states
print("\n# Current control policy:")
print(signal.control_policy)

# Create a new control policy
control_policy = "trigger=50;green=3;yellow=2;red=1;loop"

# Control this traffic light with a new control policy
signal.control(control_policy)

print("\n# Updated control policy:")
print(signal.control_policy)

# Get current state of signal
print("\n# Current signal state before simulation:")
print(signal.current_state)

seconds = 18
input("\nPress Enter to run simulation for {} seconds".format(seconds))
print("\nRunning simulation for {} seconds...".format(seconds))
sim.run(seconds)

print("\n# Current signal state after simulation:")
print(signal.current_state)
print("\nDone!")
