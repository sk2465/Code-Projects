import tkinter as tk
import random
import requests
import pandas as pd
from RandPlayers import new_player
import os



class Higher_or_Lower:
    def __init__(self, master):
        self.master = master
        self.master.title("Higher or Lower Game")
        self.score = 0
        self.current_player = new_player()
        self.player_name, self.player_points, self.player_year = self.current_player
        self.next_player = new_player()
        self.new_player_name, self.new_player_points, self.new_player_year = self.next_player

        self.label = tk.Label(master, text=f"Does {self.player_name} from {self.player_year} score Higher or Lower than {self.new_player_name} from {self.new_player_year}", font=('Arial', 16))
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)

        self.higher_button = tk.Button(self.button_frame, text="Higher", command=self.check_higher, width=10)
        self.higher_button.pack(side=tk.LEFT, padx=10)
        self.lower_button = tk.Button(self.button_frame, text="Lower", command=self.check_lower, width=10)
        self.lower_button.pack(side=tk.LEFT, padx=10)

        self.score_label = tk.Label(master, text=f"Current score: {self.score}", font=('Arial', 14))
        self.label.pack(pady=20)

        self.final_score_label = tk.Label(master, text="", font=('Arial', 14))
        self.final_score_label.pack(pady=20)

    def new_player(self):
        self.player_name, self.player_points, self.player_year = self.current_player
        self.current_player = self.next_player
        self.next_player = new_player()
        self.new_player_name, self.new_player_points, self.new_player_year = self.next_player
        self.label.config(text=f"{self.current_player} from {self.player_year}")
    
    def check_higher(self):
        if self.player_points > self.new_player_points:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.new_player()
        else:
            self.game_over()
    
    def check_lower(self):
        if self.player_points < self.new_player_points:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.new_player()
        else:
            self.game_over()
    
    def game_over(self):
        self.label.config(text="Game Over!")
        self.higher_button.config(state=tk.DISABLED)
        self.lower_button.config(state=tk.DISABLED)
        self.final_score_label.config(text=f"Final Score: {self.score}")
    
    def restart():
        root.destroy()
        os.startfile("main.py")


if __name__ == "__main__":
    root = tk.Tk()
    game = Higher_or_Lower(root)
    root.geometry("300x300")
    root.mainloop()

