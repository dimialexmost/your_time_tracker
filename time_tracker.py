import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import json
import os
import subprocess
from tkinter import filedialog
import threading
from datetime import datetime, timedelta

class TimeTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Your Time Tracker")
        root.resizable(False, False)

        # Widgets
        self.date_label = ttk.Label(root, text="Date:")
        self.date_label.grid(row=0, column=0)

        self.date_entry = DateEntry(root, date_pattern='dd.mm.yyyy')
        self.date_entry.grid(row=0, column=1)

        self.start_label = ttk.Label(root, text="Start time:")
        self.start_label.grid(row=1, column=0)

        self.start_hour = ttk.Spinbox(root, from_=0, to=23, width=3, format="%02.0f")
        self.start_hour.grid(row=1, column=1)
        self.start_minute = ttk.Spinbox(root, from_=0, to=59, width=3, format="%02.0f")
        self.start_minute.grid(row=1, column=2)

        self.end_label = ttk.Label(root, text="End time:")
        self.end_label.grid(row=2, column=0)

        self.end_hour = ttk.Spinbox(root, from_=0, to=23, width=3, format="%02.0f")
        self.end_hour.grid(row=2, column=1)
        self.end_minute = ttk.Spinbox(root, from_=0, to=59, width=3, format="%02.0f")
        self.end_minute.grid(row=2, column=2)

        self.program_label = ttk.Label(root, text="Select controlled program:")
        self.program_label.grid(row=4, column=0)

        self.total_days_result_label = ttk.Label(root, text="")
        self.total_days_result_label.grid(row=11, column=1, columnspan=2)

        self.program_entry = ttk.Entry(root, width=30)
        self.program_entry.grid(row=4, column=1)

        self.browse_button = ttk.Button(root, text="Browse...", command=self.browse_program)
        self.browse_button.grid(row=4, column=2)

        self.start_program_button = ttk.Button(root, text="Run the program", command=self.start_saved_program_thread)
        self.start_program_button.grid(row=4, column=3)

        self.result_text = tk.Text(root, height=20, width=55)
        self.result_text.grid(row=7, column=0, columnspan=4)
        self.result_text.tag_configure("bold", font=("Arial", 10, "bold"))

        self.save_button = ttk.Button(root, text="Save statistics", command=self.save_statistics)
        self.save_button.grid(row=6, column=0, columnspan=4)

        self.save_directory_label = ttk.Label(root, text="Statistics saving folder:")
        self.save_directory_label.grid(row=5, column=0)

        self.save_directory_entry = ttk.Entry(root, width=30)
        self.save_directory_entry.grid(row=5, column=1)

        self.browse_directory_button = ttk.Button(root, text="Browse...", command=self.browse_directory)
        self.browse_directory_button.grid(row=5, column=2)

        self.program_path = self.load_program_path()
        self.save_directory = self.load_save_directory()

        if self.program_path:
            self.program_entry.insert(0, self.program_path)
            self.start_saved_program_thread()

        if self.save_directory:
            self.save_directory_entry.insert(0, self.save_directory)
            self.load_statistics_from_saved_path()

        self.calculate_total_time()
        self.calculate_average_time()
        self.calculate_last_month_time()

    def start_saved_program_thread(self):
        if self.program_path and os.path.exists(self.program_path):
            threading.Thread(target=self.start_saved_program).start()
        else:
            print("The program file was not found.")

    def start_saved_program(self):
        if self.program_path and os.path.exists(self.program_path):
            subprocess.Popen(self.program_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        else:
            print("The program file was not found.")

    def save_statistics(self):
        data = {}
        save_directory = self.save_directory_entry.get()
        save_path = os.path.join(save_directory, "statistics.json")

        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                data = json.load(f)

        date = self.date_entry.get()
        start = f"{self.start_hour.get()}.{self.start_minute.get()}"
        end = f"{self.end_hour.get()}.{self.end_minute.get()}"

        # Check for empty data
        if not date or not start or not end:
            print("Please enter valid date and time.")
            return

        # Check for duplicate data
        if date in data:
            for item in data[date]:
                if item["start"] == start and item["end"] == end:
                    print("Data with the same start and end times already exists.")
                    return

        # Check for invalid hours and minutes
        if int(self.start_hour.get()) > 23 or int(self.start_minute.get()) > 59 or int(self.end_hour.get()) > 23 or int(self.end_minute.get()) > 59:
            print("Invalid time input. Hours should be between 0 and 23, and minutes should be between 0 and 59.")
            return

        if date not in data:
            data[date] = []

        data[date].append({"start": start, "end": end})

        with open(save_path, "w") as f:
            json.dump(data, f)

        self.save_stat_path_to_file(save_directory)
        self.load_statistics_from_saved_path()
        self.calculate_total_time()
        self.calculate_average_time()

    def browse_program(self):
        file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])
        if file_path:
            self.program_path = file_path
            self.program_entry.delete(0, tk.END)
            self.program_entry.insert(0, self.program_path)
            self.save_program_path(self.program_path)

    def load_program_path(self):
        if os.path.exists("program_path.txt"):
            with open("program_path.txt", "r") as f:
                return f.read().strip()
        return None

    def save_program_path(self, program_path):
        with open("program_path.txt", "w") as f:
            f.write(program_path)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory_entry.delete(0, tk.END)
            self.save_directory_entry.insert(0, directory)
            self.save_save_directory(directory)

    def load_save_directory(self):
        if os.path.exists("save_directory.txt"):
            with open("save_directory.txt", "r") as f:
                return f.read().strip()
        return None

    def save_save_directory(self, save_directory):
        with open("save_directory.txt", "w") as f:
            f.write(save_directory)

    def load_statistics_from_saved_path(self):
        save_directory = self.save_directory_entry.get()
        save_path = os.path.join(save_directory, "statistics.json")

        if not os.path.exists(save_path):
            return

        with open(save_path, "r") as f:
            data = json.load(f)

        # Sort the dictionary by dates in descending order
        sorted_data = dict(sorted(data.items(), key=lambda item: datetime.strptime(item[0], "%d.%m.%Y"), reverse=True))

        self.result_text.delete(1.0, tk.END)
        for date, items in sorted_data.items():
            self.result_text.insert(tk.END, f"{date}:\n", "bold")  # use the "bold" tag

            total_minutes_for_date = 0  # Initialize common time for date
            for item in items:
                self.result_text.insert(tk.END, f"  Start: {item['start']} - End: {item['end']}\n")

                # Calculate the total time for a date
                start_time = item["start"].split('.')
                end_time = item["end"].split('.')
                start_hours, start_minutes = int(start_time[0]), int(start_time[1])
                end_hours, end_minutes = int(end_time[0]), int(end_time[1])
                total_minutes_for_date += (end_hours * 60 + end_minutes) - (start_hours * 60 + start_minutes)

            # Add the total time after all elements for the date
            total_hours_for_date = total_minutes_for_date // 60
            total_minutes_for_date %= 60
            self.result_text.insert(tk.END, f"Total on this day: {total_hours_for_date} hr. {total_minutes_for_date} min.\n\n")  # Added





    def save_stat_path_to_file(self, path):
        with open("stat_path.txt", "w") as f:
            f.write(path)

    def calculate_total_time(self):
        data = self.load_statistics()
        total_hours = 0
        total_minutes = 0
        earliest_date = None

        for date_str, items in data.items():
            date = datetime.strptime(date_str, "%d.%m.%Y")
            if earliest_date is None or date < earliest_date:
                earliest_date = date

        if earliest_date is not None:
            today = datetime.today()
            total_days = (today - earliest_date).days  # Calculate the total days

            for date_str, items in data.items():
                date = datetime.strptime(date_str, "%d.%m.%Y")
                if earliest_date <= date <= today:
                    for item in items:
                        start_time = item["start"].split('.')
                        end_time = item["end"].split('.')
                        start_hours, start_minutes = int(start_time[0]), int(start_time[1])
                        end_hours, end_minutes = int(end_time[0]), int(end_time[1])

                        total_hours += end_hours - start_hours
                        total_minutes += end_minutes - start_minutes

            total_hours += total_minutes // 60
            total_minutes %= 60

            total_time_label = ttk.Label(self.root, text=f"Total time from {earliest_date.strftime('%d.%m.%Y')}: {total_hours} hr. {total_minutes} min.")
            total_time_label.grid(row=8, column=0, columnspan=4)
            total_days_with_session_label = ttk.Label(self.root, text=f"Total days with sessions from {earliest_date.strftime('%d.%m.%Y')}: {len(data)} days")
            total_days_with_session_label.grid(row=10, column=0, columnspan=4)
            total_days_label = ttk.Label(self.root, text=f"Total days since start from {earliest_date.strftime('%d.%m.%Y')}: {total_days} days")
            total_days_label.grid(row=9, column=0, columnspan=4)
            self.total_days_result_label.config(text=f"{total_days} days")  # Update the total days label
        else:
            total_time_label = ttk.Label(self.root, text="No data available.")
            total_time_label.grid(row=8, column=0, columnspan=4)
            self.total_days_result_label.config(text="0 days")  # Update the total days label

    from datetime import datetime, timedelta

    def calculate_last_month_time(self):
        data = self.load_statistics()
        total_hours = 0
        total_minutes = 0
        today = datetime.today()
        last_month_start = today.replace(day=1) - timedelta(days=1)
        last_month_end = last_month_start.replace(day=1)

        for date_str, items in data.items():
            date = datetime.strptime(date_str, "%d.%m.%Y")
            if last_month_end <= date <= last_month_start:
                for item in items:
                    start_time = item["start"].split('.')
                    end_time = item["end"].split('.')
                    start_hours, start_minutes = int(start_time[0]), int(start_time[1])
                    end_hours, end_minutes = int(end_time[0]), int(end_time[1])

                    total_hours += end_hours - start_hours
                    total_minutes += end_minutes - start_minutes

        total_hours += total_minutes // 60
        total_minutes %= 60

        total_last_month_time_label = ttk.Label(self.root, text=f"Total time for the last month ({last_month_start.strftime('%m.%Y')}): {total_hours} hr. {total_minutes} min.")
        total_last_month_time_label.grid(row=12, column=0, columnspan=4)


    def calculate_average_time(self):
        data = self.load_statistics()
        total_days = len(data)
        total_minutes = 0

        if total_days > 0:
            for date_str, items in data.items():
                for item in items:
                    start_time = item["start"].split('.')
                    end_time = item["end"].split('.')
                    start_hours, start_minutes = int(start_time[0]), int(start_time[1])
                    end_hours, end_minutes = int(end_time[0]), int(end_time[1])

                    total_minutes += (end_hours * 60 + end_minutes) - (start_hours * 60 + start_minutes)

            average_minutes = total_minutes // total_days

            # Calculate hours and remaining minutes
            average_hours = average_minutes // 60
            remaining_minutes = average_minutes % 60

            average_time_label = ttk.Label(self.root, text=f"Average time per day: {average_hours} hr. {remaining_minutes} min.")
            average_time_label.grid(row=11, column=0, columnspan=4)
            average_time_label.configure(background='#B3C2D7')

    def load_statistics(self):
        data = {}
        save_directory = self.save_directory_entry.get()
        save_path = os.path.join(save_directory, "statistics.json")

        if os.path.exists(save_path):
            with open(save_path, "r") as f:
                data = json.load(f)

        return data

root = tk.Tk()
app = TimeTracker(root)
root.mainloop()
