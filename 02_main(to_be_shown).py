import pandas as pd
import turtle
import matplotlib.pyplot as plt

screen = turtle.Screen()
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.title("Vehicle Crash Detection System v1.0.0")

try:
    screen.bgpic("Files/logo.gif")
except:
    print("Background image not found, continuing without it")

def detect_crashes(speed_data, timestamps, threshold_drop=30, high_speed_threshold=80):
    crashes = []
    for i in range(1, len(speed_data)):
        prev_speed = speed_data[i - 1]
        curr_speed = speed_data[i]
        if prev_speed - curr_speed >= threshold_drop and prev_speed > high_speed_threshold:
            crashes.append((i, prev_speed, curr_speed, timestamps[i]))
    return crashes

def transition():
    screen.clear()
    screen.bgcolor("black")
    try:
        screen.bgpic("Files/crash.gif")
    except:
        pass
    screen.title("Vehicle Crash Detection System v1.0.0")
    try:
        df = pd.read_csv("Files/simulated_speed_data.csv")
    except FileNotFoundError:
        print("CSV file not found. Exiting.")
        screen.bye()
        return
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['speed_kmph'], marker='o', linestyle='-', linewidth=2, color='blue')
    crashes = detect_crashes(df['speed_kmph'].tolist(), df['timestamp'].tolist())
    if crashes:
        for crash in crashes:
            i, prev, curr, timestamp = crash
            plt.plot(timestamp, curr, 'ro', markersize=10)
            plt.annotate(f'Crash: {prev} to {curr} km/h',
                         (timestamp, curr),
                         textcoords="offset points",
                         xytext=(0, 15),
                         ha='center',
                         fontsize=10,
                         color='red',
                         weight='bold')
    plt.title('Vehicle Speed Over Time with Crash Detection', fontsize=14, weight='bold')
    plt.xlabel('Timestamp', fontsize=12)
    plt.ylabel('Speed (km/h)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color("red")
    pen.goto(0, 200)
    if crashes:
        y_position = 200
        for crash in crashes:
            i, prev, curr, timestamp = crash
            pen.goto(0, y_position)
            pen.write("CRASH SUSPECTED!", align="center", font=("Arial", 45, "bold"))
            y_position -= 40
            pen.goto(0, y_position)
            pen.write(f"Time: {timestamp}", align="center", font=("Arial", 28, "bold"))
            y_position -= 30
            pen.goto(0, y_position)
            pen.write(f"Speed dropped from {prev} to {curr} km/h", align="center", font=("Arial", 28, "bold"))
            y_position -= 30
            pen.goto(0, y_position)
            pen.write(f"Impact: {prev - curr} km/h drop", align="center", font=("Arial", 28, "bold"))
            y_position -= 50
    else:
        pen.goto(0, 0)
        pen.color("green")
        pen.write("No crash events detected", align="center", font=("Arial", 24, "bold"))


screen.ontimer(transition, 4500)
try:
    screen.mainloop()
except:
    print("Turtle window closed")
