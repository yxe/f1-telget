#!/usr/bin/python3
#
# Fetch and save F1 telemetry data.
# 
# Author: hi@ilia.im
# Licence: MIT

import fastf1
import pandas as pd
import os
import argparse
import json

# Fetches and saves telemetry data for a single configuration.
def fetch_and_save_telemetry(config):
    try:
        year = int(config['year'])
        race = config['race']
        session_type = config['session']
        driver_abbr = config['driver']

        # Load session data using the configured variables.
        print(f"Loading data for: {year} {race} GP - Session: {session_type} - Driver: {driver_abbr}")
        session = fastf1.get_session(year, race, session_type)
        session.load(telemetry=True, laps=True, weather=False)
        print("Data loaded successfully.")

        # Select the laps for the desired driver.
        print(f"Fetching laps for driver: {driver_abbr}...")
        driver_laps = session.laps.pick_drivers([driver_abbr])

        if driver_laps.empty:
            print(f"No data found for driver {driver_abbr} in this session.\n")
            return

        # Get the telemetry data for all of the driver's laps.
        print("Extracting telemetry data...")
        driver_telemetry = driver_laps.get_telemetry()
        print("Telemetry data extracted.")

        # Define the output filename based on the specified format.
        race_name_formatted = race.replace(' ', '-').lower()
        output_filename = f"{year}-{race_name_formatted}-{session_type.lower()}-{driver_abbr.lower()}-telemetry.csv"

        # Save the telemetry data to a CSV file.
        driver_telemetry.to_csv(output_filename, index=False)
        print(f"Telemetry data saved to: {output_filename}\n")

    except Exception as e:
        print(f"An error occurred for configuration {config}: {e}")
        print("Please check the configuration details and your internet connection.\n")

# Parses command-line arguments to get configurations.
def get_configurations():
    parser = argparse.ArgumentParser(
        description="Fetch and save F1 telemetry data.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Argument for a JSON file
    parser.add_argument(
        '--json',
        type=str,
        help='Path to a JSON file containing a list of configurations.'
    )

    # Arguments for a single configuration
    parser.add_argument('--year', type=int, help='The year of the session (e.g., 2022).')
    parser.add_argument('--race', type=str, help="The name of the Grand Prix (e.g., 'Saudi Arabia').")
    parser.add_argument('--session', type=str, help="Session type: 'R', 'Q', 'S', 'FP1', etc.")
    parser.add_argument('--driver', type=str, help="Three-letter driver abbreviation (e.g., 'ALO').")

    args = parser.parse_args()

    # Check for JSON file input
    if args.json:
        print(f"Loading configurations from JSON file: {args.json}")
        try:
            with open(args.json, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: JSON file not found at '{args.json}'")
            return []
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from '{args.json}'. Please check its format.")
            return []

    # Check for command-line argument input
    if args.year and args.race and args.session and args.driver:
        print("Using configuration from command-line arguments.")
        return [{
            'year': args.year,
            'race': args.race,
            'session': args.session,
            'driver': args.driver
        }]

    # Fallback to interactive mode
    print("-" * 40)
    print("No configuration file or arguments provided. Entering interactive mode.")
    print("Please provide the details for the data you want to fetch.")
    try:
        config = {
            'year': input("Enter the year (e.g., 2023): "),
            'race': input("Enter the race name (e.g., 'Bahrain'): "),
            'session': input("Enter the session (R, Q, FP1, etc.): ").upper(),
            'driver': input("Enter the 3-letter driver code (e.g., 'VER'): ").upper()
        }
        return [config]
    except KeyboardInterrupt:
        print("\nInteractive input cancelled by user.")
        return []

if __name__ == '__main__':
    # Set up cache directory.
    cache_path = './fastf1-cache'
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    fastf1.Cache.enable_cache(cache_path)
    print(f"FastF1 cache enabled at: {cache_path}")

    # Set pandas to display all columns of the dataframe
    pd.set_option('display.max_columns', None)

    # Get configurations
    configurations = get_configurations()
    
    if not configurations:
        print("\nNo configurations to process. Exiting.")
    else:
        # Loop through each configuration and process it.
        for job_config in configurations:
            print("-" * 50)
            fetch_and_save_telemetry(job_config)
        
        print("-" * 50)
        print("All configurations processed.")