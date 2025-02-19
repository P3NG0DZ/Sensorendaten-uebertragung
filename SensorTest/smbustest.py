from smbus2 import SMBus

address = 0x48  # Standardadresse des ADS1115
bus = SMBus(1)

try:
    bus.write_byte(address, 0)  # Sende ein Byte zum Testen
    print("ADS1115 erfolgreich erkannt!")
except Exception as e:
    print(f"Fehler: {e}")
finally:
    bus.close()
