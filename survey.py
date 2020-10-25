import pandas as pd
import numpy as np
import matplotlib as plt
import math

df = pd.read_csv("survey_results_public.csv")

######### Head values #########
# print(df.head())

######### First three rows of each column #########
# for col in data.columns:
#     print(col)
#     print(data[col][:3])
#     print("___")

######### Utility #########
# Prints unique values
# df.unique()
def merge_df(df1, df2, on_col):
    return pd.merge(df1, df2, on=on_col)

def concat_df(df1, df2):
    return pd.concat([df1, df2], axis=1)

# Returns a dataframe with each country mappend to the continent
def continentMapping(df):
    # Country - Continent mapping :
    df_continent = pd.read_csv('Countries-Continents.csv')
    # print(df_continent.head())
    
    df_country = df['Country']
    df_country = concat_df(df_country, df['Respondent'])

    # Due to ,
    df_country = df_country.replace(['Venezuela, Bolivarian Republic of...', 'Congo, Republic of the...'], ['Venezuela Bolivarian Republic of...','Congo Republic of the...'])
    # for nan values :

    # before = set(pd.unique(df_country))
    df_continent = merge_df(df_continent, df_country, 'Country')
    # after = set(pd.unique(df_country['Country']))
    df_continent = df_continent.drop(['Country'], axis=1)

    return df_continent

######### Question1 : Average age of developers when they wrote their first line of code. #########
def ageFirstCode(df):
    df = df['Age1stCode']
    #Discrepancy 1
    df = df.replace(['Older than 85', 'Younger than 5 years'], [85, 5])
    #Discrepancy 2
    df = df.dropna().astype('int32')
    df = df.to_frame()
    #Discrepancy 3
    mean = df.mean(skipna=True)
    print(mean)

######### Question2 : Percentage of developers who know python in each country. #########
def isPython(df_person):
    # Point : str was not passed
    lang = str(df_person).split(';')
    for l in lang:
        # Better approach : regex in the if comparison
        if 'python' == l.replace(' ','').lower():
            return 1
    return 0

def knowPython(df):
    df_lang = df['LanguageWorkedWith']
    df_country = df['Country']
    df_country = concat_df(df_country, df['Respondent'])

    # 'yes' = person knows python / 'no' = person doesn't know python
    df_lang = df_lang.apply(isPython)
    df_lang = concat_df(df_lang, df['Respondent'])

    # Final merged dataframe for analysis
    df_merged_cols = merge_df(df_lang, df_country,'Respondent')

    # Add Count column to get count of people knowing python (Each row value is 1)
    df_merged_cols = df_merged_cols.assign(Count = lambda x:1)
    df_merged_cols = df_merged_cols.drop(['Respondent'], axis=1)

    # print(df_merged_cols.head())
    print(df_merged_cols.groupby(['Country','LanguageWorkedWith']).agg(np.sum))

######### Question3 : Average Salary of developer based on continent #########
def avgContinentSalary(df):
    df_continent = continentMapping(df)

    # Salary :
    # ConvertedComp and CompTotal*currency*CompFreq
    # Dropping Nan values 
    df_salary = concat_df(df['ConvertedComp'], df['Respondent'])
    df_salary = df_salary.dropna()

    df_merged_cols = merge_df(df_continent, df_salary, 'Respondent')
    df_merged_cols = df_merged_cols.drop(['Respondent'], axis=1)
    print(df_merged_cols.groupby('Continent').agg(np.mean))

######### Question4 : Most desired programming language for year 2020. #########

languages_next_year = {
    'Assembly':0,
    'Bash/Shell/PowerShell':0,
    'C':0,
    'C++':0,
    'C#':0,
    'Clojure':0,
    'Dart':0,
    'Elixir':0,
    'Erlang':0,
    'F#':0,
    'Go':0,
    'HTML/CSS':0,
    'Java':0,
    'JavaScript':0,
    'Kotlin':0,
    'Objective­':0,
    'PHP':0,
    'Python':0,
    'R':0,
    'Ruby':0,
    'Rust':0,
    'Scala':0,
    'SQL':0,
    'Swift':0,
    'TypeScript':0,
    'VBA':0,
    'WebAssembly':0,
    'Other(s):':0
}
languages_this_year = {
    'Assembly':0,
    'Bash/Shell/PowerShell':0,
    'C':0,
    'C++':0,
    'C#':0,
    'Clojure':0,
    'Dart':0,
    'Elixir':0,
    'Erlang':0,
    'F#':0,
    'Go':0,
    'HTML/CSS':0,
    'Java':0,
    'JavaScript':0,
    'Kotlin':0,
    'Objective­':0,
    'PHP':0,
    'Python':0,
    'R':0,
    'Ruby':0,
    'Rust':0,
    'Scala':0,
    'SQL':0,
    'Swift':0,
    'TypeScript':0,
    'VBA':0,
    'WebAssembly':0,
    'Other(s):':0
}

