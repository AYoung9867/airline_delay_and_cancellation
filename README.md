# Analysis of Airline Performance Data

This is an insight into the trends prevailant in delay and cancellation data of different airlines through airports in North America.

## Overview
This analysis compares the patterns in delay and cancellation outcomes across multiple airlines. Anyone who has travelled by air will find interest in this as well as people invested in the operations of airlines. Travellers may be informed on which airlines to avoid if they don't want a longer delay over a straight cancellation, or even the time they should expect to be parked at the gate after landing.

## Questions Explored
1. **Some airlines suffer more delays than others**
   - Compare delays by airline

2. **Some airlines are weighted towards cancellations over delays**
   - Use z-score to compare whether an airline is more weighted towards delays or cancellations

3. **Some airports suffer more delays**
   - Compare delay by airport

4. **Larger airports have longer taxi times**
   - Define large airports by volume of flights and compare taxi time to airport size


## Data Source

- Main dataset:
  ['Airline Delay and Cancellation Data, 2009-2018', https://www.kaggle.com/datasets/yuanyuwendymu/airline-delay-and-cancellation-data-2009-2018?resource=download&select=2018.csv]
  I chose to use the 2018 data from this set as it is the most recent.

- Supplementary Data:
  ['iata_airlines',  https://github.com/benct/iata-utils/blob/master/generated/iata_airlines.csv]
  ['airport-codes', https://datahub.io/core/airport-codes]


## Methodology

- I calculated a 2.9% sample of the whole data set would give the most information while keeping around 25Mb for comfortable upload to a live interactive notebook. 

  `df_trimmed = df.sample(frac=0.029, random_state=42)`

- The data set did not include full airline and airport names so I also sourced the 2 data sets under Supplementary Data to match IATA airlines and airport codes with their full names.

- For the airlines I identified each unique IATA code in the sample data and matched that to its full airlines name with a SQL join to the github data.

- For the airports I split my method into origin and destination so I had two sets of airport names to match up. Again I identified unique airports and found that 1 airport was not in the datahub data so I used google to fill in the gap and add 'Sloulin Field International Airport' to the data. Once I had the relevant airports I used a SQL join to match airport IATA codes on each data set.

- The ARR_DELAY column is null for cancelled and diverted flights which total 3,897 rows, these are naturally excluded from any delay based calculations

## Findings

### Question 1: [Some airlines suffer more delays than others]
![Delay distribution by airline](content/q1_delay_boxplot.png)

We can see an increasing mean as average delays become more severe but the median holds fairly consistent with each airline with a range of only 6 minutes. This means the typical flight on each airline is consistently a few minutes early but the likelihood of a significant delay increases as we move up the graph.

For example, on Frontier Airlines you are at a higher risk of a severe delay than Alaska, this variation is driven by severe outlier delays. Additionally, given the large sample size per airline, a formal significance test would likely confirm differences in mean delay are statistically significant, however this wouldn't be any more informative than the findings derived from the graph.

### Question 2: [Some airlines are weighted towards cancellations over delays]
![Difference Between Average Delay and Proportion of Cancellations by Airline](content/q2_delay_cancellation_barh.png)

This graph shows whether a given airline has more severe average delays or a higher percentage of cancelled flights. These factors are compared by calculating a z-score (z=(x-μ)/σ) for both the average delay and cancellation percentage of each airline, then the difference between the two scores indicated whether an airline leans more toward delays or cancellations. 

We find a clear distinction between some airlines that have a higher proportion of cancelled flights and ones that have more severely delayed flights. Frontier and Allegiant are the most delay dominant with a difference in delay and cancellation z-score of 2 meaning their delay performance sits 2 standard deviations further from the airline average than their cancellation performance does. Virgin America is the most cancellation dominant with a difference of nearly 3. 

### Question 3: [Some airports suffer more delays]
![Funnel Plot to Determine which Airports Contain Enough Data to be Statistically Significant](q3_funnel.png)
![Average NAS Delay by Airport](content/q3_NAS_delay_barh.png)

Here we see the 10 airports with the highest average NAS delay and the 10 airports with the lowest average NAS delay. NAS delays are delays attributed to heavy traffic and air traffic control as well as airport operations like runway closures, construction work and de-icing procedures. Other delay options like weather, carrier and late aircraft were not considered as they don't represent airport specific delays. Although security delay is airport specific, only 0.07% of the data actually included a non-zero figure compared with the 10.35% of NAS delay data.

Only origin airport data was included here as the destination data may have been affected by origin or in flight delays. Airports with less than 130 flights were excluded from this hypothesis, this number was visually determined using a funnel plot where the percentage of flights with NAS delay stabilised as flight volume increased. 

The graph shows a distinct split between the airports with average NAS delay of less than 8 minutes and the airports where average NAS delay sits between 32 and 42 minutes which is substantial enough to say some airports do suffer more NAS delays than others.

### Question 4: [Larger airports have longer taxi times]
![Number of Flight vs Average Taxi Time per Airport](content/q4_taxi_scatter.png)

What we see here are a large number of smaller airports represented by the grey points and a robust but small sample of 74 large airports represented by the green points. Visually it seems there is no correlation in the smaller airports but evidence of positive correlation in the larger.

Calculating the overall correlation between flight volume and average taxi time comes out weakly positive at r=0.258, this appears to be driven almost entirely by a small number of high volume hub airports; airports with fewer than 500 flights show virtually no relationship r=0.046. This suggests taxi time only meaningfully increases at the most congested hubs, rather than scaling steadily with airport size across the board.


## Tools & Technologies
 - Languages: Python
 - Data Manipulation: pandas
 - Database/querying: SQLite, SQL
 - Visualisation: matplotlib
 - Environment: JupyterLite (Pyodide)
 - Version Control/Hosting: Git, GitHub, GitHub Pages, GitHub Actions
