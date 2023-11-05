import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random

# Create a Tkinter window
root = tk.Tk()
root.title("Real-time Updating Plot")

# Create a Frame to contain the Matplotlib plot
frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a Matplotlib Figure and Axes
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
line, = ax.plot([], [], lw=2)

# Function to initialize the plot
def init():
    line.set_data([], [])
    return line,

# Function to update the plot data
def update(frame):
    x_data.append(frame)
    y_data.append(random.randint(0, 100))
    line.set_data(x_data, y_data)
    return line,

# Create a canvas to display the Matplotlib plot
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()

# Create a Quit button to exit the application
quit_button = ttk.Button(root, text="Quit", command=root.quit)
quit_button.pack(pady=10)

# Start the Tkinter main loop

x_data = []
y_data = []
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, frames=100, interval=100)
root.mainloop()
