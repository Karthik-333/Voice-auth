import sounddevice as sd

print("Available audio devices:")
print(sd.query_devices())

print("\nDefault device:")
print(sd.default.device)
