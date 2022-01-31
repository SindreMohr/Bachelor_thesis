# Smart meters in London dataset

found here: https://www.kaggle.com/jeanmidev/smart-meters-in-london

London Households that took part in the UK Power Networks led Low Carbon London project between November 2011 and February 2014. The data from the smart meters seems associated only to the electrical consumption.

Most data does seem to be within 2012-2014, with only 2013 being complete, the various households got smartmeters at different times, some more complete than others.

## includes:
- acorn_details.csv

- daily_dataset
  with averages, median and std for each day of smart meter power
  3510433 measurements
- halfhourly dataset
    with measurements from smartmeters each half hour in total: 167817021 measurements
 
- information households.csv
    with info about households, based on ACORN classification: https://acorn.caci.co.uk/downloads/Acorn-User-guide.pdf

    5566 households

- uk_bank_holidays
   shows which days are holidays

weather info, both daily, and hourly from darksky api

more info to be found in the various python notebooks.