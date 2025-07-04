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

Also, causal-based ML is performed to help highlight specific factors that may heavily influence 
the presence of WNV.

### Methodology
This project is split up into different python files/notebooks to help split up each major task, 
each of which are in the tasks directory.

#### First Task (`data_retrieval.py`)
The first task is to gather the data. Mosquito trap data was pulled with City of Chicago's API. 
Weather data was from NOAA.

#### Second Task (`EDA_preprocessing.ipynb`)
The second task is to preprocess the data for modeling. This involved correcting datatypes, filling 
missing values, feature engineering, and feature selection. I also merged the mosquito trap data
and the weather data collected from the first task.

#### Third Task (`model_selection.ipynb`)
The third task was to take the model-ready data from the previous task, and find the best fitting model. 
I chose to stick with a LightGBMClassifier model, given it has many benefits.
I did this with an MLFlow pipeline help keep track of metrics/feature importances, optimizing 
hyperparameters with the help of `hyperopt`'s TPE algorithm. I then refit a champion model by using 
the best set of hyperparameters by combining the validation and training data, and testing with the 
testing data. A final measure of model performance utilized ROC/AUC, since the positive class was rare.

Given the results, I made a business recommendation on a potential cost saving measure, given the model 
was not good at predicting WNV positive tests, explained more in detail below.

#### Fourth Task (`causal_modeling.ipynb`)
The fourth and final task was to supplement the findings in the third task. Since model performance was
poor due to the imbalanced data, I performed causal ML to try and highlight causality with what features
would lead to a significant increase in WNV. This was done with subsetted to the features that fulfilled
Causal ML assumptions, then fitting a DML model for each possible treatment and remaining covariates.
From this, I also tracked the average and individual treatment effects, and fitted "honest" trees to 
help uncover treatment interactions with the causality of WNV.

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
a mosquito specimen has an estimated probability greater than 12.9% of being WNV-positive, it should be sent
for testing. This would lead to considerable cost savings, and help limit the number of WNV-positive mosquitoes
that are missed.

#### Fourth Task
It was confirmed that seasonality was a very significant factor with causing WNV. In particular, the ITE/ATE was
much higher in the summer months than the winter months. Alongside that, having higher temperatures
also led to a higher ITE. A table of the individual ATEs with the corresponding interpretation is listed below:

| Feature | ATE |
| :--- | :--- |
| RA | 0.108588 |
| BR | 0.106384 |
| HZ | 0.122440 |
| TS | 0.091447 |
| ResultDir | -0.000591 |
| Sunrise | 0.002542 |
| Cool | 0.086928 |
| Heat | 0.083541 |
| day_of_year | 0.000759 |

* **HZ (Haze):**
    * **Meaning:** Whether the weather on a given day was recorded as hazy by NOAA.
    * **ATE Interpretation:** Its presence is associated with a **12.2 percentage point increase** in the probability of WNV.

* **RA (Rain):**
    * **Meaning:** Whether the weather on a given day was rainy as recorded by NOAA.
    * **ATE Interpretation:** Its presence is associated with a **10.9 percentage point increase** in the probability of WNV, likely by creating mosquito breeding grounds.

* **BR (Mist):**
    * **Meaning:** Whether the weather indicated mist (e.g., humidity in the air) as recorded by NOAA.
    * **ATE Interpretation:** Its presence is associated with a **10.6 percentage point increase** in the probability of WNV.

* **TS (Thunderstorm):**
    * **Meaning:** Whether the weather recorded a thunderstorm on a given day as recorded by NOAA.
    * **ATE Interpretation:** Its presence is associated with a **9.1 percentage point increase** in the probability of WNV.

* **Cool (Cooling Degree-Days):**
    * **Meaning:** A measure of how much hotter the daily temperature was above 65 degrees Fahrenheit, as a measurement for how much energy is needed for cooling.
    * **ATE Interpretation:** Each additional degree the average daily temperature exceeds 65°F is associated with an **8.7 percentage point increase** in the probability of WNV.

* **Heat (Heating Degree-Days):**
    * **Meaning:** A measure of how much cooler the daily temperature was above 65 degrees Fahrenheit, as a measurement for how much energy is needed for heating.
    * **ATE Interpretation:** Each additional degree the average daily temperature is below 65°F is associated with an **8.4 percentage point increase** in the probability of WNV.

* **Sunrise:**
    * **Meaning:** The time of sunrise, in 24H time.
    * **ATE Interpretation:** Each additional minute later that sunrise occurs is associated with a negligible **0.3 percentage point increase** in the probability of WNV.

* **day_of_year:**
    * **Meaning:** The sequential day of the year (1-365).
    * **ATE Interpretation:** Each day later in the year is associated with a negligible **0.08 percentage point increase** in the probability of WNV.

* **ResultDir (Resultant Wind Direction):**
    * **Meaning:** The average wind direction over 24 hours, measured in degrees (1-360) in 10 degree units.
    * **ATE Interpretation:** Each additional 10 degrees in wind direction (clockwise) is associated with a **0.06 percentage point decrease** in the probability of WNV.

Refer to the notebook for more in depth analysis.

