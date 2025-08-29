import pandas as pd
import sys  
from colorama import Fore, Style
import turtle
import matplotlib.pyplot as plt
screen = turtle.Screen()
screen.bgcolor("black")
screen.bgpic("Files/logo.gif")
screen.title("Vehicle Crash Detection System v1.0.0")

def transition():
    screen.clear()
    screen.bgpic("Files/crash.gif")
    screen.title("Vehicle Crash Detection System v1.0.0")

    try:
        df = pd.read_csv("Files/simulated_speed_data.csv")
    except FileNotFoundError:
        sys.exit()  

    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['speed_kmph'], marker='o', linestyle='-', linewidth=2)

    plt.title('Vehicle Speed Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Speed (km/h)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()
    
    def detect_crash(speed_data, threshold_drop=30, minimum_speed=30):
        alerts = []
        for i in range(1, len(speed_data)):
            prev_speed = speed_data[i - 1]
            curr_speed = speed_data[i]
            if (prev_speed - curr_speed) >= threshold_drop and curr_speed <= minimum_speed:
                alerts.append((i, prev_speed, curr_speed))
        return alerts

    alerts = detect_crash(df['speed_kmph'].tolist())

    pen = turtle.Turtle()
    pen.hideturtle()
    pen.penup()
    pen.color((1.0, 0.0, 0.0824))
    pen.goto(0, 200)
    pen.speed(0)

    line_spacing = 30  

    if alerts:
        y = 200  
        for alert in alerts:
            i, prev, curr = alert
            timestamp = df.iloc[i]['timestamp']

            message_1 = f"Crash suspected at {timestamp}"
            message_2 = f"Speed dropped from {prev} to {curr} km/h"

            # print(Fore.RED + message_1)
            # print(message_2)
            # print(Style.RESET_ALL)

            pen.goto(0, y)
            pen.write(message_1, align="center", font=("Arial", 24, "bold"))
            y -= line_spacing
            pen.goto(0, y)
            pen.write(message_2, align="center", font=("Arial", 14, "normal"))
            y -= line_spacing * 2  

    else:
        safe_msg = "No abnormal speed drops detected"
        print(Fore.GREEN + safe_msg)
        print(Style.RESET_ALL)
        pen.goto(0, 0)
        pen.write(safe_msg, align="center", font=("Arial", 26, "bold"))

screen.ontimer(transition, 4500)
screen.mainloop()