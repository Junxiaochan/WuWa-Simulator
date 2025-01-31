import tkinter as tk
from tkinter import messagebox
import random

class GachaSimulator:
    def __init__(self, base_4_rate=0.085, featured_rate=0.5):
        """
        Initialize the simulator.
          - 5★ probability is determined by the soft pity mechanism:
              • Pull 1–65: fixed at 0.8% (0.008)
              • Pull 66–70: each pull increases the rate by 4% (0.04) over the base
              • Pull 71–75: each pull increases the rate by 8% (0.08) over the previous pull
              • Pull 76–78: each pull increases the rate by 10% (0.10) over the previous pull
              • Pull 79: 100% chance
          - 4★: no soft pity. However, if 9 consecutive pulls yield no 4★ or 5★, the 10th pull (if not 5★) is forced to be 4★.
          - featured_rate applies to any 5★ pull: if the 50-50 check is lost, the next 5★ is guaranteed featured.
        """
        self.base_4_rate = base_4_rate
        self.featured_rate = featured_rate
        self.history = []            # List of pull outcomes
        self.pity_5_counter = 0      # Pulls since last 5★ (for soft pity)
        self.pity_4_counter = 0      # Pulls since last 4★ or higher
        self.guaranteed_featured = False  # Flag: next 5★ is forced to be featured if previous 5★ lost the 50-50

    def get_current_5_rate(self):
        """
        Determine the current 5★ rate based on the number of pulls since the last 5★.
        """
        pull_number = self.pity_5_counter + 1
        if pull_number <= 65:
            return 0.008
        elif pull_number <= 70:
            # Each pull from 66 to 70 increases by 4%
            return 0.008 + (pull_number - 65) * 0.04
        elif pull_number <= 75:
            # Pulls 71 to 75: add 8% per pull (after the first 5 pulls of +4%)
            return 0.008 + 5 * 0.04 + (pull_number - 70) * 0.08
        elif pull_number <= 78:
            # Pulls 76 to 78: add 10% per pull (after previous increases)
            return 0.008 + 5 * 0.04 + 5 * 0.08 + (pull_number - 75) * 0.10
        else:
            # 79th pull and beyond: guaranteed 5★
            return 1.0

    def pull(self):
        """
        Simulate a single pull with the following order:
          1. Roll for 5★ using soft pity.
          2. If no 5★ is obtained, check if 9 consecutive pulls without 4★ or higher have occurred; if so, force a 4★.
          3. Otherwise, roll for 4★ using the fixed probability.
          4. If neither 5★ nor 4★ is obtained, return 3★.
        Returns one of: "3*", "4*", "5*", or "featured 5*".
        """
        # --- Roll for 5★ first ---
        current_5_rate = self.get_current_5_rate()
        roll = random.random()
        if roll < current_5_rate:
            # 5★ obtained; reset pity counters.
            self.pity_5_counter = 0
            self.pity_4_counter = 0
            if self.guaranteed_featured:
                result = "featured 5*"
                self.guaranteed_featured = False
            else:
                if random.random() < self.featured_rate:
                    result = "featured 5*"
                else:
                    result = "5*"
                    # Lost the 50-50, so next 5★ will be featured.
                    self.guaranteed_featured = True
            self.history.append(result)
            return result
        else:
            # No 5★: increment 5★ pity.
            self.pity_5_counter += 1

            # --- Check 4★ pity: if 9 pulls without 4★ or higher, force a 4★ on the 10th pull.
            if self.pity_4_counter == 9:
                result = "4*"
                self.pity_4_counter = 0
                self.history.append(result)
                return result
            else:
                # Roll for 4★ using the fixed rate.
                if random.random() < self.base_4_rate:
                    result = "4*"
                    self.pity_4_counter = 0
                    self.history.append(result)
                    return result
                else:
                    # Neither 5★ nor 4★: outcome is 3★.
                    self.pity_4_counter += 1
                    result = "3*"
                    self.history.append(result)
                    return result

    def multi_pull(self, count=10):
        """
        Perform 10 pulls and return the list of outcomes.
        """
        results = []
        for _ in range(count):
            results.append(self.pull())
        return results

    def reset_history(self):
        """
        Reset pull history and pity counters.
        """
        self.history = []
        self.pity_5_counter = 0
        self.pity_4_counter = 0
        self.guaranteed_featured = False

    def get_summary(self):
        """
        Return a summary of the pull history including counts for each outcome and total pulls.
        """
        summary = {"3*": 0, "4*": 0, "5*": 0, "featured 5*": 0}
        for result in self.history:
            if result in summary:
                summary[result] += 1
        total_pulls = sum(summary.values())
        summary["Total Pulls"] = total_pulls
        return summary

    @staticmethod
    def simulate_probability(num_pulls, target_featured, num_simulations=10000, simulator_params=None):
        """
        Estimate the probability of obtaining at least 'target_featured' featured 5★ (up!5★) 
        in 'num_pulls' pulls using Monte Carlo simulation.
        """
        success_count = 0
        for _ in range(num_simulations):
            if simulator_params is None:
                sim = GachaSimulator()
            else:
                sim = GachaSimulator(**simulator_params)
            featured_count = 0
            for i in range(num_pulls):
                result = sim.pull()
                if result == "featured 5*":
                    featured_count += 1
            if featured_count >= target_featured:
                success_count += 1
        return success_count / num_simulations