Overall, this highlights what is suspected. Spraying should be done on a careful basis based on these factors.
Instead of spraying on a regular schedule, it should be done when these specific, predictive conditions are
met to be more targetted and to help avoid wasting funds on spraying when it is ineffective. It may be helpful
to develop some kind of risk-alert system with NOAA to help provide a level when enough conditions are fulfilled.

### NOTE/Future Work
The results of the analysis in this project depend on several assumptions, namely that WNV prevalance does not 
change significantly both temporally and spatially. Calculations will have to be adjusted if this is true, meaning more
specimans would have to be tested, and thus, decrease savings. In particular, the data used here is only
for specific years, so it is quite possible different trends do exist, but are not shown here. The data
does show that there are areas where WNV becomes more common, which is important to keep in mind. 

These issues cascade down to the causal analysis. Not only that, but only a subset of the features 
were suitable since causal ML has some strict assumptions to ensure the validity of the analysis.
A good chunk were weather based, so most of the insights there are "biased" toward weather. More
data could certainly change this subset, leading to different insights.

So all in all, the biggest thing is to fix the data issue so I can gather fully up to date data, which I annotated with 
TODOs in the first task. There were several issues, which led me to not being able to gather as much data
as I would've liked. But the code acts as a framework for such future work, and it may be relevant if patterns are still
consistent. Perhaps the City of Chicago can implement periodic testing where WNV was not previously seen to 
encase these possible patterns.

## Data Sources

### Mosquito Trap Data 

| Column Name              | Data Type | Description                                                                 |
|--------------------------|-----------|-----------------------------------------------------------------------------|
| Date                     | DateTime  | Timestamp indicating when the trap data was collected                       |
| Address                  | String    | General location where the trap was set; typically used for geocoding      |
| Species                  | String    | Type of mosquito captured in the specific record                            |
| Block                    | Integer   | Numerical identifier for the block location of the trap                     |
| Street                   | String    | Street name corresponding to the trap's placement                           |
| Trap                     | String    | Unique identifier for the mosquito trap                                     |
| AddressNumberAndStreet   | String    | Combined address number and street name for precise location info           |
| Latitude                 | Float     | Geographic latitude of the trap location                                    |
| Longitude                | Float     | Geographic longitude of the trap location                                   |
| AddressAccuracy          | Integer   | Quality score of the address returned by the geocoding process              |
| NumMosquitos             | Integer   | Count of mosquitoes of the given species caught in the trap                 |
| WnvPresent               | Boolean   | Indicates if West Nile Virus was detected in the sample (True or False)     |


Source: [City of Chicago](https://data.cityofchicago.org/Health-Human-Services/West-Nile-Virus-WNV-Mosquito-Test-Results/jqe8-8r6s/about_data)

---

### Weather Data from Nearby Weather Stations Chicago O'Hare and Midway

| Column Name   | Data Type | Description                                                                 | Notes                                                                 |
|----------------|-----------|------------------------------------------------------------------------------|-----------------------------------------------------------------------|
| Station        | Integer   | Identifies which weather station the record is from                         | 1 = O'Hare, 2 = Midway                                                |
| Date           | DateTime  | The date associated with the weather observation                            |                                                                       |
| Tmin           | Integer   | Recorded lowest temperature for the day                                     |                                                                       |
| Tmax           | Integer   | Recorded highest temperature for the day                                    |                                                                       |
| Tavg           | Integer   | Average temperature over the course of the day                              |                                                                       |
| Depart         | Integer   | Temperature deviation from the historical norm                              | Only provided for Station 1                                           |
| DewPoint       | Integer   | Dew point temperature                                                        | Temperature where air becomes saturated (dew forms)                  |
| WetBulb        | Integer   | Wet bulb temperature                                                         | Represents the adiabatic saturation temperature                       |
| Heat           | Integer   | Heating degree days: calculated as 65 minus Tavg                             | Reflects heating needs                                                |
| Cool           | Integer   | Cooling degree days: calculated as Tavg minus 65                             | Reflects cooling needs                                                |
| Sunrise        | Time      | Sunrise time in 24-hour (military) format                                   | Present only for Station 1                                            |
| Sunset         | Time      | Sunset time in 24-hour (military) format                                    | Present only for Station 1                                            |
| CodeSum        | List      | Coded indicators for observed weather conditions                            | Examples: F=Fog, H=Haze                                               |
| Depth          | Integer   | Depth of precipitation (if collected), in tenths of inches                  | Usually refers to 6-hour accumulation                                 |
| Snowfall       | Float     | Snowfall in inches                                                          |                                                                       |More actions
| PrecipTotal    | Float     | Total precipitation (inches)                                                | Includes rain and melted snow                                         |
| StnPressure    | Float     | Atmospheric pressure measured at the station                                |                                                                       |
| SeaLevel       | Float     | Sea-level adjusted pressure (in inches of Hg)                               |                                                                       |
| ResultSpeed    | Float     | Computed wind speed from vector components                                  | Combines directional wind vectors                                     |
| ResultDir      | Integer   | Computed wind direction from vector components (degrees)                    | Scale of 10; derived from wind vector calculations                    |
| AvgSpeed       | Integer   | Mean wind speed over the day                                                |                                                                       |


Source: [NOAA](https://www.ncdc.noaa.gov/cdo-web/datatools/findstation)
