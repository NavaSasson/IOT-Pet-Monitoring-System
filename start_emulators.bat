// arg: Name Units Place UpdateTime

start "Emulator: Pet Activity Monitor" python emulator.py PetActivityMonitor activity Home 10

timeout 3
start "Emulator: Pet Temperature Monitor" python emulator.py PetTemperatureMonitor Celsius Home 6
timeout 3
start "Emulator: Pet Water Level Monitor" python emulator.py PetWaterLevelMonitor liters Home 8
timeout 3
start "Emulator: Pet Feeder" python emulator.py PetFeeder food Home 9
timeout 3
start "Smart Home Manager" python manager.py
timeout 10
start "System GUI" python gui.py
