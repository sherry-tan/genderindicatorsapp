
import numpy as np
import pandas as pd
import math


#define function to create subsets of data of interest from data1 
def subset_data(data, subset_group, start, end):

    # subset data to include only subset group
    df = data[data['Country Name'].isin(subset_group)]

    #subset data to include only specified time frame
    years_to_keep = [str(year) for year in list(range(start,end+1))]
    cols_to_keep = ['Country Name','Indicator Name'] + years_to_keep
    df = df[cols_to_keep]


    # select indicators of interest, based on indicators explored in SG plots and indicators of interest
    selected_indicators = ['GNI per capita, Atlas method (current US$)',
    'Expected years of schooling, female',
    'Expected years of schooling, male',
    'Tertiary education, academic staff (% female)',
    'Educational attainment, at least completed short-cycle tertiary, population 25+, female (%) (cumulative)',
    'Educational attainment, at least completed short-cycle tertiary, population 25+, male (%) (cumulative)',
    'Literacy rate, adult female (% of females ages 15 and above)',
    'Literacy rate, adult male (% of males ages 15 and above)',
    'School enrollment, tertiary (gross), gender parity index (GPI)',
    'Proportion of women subjected to physical and/or sexual violence in the last 12 months (% of women age 15-49)',
    'Female professional and technical workers (% of total)',
    'Proportion of seats held by women in national parliaments (%)',
    'Proportion of women in ministerial level positions (%)',
    'Women participating in the three decisions (own health care, major household purchases, and visiting family) (% of women age 15-49)',
    'Female headed households (% of households with a female head)',
    'Women who were first married by age 18 (% of women ages 20-24)',
    'Adolescent fertility rate (births per 1,000 women ages 15-19)',
    'Fertility rate, total (births per woman)',
    'Maternal leave benefits (% of wages paid)',
    'Maternity leave (days paid)',
    'Firms with female participation in ownership (% of firms)',
    'Firms with female top manager (% of firms)',
    'Female share of employment in senior and middle management (%)',
    'Ratio of female to male labor force participation rate (%) (modeled ILO estimate)',
    'Unemployment, female (% of female labor force) (modeled ILO estimate)',
    'Unemployment, male (% of male labor force) (modeled ILO estimate)']

    #subset data based on selected indicators
    df = df[df['Indicator Name'].isin(selected_indicators)] 

    #get column names corresponding to years 
    years = [str(x) for x in range(start,end+1)]

    # reshape df into df1: get indicators as column headers and years as observations. Exclude redundant columns such as country code and indicator code
    df1 = pd.melt(df, id_vars=['Country Name','Indicator Name'], value_vars = years, 
            var_name='Year', value_name='Value')
    df1 = df1.set_index(['Country Name','Year','Indicator Name']).unstack(level=-1)
    df1.reset_index(inplace=True)
    df1.columns = df1.columns.droplevel(0)
    df1.columns = ['Country', 'Year']+(list(df1.columns[2:])) #rename columns

    # create new variables for gender comparison - calculate the parity index
    df1['Ratio of female to male tertiary educational attainment rate (GPI) (%)'] = 100*df1['Educational attainment, at least completed short-cycle tertiary, population 25+, female (%) (cumulative)']/df1['Educational attainment, at least completed short-cycle tertiary, population 25+, male (%) (cumulative)']
    df1['Ratio of female to male expected years of schooling (%)'] = 100*df1['Expected years of schooling, female']/df1['Expected years of schooling, male']
    df1['Literacy rate (ages 15 and above) (GPI)(%)'] = 100*df1['Literacy rate, adult female (% of females ages 15 and above)']/df1['Literacy rate, adult male (% of males ages 15 and above)']
    df1.rename(columns={'Ratio of female to male labor force participation rate (%) (modeled ILO estimate)':
                   'Labor force participation rate (ages 15 and above) (%) (GPI)'})
    df1['Ratio of female to male unemployment (%)'] = 100*df1['Unemployment, female (% of female labor force) (modeled ILO estimate)']/df1['Unemployment, male (% of male labor force) (modeled ILO estimate)']
    df1['School enrollment, tertiary (gross), gender parity index (GPI)(%)'] = 100 * df1['School enrollment, tertiary (gross), gender parity index (GPI)']
    
    #drop redundant columns
    columns_to_drop = ['Expected years of schooling, female', 
                   'Expected years of schooling, male',
                   'Educational attainment, at least completed short-cycle tertiary, population 25+, female (%) (cumulative)',
                   'Educational attainment, at least completed short-cycle tertiary, population 25+, male (%) (cumulative)',
                   'Literacy rate, adult female (% of females ages 15 and above)',
                   'Literacy rate, adult male (% of males ages 15 and above)',
                   'Unemployment, female (% of female labor force) (modeled ILO estimate)',
                   'Unemployment, male (% of male labor force) (modeled ILO estimate)',
                        'School enrollment, tertiary (gross), gender parity index (GPI)']

    df1.drop(columns_to_drop, axis = 1, inplace=True)

    #shorten column names
    df1.columns = ['Country', 'Year',
    'Adolescent fertility rate (per 1,000)',
    'Proportion of households with female head (%)',
    'Professional and technical workers (% female)',
    'Employment in senior and middle management (% female)',
    'Fertility rate',
    'Firms with female participation in ownership (% of firms)',
    'Firms with female top manager (% of firms)',
    'GNI per capita(current US$)',
    'Maternity leave (days paid)',
    'National parliament seats (% female)',
    'Ministerial level positions (% female)',
    'Proportion of women subjected to physical/sexual violence in last 12 months (%)',
    'Labor force participation rate (GPI) (%)',
    'Tertiary education, academic staff (% female)',
    'Proportion of women participating in the three decisions (%)',
    'Women who were first married by age 18 (% of women ages 20-24)',
    'Ratio of female to male tertiary educational attainment rate (GPI) (%)',
    'Ratio of female to male expected years of schooling (%)',
    'Literacy rate (ages 15 and above) (GPI)(%)',
    'Ratio of female to male unemployment (%)',
    'School enrollment, tertiary (gross),(GPI) (%)']
    
    #set year column to numeric and take log of GNI for comparability to other data as GNI values are of magnitudes larger than other indicators
    df1['Year']=pd.to_numeric(df1['Year'])
    df1['log(GNI)'] = df1['GNI per capita(current US$)'].apply(lambda x: math.log(x)) 

    return df1

