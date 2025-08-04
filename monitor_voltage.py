import csv
import os
import time
from datetime import datetime

from dependencies.HardwareMonitor.Hardware import *

class UpdateVisitor(IVisitor):
    __namespace__ = "TestHardwareMonitor"

    def VisitComputer(self, computer: IComputer):
        computer.Traverse(self)

    def VisitHardware(self, hardware: IHardware):
        hardware.Update()
        for subHardware in hardware.SubHardware:
            subHardware.Update()

    def VisitParameter(self, parameter: IParameter): pass
    def VisitSensor(self, sensor: ISensor): pass


def get_voltage(inComputer):
    voltage = -1
    for hardware in inComputer.Hardware:
        for sensor in hardware.Sensors:
            if sensor.Name == "Voltage":
                if voltage != -1:
                    print("ERR: DOUBLE VOLTAGE FOUND")
                voltage = sensor.Value
    return voltage


def init_csv(file_path):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Voltage (V)"])


def append_voltage(file_path, voltage):
    timestamp = datetime.now().isoformat()
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, voltage])


def main():
    file_path = 'out.csv'
    init_csv(file_path)

    computer = Computer()
    computer.IsMotherboardEnabled = True
    computer.IsControllerEnabled = True
    computer.IsCpuEnabled = True
    computer.IsGpuEnabled = True
    computer.IsBatteryEnabled = True
    computer.IsMemoryEnabled = True
    computer.IsNetworkEnabled = True
    computer.IsStorageEnabled = True
    computer.Open()

    while True:
        computer.Accept(UpdateVisitor())
        voltage = get_voltage(computer)
        print(f"[{datetime.now()}] Voltage: {voltage}")
        append_voltage(file_path, voltage)
        time.sleep(10)

    computer.Close()  # Never reached if killing the process


if __name__ == "__main__":
    main()
