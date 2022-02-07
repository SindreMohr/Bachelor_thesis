# Smart meters in London dataset

found here: https://www.kaggle.com/jeanmidev/smart-meters-in-london

# info from provider:

There is 19 files in this dataset :

    informations_households.csv : this file that contains all the information on the households in the panel (their acorn group, their tariff) and in which block.csv.gz file their data are stored

    halfhourly_dataset.zip: Zip file that contains the block files with the half-hourly smart meter measurement

    daily_dataset.zip: Zip file that contains the block files with the daily information like the number of measures, minimum, maximum, mean, median, sum and std.

    acorn_details.csv : Details on the acorn groups and their profile of the people in the group, it's come from this xlsx spreadsheet.The first three columns are the attributes studied, the ACORN-X is the index of the attribute. At a national scale, the index is 100 if for one column the value is 150 it means that there are 1.5 times more people with this attribute in the ACORN group than at the national scale. You can find an explanation on the CACI website. https://acorn.caci.co.uk/what-is-acorn

    weatherdailydarksky.csv : that contains the daily data from darksky api. You can find more details about the parameters in the documentation of the api

    weatherhourlydarksky.csv : that contains the hourly data from darksky api. You can find more details about the parameters in the documentation of the api




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

    5566 households:

  * What is Acorn?
    Acorn is a geodemographic segmentation of
    the UK’s population. It segments households,
    postcodes and neighbourhoods into 6
    categories, 18 groups and 62 types. By analysing
    significant social factors and population
    behaviour, it provides precise information and
    an in-depth understanding of the different
    types of people.    

  see excel sheet here for more detail: https://acorn.caci.co.uk/what-is-acorn
 
  * Category 1 Affluent AChievers
    // percentages are from pi diagram of acorn categories in our dataset
  

    Acorn A Lavish lifestyles 2.8%
        B executive wealth < 1%
        C mature Money 2.7%
  * category 2 rising prosperity
    D city sophisticates 5.2%
0 96*- * category 3 comfortable communities
    F Countryside Communities 12.3 %
    G Successful Suburbs 3.7 %
    H steady Neighbourhoods 8.2 %
    I comfortable Seniours 0.9 %
    J Starting Out 2.0 %
  * Category 4 financially stretched
    K Student Life 3.0 %
    L Modest Means 6.1 %
    M striving Families 2.0 %
    N Poorer Pensioners 2.7 %

  * Category 5 Urban Adversity
    O Young Hardship  1.9 %
    P Struggling Estates 2.0 %
    Q Difficult Circumstances 14.9 %

  there are further subgroups than this that specify more in detail the kind of house the resident has, however our dataset merely states which ACORN-X it is.


   * Lavish Lifestyles: (The 1%)
      These neighbourhoods have the greatest
      concentrations of higher rate taxpayers.

      the typical family will live in a large house worth
      over £1million and, particularly in the South East,
      their homes may be worth many millions. A good
      number will own additional property, either abroad
      or in the UK.

   * Executive Wealth:
        These are high income people, successfully
        combining jobs and families

         Many families
        own their home but a good number may still be
        repaying a mortgage. The likelihood of these families
        owning a second home, in the UK or abroad, is over
        five times the UK average.
   * Mature Money:
      These people tend to be older empty nesters
      and retired couples.
      These are high income households and even those
      that have retired have good incomes.

    cat 2 Rising Prosperity:
   * City Sophisticates:
      These affluent younger people generally own flats
      in major towns and cities. These flats are over twice the cost of
      the average UK house and more expensive than the
      average property in these more expensive urban
      locations.

      Single people and couples without children form the
      majority of people in these areas. 

   * Career Climbers: (majority of our households in this group 28%)
   * 
      These are younger people, singles, couples and
      families with young children. They live in flats,
      apartments and smaller houses, which they are
      sometimes renting and often buying with a mortgage,
      occasionally using a shared equity scheme. Usually
      these are in urban locations, frequently in London
      and large towns and cities across the country where
      the flats cost more than the national average price
      of a house.

      Although they are more likely than average to have
      some savings, investments and pensions, others are
      more likely to have loans, perhaps the residue of
      student borrowing and to have mortgage repayments.

      As a result the good jobs may not always reflect high
      disposable income and a few may even be having
      some difficulties with debt. The Career Climbers are
      more likely than many to switch provider of all forms
      of financial services.

    *  Comfortable Communities: 

      this category contains much of middle-of-the-road Britain,
      whether in the suburbs, smaller towns or the countryside.

    * Countryside Communities (third largest in dataset 12%):
      These are areas of the lowest population densities in
      the country, ranging from remote farming areas to
      smaller villages and housing on the outskirts of
      smaller towns.

      // might have greater access to firewood, ie not heating with electricity

    * Successful Suburbs (3.7% ):

    * Steady Neighbourhoods
        These home-owning families, often middle–aged, are
        living comfortably in suburban and urban locations.
        They mainly own older, lower priced, three bedroom
        terraced or semi-detached homes, which they may
        have occupied for many years.
    * comfortable seniors

    * starting out

    * financially stretched
    *  students
    *  modest means
    *  striving families
    *  urban adversity
    *  young hardship
    *  struggling estates
    *  Difficult circumstances (15%)
        Generally these are streets with a higher proportion
          of younger people. Although all age groups may be
          represented those aged under 35 and with young
          children are more prevalent. There are twice as many
          single parents compared to the national average.
          The bulk of the housing is flats rented from the
          council or housing association although there may also
          be some socially rented terraced housing. Generally
          these are small flats and a good proportion of Britain’s
          high rise blocks make up a small part of this group.
          These are relatively deprived neighbourhoods. The
          numbers claiming Jobseeker’s Allowance, Income
          Support, and Employment and Support Allowance
          are all at their highest levels in this group. There may
          be high levels of long term unemployment and of
          households relying entirely on state benefits

          

- uk_bank_holidays
   shows which days are holidays

weather info, both daily, and hourly from darksky api

more info to be found in the various python notebooks.