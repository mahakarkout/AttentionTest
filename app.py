import tkinter as tk
from tkinter import messagebox
import random
import time

class AttentionSwitchingExperiment:
    def __init__(self, root):
        self.root = root
        self.root.title("Attention Switching Experiment")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#d0e7f9")

        # Instructions before starting
        self.instructions = (
            "Welcome to the Attention Switching Experiment!\n\n"
            "Instructions:\n"
            "- A 'Green' or 'Red' light will appear.\n"
            "- If the light is Green, press 'Press Enter' quickly after seeing the White light.\n"
            "- If the light is Red, DO NOT press 'Press Enter' when the White light appears.\n"
            "- Your accuracy and speed will be measured.\n\n"
            "Click 'Start' to begin the experiment."
        )

        # GUI Elements
        self.top_frame = tk.Frame(root, bg="#d0e7f9")
        self.top_frame.pack(pady=10)

        self.label = tk.Label(self.top_frame, text=self.instructions, font=("Helvetica", 12), bg="#d0e7f9", wraplength=500, justify="left")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.button_frame = tk.Frame(root, bg="#d0e7f9")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_experiment, font=("Helvetica", 14), bg="green", fg="white", width=12)
        self.start_button.grid(row=0, column=0, padx=10)

        self.reaction_button = tk.Button(self.button_frame, text="Press Enter", state="disabled", command=self.record_reaction, font=("Helvetica", 14), bg="orange", fg="black", width=12)
        self.reaction_button.grid(row=0, column=1, padx=10)

        self.end_button = tk.Button(self.button_frame, text="End Experiment", command=self.end_experiment, font=("Helvetica", 14), bg="red", fg="white", width=15)
        self.end_button.grid(row=0, column=2, padx=10)

        # Canvas for Signal Lights
        self.canvas_frame = tk.Frame(root, bg="#d0e7f9")
        self.canvas_frame.pack(pady=30)

        self.canvas = tk.Canvas(self.canvas_frame, width=250, height=250, bg="#d0e7f9", highlightthickness=0)
        self.canvas.pack()

        # Create the light oval but keep it hidden initially
        self.light = self.canvas.create_oval(50, 50, 200, 200, fill="grey", state='hidden')  # Initially hidden

        # Result Table Frame
        self.results_frame = tk.Frame(root, bg="#d0e7f9")
        self.results_frame.pack(pady=20)

        # Experiment Variables
        self.num_stimuli = 10
        self.current_stimulus = 0
        self.correct_reactions = 0
        self.errors = 0
        self.total_time = 0
        self.pre_signal = ""
        self.start_time = 0
        self.user_pressed = False
        self.allowed_reaction_time = 1500  # in milliseconds
        self.reaction_timeout_id = None  # To keep track of the timeout event

    def start_experiment(self):
        # Reset variables
        self.correct_reactions = 0
        self.errors = 0
        self.total_time = 0
        self.current_stimulus = 0
        self.clear_results()  # Clear any previous results
        self.reaction_button.config(state="disabled")
        self.start_button.config(state="disabled")
        self.end_button.config(state="normal")

        # Update label for start message
        self.label.config(text="Experiment started! Please follow the signals.", fg="black")
        
        # Start the first signal
        self.next_signal()

    def next_signal(self):
        if self.current_stimulus < self.num_stimuli:
            # Choose pre-signal randomly (green or red)
            self.pre_signal = random.choice(['green', 'red'])
            self.current_stimulus += 1
            pre_signal_time = random.uniform(0.5, 2.0)

            # Show the light oval
            self.canvas.itemconfig(self.light, state='normal')

            # Display pre-signal light
            if self.pre_signal == 'green':
                self.canvas.itemconfig(self.light, fill="green")
                self.label.config(text="Green light! Get ready.", fg="black")
            else:
                self.canvas.itemconfig(self.light, fill="red")
                self.label.config(text="Red light! Wait...", fg="black")

            # Wait for a bit and then show the white signal
            self.root.after(int(pre_signal_time * 1000), self.show_white_signal)
        else:
            # Experiment is over, show results
            self.show_results()

    def show_white_signal(self):
        # Show the white signal and activate the reaction button
        self.canvas.itemconfig(self.light, fill="white")
        self.label.config(text="White signal! Respond accordingly.", fg="black")
        self.reaction_button.config(state="normal")
        self.start_time = time.time()
        self.user_pressed = False

        # Set up the reaction timeout
        self.reaction_timeout_id = self.root.after(self.allowed_reaction_time, self.reaction_timeout)

    def record_reaction(self):
        # Record that the user has pressed the button
        self.user_pressed = True

        # Disable the reaction button
        self.reaction_button.config(state="disabled")
        # Cancel the reaction timeout
        if self.reaction_timeout_id:
            self.root.after_cancel(self.reaction_timeout_id)
            self.reaction_timeout_id = None
        # Hide the light
        self.canvas.itemconfig(self.light, state='hidden')

        reaction_time = (time.time() - self.start_time)
        self.total_time += reaction_time

        # Determine correctness based on pre_signal
        if self.pre_signal == 'green':
            # User pressed the button within allowed time
            self.correct_reactions += 1
        elif self.pre_signal == 'red':
            # User should not have pressed the button
            self.errors += 1

        # Proceed to next signal after a short delay
        self.root.after(500, self.next_signal)  # 500 ms delay

    def reaction_timeout(self):
        # Disable the reaction button
        self.reaction_button.config(state="disabled")
        self.reaction_timeout_id = None
        # Hide the light
        self.canvas.itemconfig(self.light, state='hidden')

        # Determine correctness based on pre_signal
        if self.pre_signal == 'green':
            # User failed to press the button in time
            self.errors += 1
        elif self.pre_signal == 'red':
            # User correctly did not press the button
            self.correct_reactions += 1

        # Proceed to next signal after a short delay
        self.root.after(500, self.next_signal)  # 500 ms delay

    def show_results(self):
        # Cancel any pending timeouts
        if self.reaction_timeout_id:
            self.root.after_cancel(self.reaction_timeout_id)
            self.reaction_timeout_id = None

        # Disable buttons
        self.reaction_button.config(state="disabled")
        self.end_button.config(state="disabled")
        self.start_button.config(state="normal", text="Restart")

        # Hide the light
        self.canvas.itemconfig(self.light, state='hidden')

        # Calculate and display the results
        if self.correct_reactions != 0:
            avg_reaction_time = self.total_time / self.correct_reactions
        else:
            avg_reaction_time = 0

        if self.num_stimuli - self.errors != 0:
            PV = (self.num_stimuli / (self.num_stimuli - self.errors)) * avg_reaction_time
        else:
            PV = 0  # Avoid division by zero

        # Display results in a structured way in a table
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        result_labels = [
            ("Number of Correct Reactions:", self.correct_reactions),
            ("Number of Errors:", self.errors),
            ("Average Reaction Time (seconds):", f"{avg_reaction_time:.2f}"),
            ("Switching Attention Score (PV):", f"{PV:.2f}")
        ]

        for idx, (label_text, value) in enumerate(result_labels):
            tk.Label(self.results_frame, text=label_text, font=("Helvetica", 12), bg="#d0e7f9", anchor="w").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            tk.Label(self.results_frame, text=value, font=("Helvetica", 12, "bold"), bg="#d0e7f9", anchor="e").grid(row=idx, column=1, sticky="e", padx=10, pady=5)

        self.label.config(text="Experiment completed! See your results below.", fg="black")

    def end_experiment(self):
        # Confirm if the user wants to end the experiment early
        if messagebox.askyesno("End Experiment", "Are you sure you want to end the experiment?"):
            self.show_results()  # Display current results
            self.reaction_button.config(state="disabled")
            self.start_button.config(state="normal", text="Restart")
            self.end_button.config(state="disabled")

    def clear_results(self):
        # Clear any previous result labels
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.label.config(text="Experiment started! Please follow the signals.", fg="black")
        # Hide the light
        self.canvas.itemconfig(self.light, state='hidden')

# Main Application Loop
if __name__ == "__main__":
    root = tk.Tk()
    experiment = AttentionSwitchingExperiment(root)
    root.mainloop()
