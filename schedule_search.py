# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:29:21 2025

@author: croco
"""

import math

# Tasks dfinitions
tasks = [
    {"name": "τ1", "execution": 2, "period": 10},
    {"name": "τ2", "execution": 3, "period": 10},
    {"name": "τ3", "execution": 2, "period": 20},
    {"name": "τ4", "execution": 2, "period": 20},
    {"name": "τ5", "execution": 2, "period": 40},
    {"name": "τ6", "execution": 2, "period": 40},
    {"name": "τ7", "execution": 3, "period": 80},
]

# Job
def calculate_utilization(tasks):
    total_utilization = sum(task["execution"] / task["period"] for task in tasks)
    return total_utilization

# Schedulable
def check_schedulability(tasks):
    utilization = calculate_utilization(tasks)
    return utilization <= 1

# Hyperperiod (LCM)
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def find_hyperperiod(tasks):
    periods = [task["period"] for task in tasks]
    hyperperiod = periods[0]
    for period in periods[1:]:
        hyperperiod = lcm(hyperperiod, period)
    return hyperperiod

# FCFS
def non_preemptive_schedule(tasks, hyperperiod):
    schedule = []
    for t in tasks:
        for i in range(hyperperiod // t["period"]):
            schedule.append((t["name"], i * t["period"]))
    schedule.sort(key=lambda x: x[1])  # Trier par temps de début
    return schedule

import matplotlib.pyplot as plt

# Gantt graph
def plot_gantt(schedule, tasks):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    task_names = [task['name'] for task in tasks]
    task_indices = {name: idx for idx, name in enumerate(task_names)}
    
    current_time = 0
    for task_name, arrival_time in schedule:
        # Attention : chercher dans tasks (qui est une liste de dictionnaires)
        execution_time = next(t["execution"] for t in tasks if t["name"] == task_name)
        
        if current_time < arrival_time:
            current_time = arrival_time
        start = current_time
        duration = execution_time
        
        ax.broken_barh(
            [(start, duration)],
            (task_indices[task_name]*10, 9),
            facecolors='tab:blue'
        )
        current_time += duration

    ax.set_yticks([i*10 + 5 for i in range(len(task_names))])
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Time')
    ax.set_ylabel('Tasks')
    ax.set_title('Gantt graph')
    ax.grid(True)
    
    plt.show()

if check_schedulability(tasks):
    print("Schedulable.")
    hyperperiod = find_hyperperiod(tasks)
    print("Hyperperiod:", hyperperiod)
    
    schedule = non_preemptive_schedule(tasks, hyperperiod)
    print("non-preemptive:", schedule)
    
    plot_gantt(schedule, tasks)
else:
    print("Non-scheluable.")
