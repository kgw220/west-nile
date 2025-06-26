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
missing values, feature engineering, and feature selection. I also merged the mosquito trap data
and the weather data collected from the first task.

### Third Task (`model_selection.py`)
The third task was to take the model-ready data from the previous task, and find the best fitting model. 
I chose to stick with a LightGBMClassifier model, given it has many benefits.
I did this with an MLFlow pipeline help keep track of metrics/feature importances, optimizing 
hyperparameters with the help of `hyperopt`'s TPE algorithm. I then refit a champion model by using 
the best set of hyperparameters by combining the validation and training data, and testing with the 
testing data. A final measure of model performance utilized ROC/AUC, since the positive class was rare.

Given the results, I made a business recommendation on a potential cost saving measure, given the model 
was not good at predicting WNV positive tests, explained more in detail below.

### Fourth Task (still WIP, planned to perform CausalML)
N/A

### Results 
#### Third Task:
The champion LGBMClassifier model ended up with a cross-validated ROC/AUC score of 0.83, which is fairly
good, given 0.5 is equivalent to random guessing. The test ROC/AUC score was slightly lower at 0.75.
However, given the data was imbalanced, the overall zero recall was much higher than the non-zero recall, 
and we really want to focus on correctly predicting when WNV *is* present, not when it is not.

As such, because even a small false positive rate results in a very large number in false positives (there
are thousands of mosquito specimans tested each year, and from the data, about 95% do not have WNV), it
is not ideal to focus on creating the best predictive model for when WNV is positive. Spraying can be 
expensive and of course, harmful to the environment when it is sprayed when not needed. Instead, this can
be used by the City of Chicago and CPHD to help determine which species need to be sent for testing, and 
which don't. If a specific species always has a very low, near-zero probability of testing positive, the 
city should just not send it in for testing to save money. With an estimate of $100 per lab test, this 
quickly adds up to significant cost savings with all the testing that is completed (as indicated with
the mosquito trap data!). The table below helps to highlight such savings at various predictive thresholds,
based on the champion model with all the data:

| **TPR/Recall Level (% of actual WNV-positive cases predicted correctly)** | **Prediction Threshold (probability needed to be predicted WNV-positive)** | **Estimated # of Traps to Avoid Testing (predicted WNV-negative)** | **Estimated Annual Savings (based on $100 per test)** |
|---------------------------------------------------------------------|------------------------------------------------------------------|--------------------------------------------------------------------------------|--------------------------------------------------------|
| 80%                                                                 | 0.13444                                                            | 2,284                                                                         | $228,475                                             |
| 85%                                                                 | 0.12948                                                            | 2,274                                                                          | $227,450                                               |
| 90%                                                                 | 0.11911                                                            | 2,259                                                                         | $225,950                                               |
| 95%                                                                 | 0.11062                                                            | 2,244                                                                          | $224,450                                               |
| 100%                                                                | 0.10147                                                            | 2,227                                                                           | $222,700                                               |

Given the data, there is not any "obvious" TPR to suggest, but I would suggest a TPR of 85% for the City of Chicago and the Chicago Department of Public Health, since this is 
the point before savings begins to dip at a faster rate compared to the other options. This means, that if 
a mosquito specimen has an estimated probability greater than 15% of being WNV-positive, it should be sent
for testing. This would lead to considerable cost savings, and help limit the number of WNV-positive mosquitoes
that are missed.

### NOTE/Future Work
The results of the analysis in this project depend on several assumptions, namely that WNV prevalance does not 
change significantly both temporally and spatially. Calculations will have to be adjusted if this is true, meaning more
specimans would have to be tested, and thus, decrease savings. In particular, the data used here is only
for specific years, so it is quite possible different trends do exist, but are not shown here. The data
does show that there are areas where WNV becomes more common, which is important to keep in mind. 

The biggest thing is to fix the data issue so I can gather fully up to date data, which I annotated with 
TODOs in the first task. There were several issues, which led me to not being able to gather as much data
as I would've liked. But the code acts as a framework for such future work, and it may be relevant if patterns are still
consistent. Perhaps the City of Chicago can implement periodic testing where WNV was not previously seen to 
encase these possible patterns.

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

