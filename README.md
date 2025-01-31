# WuWa-Simulator
This program is simulates Wuthering Waves game pulling results under mathematical basis.

# Installation
Requirements:

Python 3.x
Tkinter (typically bundled with Python)
Clone or Download the Repository:

git clone https://your-repository-url.git
cd gacha-simulator

Running the Program
Run the simulator by executing the main Python file:
python your_script_name.py
This command will launch the GUI for the gacha simulator.

# User Interface
Pull Buttons:

Single Pull: Click to perform one pull.
10 Pulls: Click to perform 10 consecutive pulls.
The results are displayed using the following mappings:

"3*" → 3★

"4*" → 4★

"5*" → 5★

"featured 5*" → up!5★

History:

Click the History button to open a window displaying the pull history summary.
The summary includes the total number of pulls and the count for each rarity.
Within the history window, a Reset History button allows you to clear all previous pull data.
Probability Calculation:

Click the Calculate Probability button to open a window where you can enter:
The planned number of pulls.
The target number of featured 5★ (up!5★) pulls.
The simulator then uses Monte Carlo simulation to estimate the probability of reaching the target.
