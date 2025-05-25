import random
from datetime import datetime
import pandas as pd
import os

class RPSGame:
    def __init__(self):
        self.game_history = []
        self.move_counts = {'rock': 0, 'paper': 0, 'scissors': 0}
        self.win_rates = [0]  # Initialize with 0
        self.wins = 0
        self.total_games = 0
        self.current_user = None
        self.data_file = "game_data.xlsx"
        
        # Create data file if it doesn't exist
        if not os.path.exists(self.data_file):
            df = pd.DataFrame(columns=["username", "total_games", "wins", "rock", "paper", "scissors"])
            df.to_excel(self.data_file, index=False)
        
        # Create history file if it doesn't exist
        if not os.path.exists("game_history.xlsx"):
            df = pd.DataFrame(columns=["username", "datetime", "player", "computer", "result"])
            df.to_excel("game_history.xlsx", index=False)

    def set_user(self, username):
        """Set the current user and load their stats"""
        self.current_user = username
        
        # Load user stats from Excel
        df = pd.read_excel(self.data_file)
        user_row = df[df["username"] == username]
        
        if len(user_row) > 0:
            self.total_games = user_row["total_games"].values[0]
            self.wins = user_row["wins"].values[0]
            self.move_counts["rock"] = user_row["rock"].values[0]
            self.move_counts["paper"] = user_row["paper"].values[0]
            self.move_counts["scissors"] = user_row["scissors"].values[0]
            
            # Calculate win rate
            if self.total_games > 0:
                win_rate = (self.wins / self.total_games) * 100
                self.win_rates = [0, win_rate]  # Simplified trend
        else:
            # New user, initialize stats
            self.total_games = 0
            self.wins = 0
            self.move_counts = {'rock': 0, 'paper': 0, 'scissors': 0}
            self.win_rates = [0]
            
            # Add user to dataframe
            new_user = {
                "username": username,
                "total_games": 0,
                "wins": 0,
                "rock": 0,
                "paper": 0,
                "scissors": 0
            }
            df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
            df.to_excel(self.data_file, index=False)
        
        # Load user history
        history_df = pd.read_excel("game_history.xlsx")
        self.game_history = history_df[history_df["username"] == username].to_dict("records")

    def play(self, player_choice):
        """Play a round and save results to Excel"""
        if not self.current_user:
            return None, None
            
        choices = ['rock', 'paper', 'scissors']
        computer_choice = random.choice(choices)
        
        # Update move counts
        self.move_counts[player_choice.lower()] += 1
        
        # Determine winner
        if player_choice == computer_choice:
            result = 'ties'
        elif (
            (player_choice == 'rock' and computer_choice == 'scissors') or
            (player_choice == 'paper' and computer_choice == 'rock') or
            (player_choice == 'scissors' and computer_choice == 'paper')
        ):
            result = 'wins'
            self.wins += 1
        else:
            result = 'losses'
        
        self.total_games += 1
        
        # Calculate and store win rate
        win_rate = (self.wins / self.total_games) * 100 if self.total_games > 0 else 0
        self.win_rates.append(win_rate)
        
        # Record game in history
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update Excel data
        # 1. Update user stats
        df = pd.read_excel(self.data_file)
        df.loc[df["username"] == self.current_user, "total_games"] = self.total_games
        df.loc[df["username"] == self.current_user, "wins"] = self.wins
        df.loc[df["username"] == self.current_user, "rock"] = self.move_counts["rock"]
        df.loc[df["username"] == self.current_user, "paper"] = self.move_counts["paper"]
        df.loc[df["username"] == self.current_user, "scissors"] = self.move_counts["scissors"]
        df.to_excel(self.data_file, index=False)
        
        # 2. Add to history
        history_df = pd.read_excel("game_history.xlsx")
        new_record = {
            "username": self.current_user,
            "datetime": timestamp,
            "player": player_choice,
            "computer": computer_choice,
            "result": result
        }
        history_df = pd.concat([history_df, pd.DataFrame([new_record])], ignore_index=True)
        history_df.to_excel("game_history.xlsx", index=False)
        
        # Add to in-memory history
        self.game_history.append(new_record)
        
        return computer_choice, result

    def get_stats(self):
        win_rate = f"{(self.wins / self.total_games * 100):.1f}%" if self.total_games > 0 else "0.0%"
        return {
            'total_games': self.total_games,
            'wins': self.wins,
            'win_rate': win_rate
        }

    def get_move_distribution(self):
        return {k.capitalize(): v for k, v in self.move_counts.items()}

    def get_winrate_trend(self):
        return self.win_rates
