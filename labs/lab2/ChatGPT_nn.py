#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 11:06:28 2024

@author: dgrimes
"""

import numpy as np

# Function to calculate the total tour distance
def calculate_total_distance(tour, distance_matrix):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += distance_matrix[tour[i]][tour[i+1]]
    # Add distance to return to the starting point
    total_distance += distance_matrix[tour[-1]][tour[0]]
    return total_distance

# Nearest Neighbor Heuristic for TSP
def nearest_neighbor_tsp(distance_matrix, start_city=0):
    num_cities = len(distance_matrix)
    unvisited = list(range(num_cities))  # List of unvisited cities
    unvisited.remove(start_city)         # Remove the starting city from the list
    tour = [start_city]                  # Initialize the tour with the starting city

    current_city = start_city
    while unvisited:
        # Find the nearest unvisited city
        nearest_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        tour.append(nearest_city)       # Add nearest city to the tour
        unvisited.remove(nearest_city)  # Remove the city from unvisited list
        current_city = nearest_city     # Move to the next city

    return tour

# Example usage
if __name__ == "__main__":
    # Define the distance matrix (symmetric for simplicity)
    distance_matrix = np.array([[0, 29, 20, 21],
                                [29, 0, 15, 17],
                                [20, 15, 0, 28],
                                [21, 17, 28, 0]])

    start_city = 0  # Starting from city 0
    tour = nearest_neighbor_tsp(distance_matrix, start_city)
    total_distance = calculate_total_distance(tour, distance_matrix)

    print("Tour:", tour)
    print("Total distance:", total_distance)
