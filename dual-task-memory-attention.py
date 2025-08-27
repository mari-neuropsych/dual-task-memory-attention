import tkinter as tk
import random
import time
import numpy as np

class DualTask:
    def __init__(self, master, n=2, sequence_length=15, target_chance=0.3):
        self.master = master
        self.n = n
        self.sequence_length = sequence_length
        self.current_index = 0
        self.user_responses = []
        self.target_chance = target_chance

        self.sequence = [random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(sequence_length)]
        self.label = tk.Label(master, text="", font=("Arial", 48))
        self.label.pack(padx=20, pady=20)

        self.button = tk.Button(master, text="Click if TARGET!", width=20, height=3,
                                command=self.record_target)
        self.button.pack(pady=10)

        self.results = []
        self.show_next_stimulus()

    def generate_synthetic_eeg(self, length=100):
        t = np.linspace(0, 1, length)
        signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(length)
        return signal

    def show_next_stimulus(self):
        if self.current_index < self.sequence_length:
            self.is_target = random.random() < self.target_chance
            self.current_stimulus = self.sequence[self.current_index]
            display_text = self.current_stimulus
            if self.is_target:
                display_text += " (TARGET)"
            self.label.config(text=display_text)
            self.start_time = time.time()
            self.current_eeg = self.generate_synthetic_eeg()
            self.master.after(1000, self.end_trial)
        else:
            self.show_results()

    def record_target(self):
        reaction_time = time.time() - self.start_time
        self.user_responses.append({
            "trial": self.current_index+1,
            "stimulus": self.current_stimulus,
            "target": self.is_target,
            "clicked": True,
            "reaction_time": reaction_time,
            "eeg_signal": self.current_eeg.tolist()
        })

    def end_trial(self):
        # Record no-click if participant didn't respond
        if len(self.user_responses) < self.current_index + 1:
            self.user_responses.append({
                "trial": self.current_index+1,
                "stimulus": self.current_stimulus,
                "target": self.is_target,
                "clicked": False,
                "reaction_time": None,
                "eeg_signal": self.current_eeg.tolist()
            })
        self.current_index += 1
        self.show_next_stimulus()

    def show_results(self):
        self.label.config(text="Task Complete!")
        self.button.config(state="disabled")
        print("Trial | Stimulus | Target | Clicked | Reaction Time")
        for r in self.user_responses:
            print(f"{r['trial']} | {r['stimulus']} | {r['target']} | {r['clicked']} | {r['reaction_time']}")
        print("\nSynthetic EEG data for each trial is available in 'eeg_signal' field.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Dual Task – Memory & Attention Challenge")
    app = DualTask(root)
    root.mainloop()
