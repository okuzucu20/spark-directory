#!/usr/bin/env python3
from environs import Env
import lgsvl
import threading
import time
import subprocess
from tkinter import *
from tkinter import messagebox

class Simulation:

    def __init__(self):
        self.env = Env()

        self.sim = lgsvl.Simulator(self.env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1"), self.env.int("LGSVL__SIMULATOR_PORT", 8181))
        self.sensors = None

    def initialize_simulation(self):
        if self.sim.current_scene == "Teknofest-1.1":
            self.sim.reset()
        else:
            self.sim.load(scene="Teknofest-1.1")
        spawns = self.sim.get_spawn()
        state = lgsvl.AgentState()
        state.transform = spawns[0]
        ego = self.sim.add_agent(name="Jaguar2015XE (ROS2 Bridge)", agent_type=lgsvl.AgentType.EGO, state=state)

        self.sensors = ego.get_sensors()

    def run_simulation(self):
        self.sim.run()

    def get_sensors(self):
        return self.sensors


class TkinterApp:

    def __init__(self, sensors):
        self.sensors = sensors

        self.window = Tk()
        window = self.window

        window.title("SPARK LGSVL Image/Point Cloud Saver")

        window.geometry('750x750')

        btn = Button(window, text="Save Point Cloud", command=self.PclFrequency)
        btn.grid(column=0, row=0)

        btn = Button(window, text="Save Main Camera Image", command=self.ImageFrequency)
        btn.grid(column=0, row=1)

    def getLastCameraIndex(self, save_type):
        subprocess.call("chmod 755 ~/spark/lgsvl-pcl-image-saver-tool/findLast.sh", shell=True)
        output = subprocess.getoutput(f"~/spark/lgsvl-pcl-image-saver-tool/findLast.sh {save_type}")
        last_file_number = int(output)

        return last_file_number

    def clicked_save(self, save_type, frequency):

        if save_type == 'image':
            for s in self.sensors:
                if s.name == "Main Camera":
                    c = self.getLastCameraIndex('camera')
                    while True:
                        c += 1
                        time.sleep(frequency)
                        s.save(f"camera/camera{c}.png", compression=0)
                        print("geldi")

        elif save_type == 'pcl':
            for s in self.sensors:
                if s.name == "Lidar":
                    c = self.getLastCameraIndex('lidar')
                    while True:
                        c += 1
                        time.sleep(frequency)
                        s.save(f"lidar/lidar{c}.pcd")

    def runFrequencyWindow(self, save_type):

        frequency_window = Tk()

        label = Label(frequency_window, text="Please enter a frequency (in seconds)")
        label.grid(column=0, row=0)

        entry = Entry(frequency_window)
        entry.grid(column=0, row=1)

        def getFrequency():

            try:
                frequency = float(entry.get())
                #frequency_window.destroy()
                #self.window.destroy()
                self.clicked_save(save_type, frequency)

            except ValueError:
                messagebox.showwarning("Input Error", "You should enter a number.")

        btn = Button(frequency_window, text="Enter", command=getFrequency)
        btn.grid(column=0, row=2)

        frequency_window.mainloop()

    def ImageFrequency(self):
        self.runFrequencyWindow('image')

    def PclFrequency(self):
        self.runFrequencyWindow('pcl')

    def run(self):
        self.window.mainloop()


def main():
    simulation = Simulation()
    simulation.initialize_simulation()
    thread1 = threading.Thread(target=simulation.run_simulation,daemon=True)
    thread1.start()
    print("x")
    app = TkinterApp(simulation.get_sensors())
    app.run()


if __name__ == "__main__":
    main()
