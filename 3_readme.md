# UK Unemployment Rate data exploration
run pip install -i 3_requirement.txt first and then run python 1_data.py, we can get prepared data and pictures.


# UK Unemployment Rate Database System

## Overview
This project is a Python-based database system designed to manage and analyze unemployment rate data in the UK. The system supports importing and querying unemployment rate data categorized by gender and region.

## Data Structure
The system includes the following main tables:
- TimePeriod: Time period information
- Gender: Gender categories
- Region: Regional categories
- UnemploymentRateByGender: Unemployment rates by gender
- UnemploymentRateByRegion: Unemployment rates by region

## Features
- Automatic SQLite database creation
- CSV data import functionality
- Gender-based unemployment rate analysis
- Region-based unemployment rate analysis
- Data integrity checks and error handling

## Usage
1. Ensure Python and required packages are installed:
pip install pandas sqlite3

2. Prepare data files:
- q1_gender.csv: Contains gender-based unemployment data
- q2_region.csv: Contains region-based unemployment data

3. Run the program:
python 2_create_database.py

## Database Schema
### Table Structures
1. TimePeriod Table
   - PeriodID (Primary Key)
   - PeriodName

2. Gender Table
   - GenderID (Primary Key)
   - GenderName

3. Region Table
   - RegionID (Primary Key)
   - RegionName

4. UnemploymentRateByGender Table
   - ID (Primary Key)
   - PeriodID (Foreign Key)
   - GenderID (Foreign Key)
   - Rate

5. UnemploymentRateByRegion Table
   - ID (Primary Key)
   - PeriodID (Foreign Key)
   - RegionID (Foreign Key)
   - Rate