import pandas as pd                  # Load the pandas library to read CSV files and handle tabular data.
import sys                           # (Imported but not used.) Normally for system-level stuff like args, exit codes.
import turtle                        # Turtle graphics library for a simple GUI window and drawing text.
import matplotlib.pyplot as plt      # Matplotlib plotting module to draw the speed vs. time graph.
import numpy as np                   # NumPy for fast math (e.g., sine function to simulate speed wiggles).


screen = turtle.Screen()             # Create a new Turtle window (the canvas where we draw).
screen.bgcolor("black")              # Make the Turtle window background black.
screen.setup(width=800, height=600)  # Set the window size to 800x600 pixels.
screen.title("Vehicle Crash Detection System v1.0.0")  # Set the window title text.

try:
    screen.bgpic("Files/logo.gif")   # Try to set a background image (GIF only) if the file exists.
except:
    print("Background image not found, continuing without it")  # If missing/invalid, tell the console and carry on.


def detect_crashes(speed_data, timestamps, threshold_drop=30, high_speed_threshold=80):
    # Define a function that scans speeds and flags “crashes”:
    # A crash = previous speed > 80 km/h AND sudden drop ≥ 30 km/h compared to current speed.
    crashes = []                                                     # Will store tuples for each detected crash.
    for i in range(1, len(speed_data)):                              # Loop from the 2nd data point to the end.
        prev_speed = speed_data[i - 1]                               # Speed at previous time step.
        curr_speed = speed_data[i]                                   # Speed at current time step.
        speed_drop = prev_speed - curr_speed                         # How much speed fell between steps.
    
        if speed_drop >= threshold_drop and prev_speed > high_speed_threshold:
            # If drop is big enough AND we were going fast before the drop, mark as crash.
            crashes.append((i, prev_speed, curr_speed, timestamps[i]))  # Save index, speeds, and timestamp.
    
    return crashes                                                   # Give back the list of all detected crashes.


