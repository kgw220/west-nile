# Mosquito Watch

### Background
This project aims to analyze and model the distribution of the potentially deadly West Nile Virus 
around the Chicago area, as the local mosquito population can carry this virus.

West Nile Virus (WNV) is an infectious disease that was discovered in 1937 in the West Nile region 
of Uganda. It started spreading to the United States in 1999, via infected mosquitos. Most people
who are infected do not have symptoms (at least initially), but some do; Said symptoms include
fever, headaches, body aches, and skin rashes. In rare circumstances, WNV can be life-threatening 
if it enters the brain, causing Encephalitis (inflammation to the brain). Unfortunately there are no
vaccines or treatments available, so the best way way to prevent getting WNV is to avoid mosquito 
bites altogether.

Traps were placed around Chicago to help track the amount of mosquitoes in different areas.
They are then grouped into pools, and tested in a lab to determine if any in the group carry WNV. 
Each row represents one test of a mosquito pool from a specific trap on a specific date, with 
results indicating whether WNV was detected. This surveillance data helps public health officials 
monitor mosquito-borne virus activity, assess risk to humans, and guide mosquito control efforts.

The City of Chicago and the Chicago Public Health Department (CPHD) have resorted to spraying areas 
when WNV is detected to kill the infected mosquites and prevent the virus' spread. 

### Goal
The main goal is to build an accurate predictive model to help predict when there are 
spikes in WNV based on the historical data gathered thus far, which can help city officials more 
efficiently and effectively allocate resources towards preventing transmission of this potentially 
deadly virus. Not only that, but further insights and (theoretical) propositions are given
based on the trends that were highlighted throughout the process.

### Methodology
This project is split up into different python files/notebooks to help split up each major task, 
each of which are in the tasks directory.

#### First Task (`data_retrieval.py`)
The first task is to gather the data. Mosquito trap data was pulled with City of Chicago's API. 
Weather data was from NOAA.

#### Second Task (`EDA_preprocessing.py`)
The second task is to preprocess the data for modeling. This involved correcting datatypes, filling 
missing values, feature engineering, and feature selection.

### Future Work
The biggest thing is to fix the data issue so I can gather fully up to date data, which I annotated with 
TODOs in the first task. There were several issues, which led me to not being able to gather as much data
as I would've liked.

A very minor thing (that I don't think matters in the long run) is to display the correlation matrix of
all possible features in my EDA notebook. I displayed individual correlation matrices for the weather and 
mosquito trap data, but this of course does not display any correlation with features across both. However,
since I performed feature selection with mRMR at the very end, this is probably being nitpicky and unnecessary.

## Data Sources

### Mosquito Trap Data 

| Column Name          | Data Type | Description                              | Notes                       |
| --------------------- | --------- | ---------------------------------------- | --------------------------- |
| Date                  | DateTime  | Date the row's data come from            |                             |
| Address               | String    | Approximate address of the location of trap. Used for GeoCoder |  |
| Species               | String    | Species of mosquito for that row of data |                             |
| Block                 | Integer   | Block Number of trap address             |                             |
| Street                | String    | Street name of trap address              |                             |
| Trap                  | String    | Trap ID                                   |                             |
| AddressNumberAndStreet| String    | Address and street of the trap           |                             |
| Latitude              | Float     | Trap latitude                             |                             |
| Longitude             | Float     | Trap longitude                            |                             |
| AddressAccuracy       | Integer   | Accuracy of trap address returned from GeoCoder |             |
| NumMosquitos          | Integer   | Number of mosquitoes of a particular species found in a trap |  |
| WnvPresent            | Boolean   | Whether or not West Nile Virus was found in the sample |  |

Source: [City of Chicago](https://data.cityofchicago.org/Health-Human-Services/West-Nile-Virus-WNV-Mosquito-Test-Results/jqe8-8r6s/about_data)

---

### Weather Data from Nearby Weather Stations Chicago O'Hare and Midway

| Column Name  | Data Type | Description                             | Notes                              |
| ------------- | --------- | --------------------------------------- | ---------------------------------- |
| Station       | Integer   | Which station the data in the row come from | Station 1 = Chicago O-Hare, Station 2 = Midway |
| Date          | DateTime  | Date the row’s data come from           |                                    |
| Tmin          | Integer   | Minimum temperature that date           |                                    |
| Tmax          | Integer   | Maximum temperature that date           |                                    |
| Tavg          | Integer   | Average temperature across the day      |                                    |
| Depart        | Integer   | Difference from normal for that day     | Only available for Station 1       |
| DewPoint      | Integer   | Average Dew Point Temperature           | Temperature where water vapor starts to condense out of the air |
| WetBulb       | Integer   | Average Wet Bulb Temperature            | Adiabatic saturation temperature ([more info here](https://en.wikipedia.org/wiki/Wet-bulb_temperature)) |
| Heat          | Integer   | 65 - Tavg (65-Tavg)                     |                                    |
| Cool          | Integer   | Tavg - 65 (Tavg-65)                     |                                    |
| Sunrise       | Time      | Sunrise time in military time           | Only available for Station 1       |
| Sunset        | Time      | Sunset time in military time            | Only available for Station 1       |
| CodeSum       | List      | Code(s) for various weather conditions  | e.g. F=Fog, H=Haze                 |
| Depth         | Integer   | Precipitation Depth, if applicable (collected in 6hr) |                  |
| Snowfall      | Float     | Snowfall (inches)                       |                                    |
| PrecipTotal   | Float     | Rain (inches)                           |                                    |
| StnPressure   | Float     | Average station pressure                |                                    |
| SeaLevel      | Float     | Sea level pressure (inches of Hg)       |                                    |
| ResultSpeed   | Float     | Resultant wind speed (mph)              | Resultant wind = vector sum of wind speeds and directions |
| ResultDir     | Integer   | Resultant wind direction (degrees)      | Resultant wind = vector sum of wind speeds and directions. Scale of 10 per integer. |
| AvgSpeed      | Integer   | Average wind speed                      |                                    |

Source: [NOAA](https://www.ncdc.noaa.gov/cdo-web/datatools/findstation)

