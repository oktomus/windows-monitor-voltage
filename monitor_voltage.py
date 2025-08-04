import time
from dependencies.HardwareMonitor.Hardware import *

# Config
charger_amps = 3.5
interval_seconds = 10

# Accumulators
total_voltage = 0.0
total_power = 0.0
samples = 0
start_time = None

# Min/max tracking
max_power = float('-inf')
min_power = float('inf')

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


def main():
    global total_voltage, total_power, samples, start_time
    global max_power, min_power

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

    start_time = time.time()

    try:
        while True:
            computer.Accept(UpdateVisitor())
            voltage = get_voltage(computer)

            if voltage is not None and voltage > 0:
                power = voltage * charger_amps

                total_voltage += voltage
                total_power += power
                samples += 1

                max_power = max(max_power, power)
                min_power = min(min_power, power)

                elapsed_time = time.time() - start_time
                elapsed_hours = elapsed_time / 3600
                avg_power = total_power / samples
                total_energy_wh = avg_power * elapsed_hours

                # Min/max energy based on worst/best case if sustained
                min_energy_wh = min_power * elapsed_hours
                max_energy_wh = max_power * elapsed_hours

                print(f"Sample #{samples}")
                print(f"Voltage: {voltage:.2f} V | Instant Power: {power:.2f} W")
                print(f"Total Time: {elapsed_hours:.4f} h")
                print(f"Average Power: {avg_power:.2f} W")
                print(f"Min Power: {min_power:.2f} W | Max Power: {max_power:.2f} W")
                print(f"Total Power Sum: {total_power:.2f} W")
                print(f"Total Energy: {total_energy_wh:.4f} Wh")
                print(f"Min Energy Estimate: {min_energy_wh:.4f} Wh")
                print(f"Max Energy Estimate: {max_energy_wh:.4f} Wh")
                print("-" * 70)

            time.sleep(interval_seconds)

    finally:
        computer.Close()


if __name__ == "__main__":
    main()
