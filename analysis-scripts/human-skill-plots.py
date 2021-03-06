# Participants selected their ratings against a number of "Human Skills".
# This script plots the 1-5 confidence of participants who report those skills,
#   bucketed per "years experience in field" categories.
# Currently, using box catplot from Seaborn python library

# Needs all the data from this google sheet, exported to CSVs:
# https://docs.google.com/spreadsheets/d/1IgbQiHOBhKZNEaTAXMJY16ZDwbE8NQmgZbX07fmMY6I/edit?usp=sharing

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

rsf = pd.read_csv('input-data/RSF_data.csv')
skills = pd.read_csv('input-data/human-skill-codes.csv')
bands = pd.read_csv('input-data/year-bands.csv')
outputfolder = "graphics/human-skill-plots/"

# SKILL LOOP
# Iterate through all skills
for index, skill in skills.iterrows():

    rows_list = []

    # EXPERIENCE BAND LOOP
    # Get observations for this skill, by band level as rows, dump into dataframe (skillframe)
    for index, band in bands.iterrows():
        slice = rsf.loc[(rsf['years_in_field'] >= band['min']) & (rsf['years_in_field'] <= band['max'])]

        #observations
        # There's gotta be a better way... I don't know how to melt
        for index, obs in slice.iterrows():
            rows_list.append([band['name'],obs['years_in_field'],obs[skill['code']],obs['job_category_select']])

    skillframe = pd.DataFrame(rows_list,columns=['experience', 'years', 'rating', 'role'])
    print skillframe
    # Plot skillframe and save as graphical output
    sns.set(style="whitegrid", palette="muted")
    g = sns.lineplot(x="years", y="rating",
                    #hue="role",
                    data=skillframe)
    #g.set_ylabels("confidence rating")
    #g.set_xlabels("Years experience")
    plt.ylim(0,5)
    plt.xlim(0,5)
    plt.title(skill['skill'].capitalize())
    print("generating Skill: " + skill['skill'].capitalize() + " image")
    #plt.show()

    #Title with skillname-cleaned up
    plt.savefig(outputfolder + skill['skill'].replace(" ", "_").replace("/","-").replace("&","-and-")+".png")
    plt.close()
