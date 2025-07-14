# F1 telemetry downloader

Downloads telemetry data using the [FastF1](https://github.com/theOehrly/Fast-F1) library and saves it to a CSV file.

## Requirements

* Python 3.8 or higher
* fastf1
* pandas

## Installation

1.  Clone the repository:
```bash
git clone https://github.com/yxe/f1-telget.git
cd f1-telget
```
2.  Install the required libraries using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Usage

You can run the script in one of three ways.

### 1. Using a JSON file

Create a `configs.json` file to define multiple races or drivers. This is ideal for batch downloads.

**`configs.json` example:**
```json
[
    {
        "year": 2022,
        "race": "Saudi Arabia",
        "session": "R",
        "driver": "ALO"
    },
    {
        "year": 2022,
        "race": "Italy",
        "session": "R",
        "driver": "ALO"
    }
]
```

Run the script with the `--json` argument:
```bash
python f1-telget.py --json configs.json
```

### 2. Using command-line arguments

Pass the parameters for a single event directly in the command line:
```bash
python f1-telget.py --year 2022 --race "Singapore" --session "R" --driver "ALO"
```

### 3. Using interactive mode

Run the script without arguments to enter interactive mode. The script will prompt you for each required value:
```bash
python f1-telget.py
```
**Example interaction:**
```
No configuration file or arguments provided. Entering interactive mode.
Enter the year (e.g., 2023): 2024
Enter the race name (e.g., 'Bahrain'): Spain
Enter the session (R, Q, FP1, etc.): R
Enter the 3-letter driver code (e.g., 'VER'): SAI
```

## Output

The script will generate a CSV file in the same directory, named according to the format:
`{year}-{race_name}-{session}-{driver}-telemetry.csv`

**Example:** `2024-miami-q-nor-telemetry.csv`

It will also create a fastf1-cache directory for the data returned from the fastf1 API. Feel free to remove this directory when it is no longer needed.