def transition():
    # This function runs after a short delay; it switches the UI into “analysis” mode and does the work.
    screen.clear()                                                   # Wipe whatever was on the Turtle screen.
    screen.bgcolor("black")                                          # Keep the background black again.
    try:
        screen.bgpic("Files/crash.gif")                              # Try to show a “crash” background GIF.
    except:
        pass                                                         # If that fails, silently ignore and move on.
    
    screen.title("Vehicle Crash Detection System - Crash Analysis")  # Update the window title for the analysis phase.

    try:
        df = pd.read_csv("Files/simulated_speed_data.csv")           # Try to load speed data from a CSV file.
    except FileNotFoundError:
        # If the CSV isn’t there, build a fake dataset so the program still demonstrates the logic.
        print("CSV file not found, creating sample data...")
        timestamps = [f"00:{i:02d}" for i in range(60)]              # Make 60 timestamps: 00:00, 00:01, ..., 00:59
        speeds = [120 + 5*np.sin(i/3) for i in range(60)]            # Simulate speeds around 120 with tiny sine wiggles.
        
        speeds[30] = 45                                              # Inject a big sudden drop at t=30 (possible crash).
        speeds[31] = 40                                              # Follow-up slight drop at t=31 (not big enough to count).
        df = pd.DataFrame({'timestamp': timestamps, 'speed_kmph': speeds})  # Build a DataFrame with our data.
    
    # ---- Plotting the speed curve and marking detected crashes ----
    plt.figure(figsize=(12, 6))                                      # New plot with a wide aspect ratio.
    plt.plot(df['timestamp'], df['speed_kmph'],                      # X = timestamps (strings), Y = speeds.
             marker='o', linestyle='-', linewidth=2, color='blue')   # Style: line with circular markers, blue line.
    
    crashes = detect_crashes(df['speed_kmph'].tolist(),              # Convert pandas columns to plain Python lists,
                             df['timestamp'].tolist())               # then run the crash detection.
    
    if crashes:                                                      # If we found any crashes…
        for crash in crashes:                                        # Loop through each flagged crash.
            i, prev, curr, timestamp = crash                         # Unpack the saved tuple.
            plt.plot(timestamp, curr, 'ro', markersize=10)           # Draw a big red dot at the crash point.
            plt.annotate(f'Crash: {prev} to {curr}km/h',             # Add a text label near the dot:
                         (timestamp, curr),                           # anchor at the crash point,
                         textcoords="offset points",                  # position text by pixel offset,
                         xytext=(0,15),                               # 15 pixels above the point,
                         ha='center',                                 # center the text horizontally,
                         fontsize=10,                                 # smallish font,
                         color='red',                                 # red text,
                         weight='bold')                               # bold weight for emphasis.
    
    plt.title('Vehicle Speed Over Time with Crash Detection',         # Graph title.
              fontsize=14, weight='bold')
    plt.xlabel('Timestamp', fontsize=12)                              # X-axis label.
    plt.ylabel('Speed (km/h)', fontsize=12)                           # Y-axis label.
    plt.grid(True, alpha=0.3)                                         # Light grid for readability.
    plt.xticks(rotation=45)                                           # Rotate x labels so they don’t overlap.
    plt.tight_layout()                                                # Auto-fit everything nicely within the figure.
    plt.show()                                                        # Display the graph (usually blocks until closed).

    # ---- Write results on the Turtle window as big, readable text ----
    pen = turtle.Turtle()                                             # Create a drawing “pen”.
    pen.hideturtle()                                                  # Hide the arrow icon; we only want text.
    pen.penup()                                                       # Don’t draw lines when moving the pen.
    pen.color("red")                                                  # Default text color red (for alerts).
    pen.goto(0, 200)                                                  # Move to near the top-center of the window.

    if crashes:                                                       # If there are crashes to report…
        y_position = 200                                              # Start printing from y=200 and go downward.
        for crash in crashes:                                         # For each crash…
            i, prev, curr, timestamp = crash                          # Unpack the details.
            
            pen.goto(0, y_position)                                   # Move to current y position.
            pen.write("CRASH SUSPECTED!",                             # Big alert headline.
                      align="center", font=("Arial", 45, "bold"))
            
            y_position -= 40                                          # Step down for the next line.
            pen.goto(0, y_position)
            pen.write(f"Time: {timestamp}",                           # Show the time the drop occurred.
                      align="center", font=("Arial", 28, "bold"))
            
            y_position -= 30
            pen.goto(0, y_position)
            pen.write(f"Speed dropped from {prev} to {curr} km/h",    # Show before/after speeds.
                      align="center", font=("Arial", 28, "bold"))
            
            y_position -= 30
            pen.goto(0, y_position)
            pen.write(f"Impact: {prev-curr} km/h drop",               # Show magnitude of the drop.
                      align="center", font=("Arial", 28, "bold"))
            
            y_position -= 50                                          # Leave extra space before next crash block.
    else:
        pen.goto(0, 0)                                                # Center of the window.
        pen.color("green")                                            # Green to indicate all clear.
        pen.write("No crash events detected",                         # Friendly no-crash message.
                  align="center", font=("Arial", 24, "bold"))
    
    # ---- Also print a neat summary to the console ----
    print("\n" + "="*50)                                              # Separator line (50 '=' symbols).
    print("CRASH ANALYSIS RESULTS")                                   # Section header.
    print("="*50)                                                     # Another separator.
    if crashes:
        for i, crash in enumerate(crashes, 1):                        # Number crashes 1,2,3,… for printing.
            i, prev, curr, timestamp = crash                          # (Note: reuses variable name 'i'. See note below.)
            print(f"Crash #{i}:")                                     # Prints "Crash #<index>" (but see note below).
            print(f"  Time: {timestamp}")                             # Time string.
            print(f"  Speed dropped from {prev} to {curr} km/h")      # From-to speeds.
            print(f"  Impact: {prev-curr} km/h drop")                 # Magnitude of drop.
            print()                                                   # Blank line between crashes.
    else:
        print("No crash events detected")                             # Console message if none.
    print("="*50)                                                     # Closing separator.


screen.ontimer(transition, 4500)                                      # Schedule transition() to run after 4500 ms (4.5 s).

try:
    screen.mainloop()                                                 # Start Turtle’s event loop (keeps window alive).
except:
    print("Turtle window closed")                                      # If user closes abruptly, avoid a crash and print.
