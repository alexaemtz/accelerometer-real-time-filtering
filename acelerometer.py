"""Moving average filter in real time
for a 3-axis accelerometer
Date: 29-04-2024
V. 1.1.0"""

import serial
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Inicializes serial communication
esp32_port = 'COM3'  # Initializes reading in COM port
baud = 9600

ser = serial.Serial(esp32_port, baud)
print(f'Conexión exitosa a ESP32 en puerto {esp32_port}.')

# Lists to save the data
x_values = []
y_values = []
z_values = []

x_values_filtered = []
y_values_filtered = []
z_values_filtered = []

# The bigger the window, the better the filter but it's slower 
window_size = 20

# Read and process data from the ESP32
def read_and_process_data():
    try:
        line = ser.readline().decode().strip()
        sensorValues = line.split(',')

        if len(sensorValues) == 3:
            x_values.append(float(sensorValues[0]))
            y_values.append(float(sensorValues[1]))
            z_values.append(float(sensorValues[2]))
            
    except Exception as e:
        print("Error al leer los datos:", e)

def moving_average(data):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')
    
def moving_average_real_time():
    global x_values
    if len(x_values) >= window_size:
        x_filtered = moving_average(x_values)[-1]
        y_filtered = moving_average(y_values)[-1]
        z_filtered = moving_average(z_values)[-1]
        
        x_values_filtered.append(x_filtered)
        y_values_filtered.append(y_filtered)
        z_values_filtered.append(z_filtered)
        
def update_plot(frame):
    read_and_process_data()
    plt.cla()  
    plt.plot(x_values, label='X original')
    plt.plot(y_values, label='Y original')
    plt.plot(z_values, label='Z original')
    
    moving_average_real_time()
    plt.plot(x_values_filtered, label='X filtrada')
    plt.plot(y_values_filtered, label='Y filtrada')
    plt.plot(z_values_filtered, label='Z filtrada')

    plt.xlabel("Muestras")
    plt.ylabel("Aceleración")
    plt.legend()        

def on_close(event):
    ser.close()

fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update_plot, interval=10, cache_frame_data=False) # 10 ms = 100 Hz (1/0.01)
plt.show()
