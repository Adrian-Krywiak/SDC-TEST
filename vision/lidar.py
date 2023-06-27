import time
import numpy as np
import matplotlib.pyplot as plt
from rplidar import RPLidar

lidar = RPLidar('COM3')  # Replace with your port, like 'COM3'

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')

try:
    print("Recording measurements... Stop with Ctrl+C")
    for scan in lidar.iter_scans():
        angles = []
        distances = []
        for (_, angle, distance) in scan:
            angles.append(np.radians(angle))
            distances.append(distance)
        ax.clear()
        ax.scatter(angles, distances, s=1)
        ax.set_rmax(6000)
        ax.grid(True)
        plt.pause(0.001)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    lidar.stop()
    lidar.disconnect()
    plt.close()