# Mapping function for display conversion
def map_result(result):
    mapping = {
        "3*": "3★",
        "4*": "4★",
        "5*": "5★",
        "featured 5*": "up!5★"
    }
    return mapping.get(result, result)

# --- UI Implementation using Tkinter ---
class GachaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gacha Simulator")
        self.geometry("900x300")
        self.simulator = GachaSimulator()

        # Create buttons for pulling and other functions.
        btn_single = tk.Button(self, text="Single Pull", command=self.single_pull)
        btn_single.pack(pady=5)
        
        btn_ten = tk.Button(self, text="10 Pulls", command=self.ten_pulls)
        btn_ten.pack(pady=5)

        btn_history = tk.Button(self, text="History", command=self.show_history)
        btn_history.pack(pady=5)

        btn_probability = tk.Button(self, text="Calculate Probability", command=self.show_probability_window)
        btn_probability.pack(pady=5)

        self.result_label = tk.Label(self, text="Result: ", font=("Arial", 14))
        self.result_label.pack(pady=10)

    def single_pull(self):
        result = self.simulator.pull()
        display_result = map_result(result)
        self.result_label.config(text=f"Result: {display_result}")

    def ten_pulls(self):
        results = self.simulator.multi_pull(10)
        display_results = ", ".join(map(map_result, results))
        self.result_label.config(text=f"Results: {display_results}")

    def show_history(self):
        summary = self.simulator.get_summary()
        history_text = f"Total Pulls: {summary['Total Pulls']}\n"
        history_text += f"3★: {summary.get('3*', 0)}\n"
        history_text += f"4★: {summary.get('4*', 0)}\n"
        history_text += f"5★: {summary.get('5*', 0)}\n"
        history_text += f"up!5★: {summary.get('featured 5*', 0)}\n"
        
        # Create a new window to display history.
        history_window = tk.Toplevel(self)
        history_window.title("Pull History")
        history_window.geometry("250x200")
        
        lbl_history = tk.Label(history_window, text=history_text, justify=tk.LEFT)
        lbl_history.pack(pady=10)

        # Reset History button inside the history window.
        btn_reset = tk.Button(history_window, text="Reset History", command=lambda: self.reset_history(history_window))
        btn_reset.pack(pady=5)

    def reset_history(self, window):
        self.simulator.reset_history()
        messagebox.showinfo("Reset", "Pull history has been reset.")
        window.destroy()

    def show_probability_window(self):
        # Create a new window for probability calculation.
        prob_window = tk.Toplevel(self)
        prob_window.title("Calculate Probability")
        prob_window.geometry("300x200")

        lbl_info = tk.Label(prob_window, text="Enter planned pulls and target up!5★:")
        lbl_info.pack(pady=5)

        frame = tk.Frame(prob_window)
        frame.pack(pady=5)

        lbl_pulls = tk.Label(frame, text="Planned Pulls:")
        lbl_pulls.grid(row=0, column=0, padx=5, pady=5)
        entry_pulls = tk.Entry(frame)
        entry_pulls.grid(row=0, column=1, padx=5, pady=5)

        lbl_target = tk.Label(frame, text="Target up!5★:")
        lbl_target.grid(row=1, column=0, padx=5, pady=5)
        entry_target = tk.Entry(frame)
        entry_target.grid(row=1, column=1, padx=5, pady=5)

        result_label = tk.Label(prob_window, text="")
        result_label.pack(pady=5)

        def calculate():
            try:
                num_pulls = int(entry_pulls.get())
                target = int(entry_target.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid integer values.")
                return
            probability = GachaSimulator.simulate_probability(num_pulls, target)
            result_label.config(text=f"Probability: {probability*100:.2f}%")
        
        btn_calc = tk.Button(prob_window, text="Calculate", command=calculate)
        btn_calc.pack(pady=5)

if __name__ == "__main__":
    app = GachaApp()
    app.mainloop()