def lang_next_year(df_lang):
    if type(df_lang)==str:
        language = df_lang.split(';')

        for l in language:
            l = l.replace(' ','')
            if languages_next_year.get(l):
                languages_next_year[l] += 1
            else:
                languages_next_year.update({l:1})

def lang_this_year(df_lang):
    if type(df_lang)==str:
        language = df_lang.split(';')

        for l in language:
            l = l.replace(' ','')
            if languages_this_year.get(l):
                languages_this_year[l] += 1
            else:
                languages_this_year.update({l:1})

def findMaxDifference_Index(A, B):
    arr_len = len(A)
    maxn = 0

    for i in range(arr_len):
        d = A[i]-B[i]
        if d>maxn:
            indexes = [i]
            maxn = d
        elif d==maxn:
            indexes.append(i)

    return indexes

def nextYear(df):
    df_currenty = df['LanguageWorkedWith']
    df_nexty = df['LanguageDesireNextYear']
    
    # df_temp = concat_df(df['Employment'], df['Hobbyist'])
    # df_temp = df_temp.assign(Count = lambda x:1)
    # print(df_temp.groupby(['Employment','Hobbyist']).count())
    df_currenty.apply(lang_this_year)
    df_nexty.apply(lang_next_year)
    print("       Before | After")
    for key in languages_next_year.keys():
        print("%s : %d | %d" % (key, languages_this_year[key], languages_next_year[key]))
    next_year = list(languages_next_year.values())
    this_year = list(languages_this_year.values())
    indexes = findMaxDifference_Index(next_year, this_year)

    for i in indexes:
        k = list(languages_next_year)[i]
        v = languages_next_year[k] - languages_this_year[k]
        print("Most desired language/s : %s. %d people chose this as the language they will use next year."%(k, v) )

######### Question5 : People who code as hobby based on gender and continent #########
def genderMapping(row):
    if row=='Man':
        return 'Man'
    elif row=='Woman':
        return 'Woman'
    else:
        return 'Others'
    
def codeAsHobby(df):
    df_continent = continentMapping(df)

    df_gender = df['Gender'].apply(genderMapping)
    df_gender = concat_df(df['Respondent'], df_gender)
    
    # # Encoded hobbyist column. 1 = Yes 0 = No
    # df_hobbyist = df['Hobbyist'].apply(lambda x: 1 if x=='Yes' else 0)
    df_hobbyist = df['Hobbyist']

    df_merged_cols = merge_df(df_continent, df_gender, on_col='Respondent')

    df_merged_cols = concat_df(df_merged_cols, df_hobbyist)

    df_counts = df['Respondent'].apply(lambda x: 1).to_frame()
    df_counts = df_counts.rename({df_counts.columns[0]:'Counts'}, axis=1)
    df_merged_cols = concat_df(df_merged_cols, df_counts)
    
    df_merged_cols = df_merged_cols.drop('Respondent', axis=1)
    df_merged_cols = df_merged_cols.groupby(['Continent', 'Gender', 'Hobbyist']).agg(np.sum)
    
    print(df_merged_cols)

######### Question6 : People who are satisfied with their job/career based on gender and continent #########
def satisfied(df):
    df_continent = continentMapping(df)

    df_gender = df['Gender'].apply(genderMapping)
    df_gender = concat_df(df['Respondent'], df_gender)

    df_job = df['JobSat']

    df_merged_cols = merge_df(df_continent, df_gender, on_col='Respondent')
    df_merged_cols.drop('Respondent', axis=1)

    df_merged_cols = concat_df(df_merged_cols, df_job)
    df_counts = df['Respondent'].apply(lambda x: 1).to_frame()
    df_counts = df_counts.rename({df_counts.columns[0]:'Counts'}, axis=1)

    df_merged_cols = concat_df(df_merged_cols, df_counts)

    df_merged_cols = df_merged_cols.groupby(['Continent', 'Gender','JobSat']).agg(np.sum)

    # Drop Respondent column
    df_merged_cols = df_merged_cols.drop('Respondent', axis=1)

    print(df_merged_cols)

######### Choose questions to run #########

print('Question 1: Average age of developers when they wrote their first line of code.')
print('Question 2: Percentage of developers who know python in each country.')
print('Question 3: Average Salary of developer based on continent.')
print('Question 4: Most desired programming language for year 2020.')
print('Question 5: People who code as hobby based on gender and continent.')
print('Question 6: People who are satisfied with their job/career based on gender and continent.')

while(True):
    entered = int(input('Enter Question number : (1/2/3/4/5/6)'))
    print('Answer :')
    print(' ')
    if entered == 1:
        ageFirstCode(df)
    elif entered == 2:
        knowPython(df)
    elif entered == 3:
        avgContinentSalary(df)
    elif entered == 4:
        nextYear(df)
    elif entered == 5:
        codeAsHobby(df)
    elif entered == 6:
        satisfied(df)
    else:
        break
    print(' ')
    print('Enter 0 to stop')