import os
from sys import argv

# script, source_file_input, save_file_input = argv


def profileGen(source_file):
    #Import
    import openpyxl
    from datetime import datetime
    from pandas import ExcelWriter
    import pandas as pd
    import numpy as np
    from pandas import ExcelWriter
    pd.set_option('max_columns', 50)

    #Define functions
    def data_type_test(in_data):
        if type(in_data) == str:
            in_data = pd.to_datetime(in_data)
        return type(in_data)

    from_csv = pd.read_csv(source_file)

    #Create table and populate with the data types
    data_profile = pd.DataFrame(from_csv.dtypes, columns=['data_type'])

    #Add profiling columns
    for i in data_profile.index.values:
        #Add Row count and number of unique values
        data_profile.loc[i,'Row Count'] = len(from_csv[i])
        data_profile.loc[i,'Unique Values'] = len(from_csv[i].value_counts())
        #Add first, second and third most common values
        data_profile.loc[i,'1st Most Common'] = from_csv[i].value_counts().index[0]
        data_profile.loc[i,'1st Most Common Count'] = from_csv[i].value_counts().values[0]
        if len(from_csv[i].value_counts()) > 1:
            data_profile.loc[i,'2nd Most Common'] = from_csv[i].value_counts().index[1]
            data_profile.loc[i,'2nd Most Common Cnt'] = from_csv[i].value_counts().values[1]
        if len(from_csv[i].value_counts()) > 2:
            data_profile.loc[i,'3rd Most Common'] = from_csv[i].value_counts().index[2]
            data_profile.loc[i,'3rd Most Common Count'] = from_csv[i].value_counts().values[2]

    #Create summary stats for each column (
    summary_stats = from_csv.describe()
    summary_stats = pd.DataFrame.transpose(summary_stats)

    #Merge the data types and the stats together
    data_profile = pd.merge(data_profile, summary_stats, left_index=True, right_index=True, how='left')

    #Add additional information for the non numeric columns
    for i in data_profile.index.values:
        if data_profile.loc[i,'data_type'] == "object":
            data_profile.loc[i,'data_type'] = str(data_type_test(from_csv.loc[1,i]).__name__)
            data_profile.loc[i,'count'] = from_csv[i].count()
            if data_profile.loc[i,'data_type'] == 'Timestamp':
                data_profile.loc[i,'max'] = max(pd.to_datetime(from_csv[i]))
                data_profile.loc[i,'min'] = min(pd.to_datetime(from_csv[i]))

    #The data type column needs to be converted to stings before being sent to the excel file
    data_profile.data_type = data_profile.data_type.apply(str)

    return data_profile
    # if save:
    #     writer = ExcelWriter(save_file)
    #     data_profile.to_excel(writer, 'sheet1')
    #     writer.save()
    #     print("Profile saved to " + working_directory + "/" + save_file)

# print("Running ",script)
# csv_profile(source_file_input, save_file_input)