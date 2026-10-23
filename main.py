# Teddy Rodd Lab 4

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import random

# Make our simulation repeatable
random.seed(42)

# Store all player records here
players = []

# Generate data for 200 players
for i in range(1, 201):
    difficulty = random.choice(["Easy", "Hard"])

    if difficulty == "Easy":
        survival_time = random.uniform(10, 30)
        lives_lost = random.randint(0, 2)
        player_score = random.randint(500, 1000)
        enemies_defeated = random.randint(20, 50)
    else:
        survival_time = random.uniform(1, 20)
        lives_lost = random.randint(2, 5)
        player_score = random.randint(100, 700)
        enemies_defeated = random.randint(0, 35)

    player = {
        "Player_ID": f"P{i:03d}",
        "Difficulty": difficulty,
        "Survival_Time": round(survival_time, 1),
        "Lives_Lost": lives_lost,
        "Player_Score": player_score,
        "Enemies_Defeated": enemies_defeated
    }

    players.append(player)

# Convert the records into a table
df = pd.DataFrame(players)

# Save the table as a CSV file
df.to_csv("zombie_survival.csv", index=False)

# Used commented code bellow during testing...
# Display the first five rows
#print(df.head())

# Display the number of player records
#print("Total players:", len(df))

df = pd.read_csv("zombie_survival.csv")

sns.set_theme(style="darkgrid")

# Chart numero uno
plt.figure(figsize=(9,5))

sns.histplot(
    data=df,
    x="Enemies_Defeated",
    y="Difficulty",
    hue="Difficulty",
    kde=True
)

plt.title("Zombie Kills Easy vs. Hard")
plt.xlabel("Kills)")
plt.ylabel("Difficulty")
plt.tight_layout()
plt.savefig("kills_histogram.png")
plt.show()

# Chart Numero Dose
plt.figure(figsize=(8,5))

sns.boxplot(
    data=df,
    x="Difficulty",
    y = "Survival_Time",
    hue="Difficulty"
)

plt.title("Survival Time: Easy vs. Hard")
plt.xlabel("Game Difficulty")
plt.ylabel("Survival Time (minutes)")
plt.tight_layout()
plt.savefig("Survival_boxplot.png")
plt.show()


# Animation: Players surviving over time

# Create time points from minute 0 through minute 30
times = list(range(31))

# Count how many players are still alive at each time
survivors = [
    (df["Survival_Time"] > t).sum()
    for t in times
]

# Create the animation chart
fig, ax = plt.subplots(figsize=(9, 5))

line, = ax.plot([], [], color="green", linewidth=3)

ax.set_xlim(0, 30)
ax.set_ylim(0, 500)
ax.set_xlabel("Time Elapsed (minutes)")
ax.set_ylabel("Players Still Alive")
ax.set_title("Zombie Outbreak: Player Survival Over Time")
ax.grid(True)

# Prepare the chart before the animation begins
def init():
    line.set_data([], [])
    return line,

# Update the line for each animation frame
def update(frame):
    line.set_data(times[:frame + 1], survivors[:frame + 1])
    return line,

# Create the animation
ani = FuncAnimation(
    fig,
    update,
    frames=len(times),
    init_func=init,
    interval=200,
    blit=True,
    repeat=False
)

plt.tight_layout()

# Saves as a GIF
ani.save("zombie_survival.gif",writer="pillow", fps=5)
print("Animation saved as zombie_survival.gif")

plt.show()