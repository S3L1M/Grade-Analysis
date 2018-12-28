# Imports
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from functions import grade2gpa

# Load dataset form pickle file
df = pd.read_pickle('dataset').set_index('ID')

# Change columns names for more convenience
subs = ['stat1', 'stat2', 'pm', 'icm', 'signals', 'patterns', 'data minning', 'compilers', 'simulation', 'or', 'pl1', 'pl3', 'network security', 'security', 'sa2', 'dc', 'discrete', 'logic', 'ia', 'it', 'ct', 'hr', 'algorithms', 'math2', 'networks1', 'english2', 'management', 'economics', 'data warehouse', 'gp', 'nlp', 'aa', 'communications', 'it selected1', 'it selected4', 'cs selected2', 'is selected4', 'os1', 'graphics1', 'mis', 'dss', 'se1', 'se2', 'ds']
df.columns = ['lvl', 'name'] + subs

# Add student total GPA column
gpa_col = []
for i in range(2429):
    grades = df.iloc[i]['stat1':].dropna().apply(grade2gpa)
    c = grades.count()  # Set grades count to avoid multiple re-calculations
    gpa_col.append(sum(grades)/c if c!=0 else c)

df['gpa'] = gpa_col

# Summary of dataset
des = df.describe() # count, mean, std, min, 25%, 50%, 75%, max
info = df.info()    # count, datatype (used to check unlogical errors)
cov = df.cov()      # covariance matrix is not convenient because of unit is Grade^2
corr = df.corr()    # correlation matix is better due to its range (-1, 1)
sns.heatmap(corr)   # won't be a useful info due to nan values (could calc sub affect on GPA)

# Seprate grades by student level
df1 = df[df['lvl']=='Level1'].dropna(how='all', axis='columns')
df2 = df[df['lvl']=='Level2'].dropna(how='all', axis='columns')
df3 = df[df['lvl']=='Level3'].dropna(how='all', axis='columns')
df4 = df[df['lvl']=='Level4'].dropna(how='all', axis='columns')

### Exploratory analysis ###
sns.boxplot(data=df, x='lvl', y='gpa', order=['Level1','Level2','Level3','Level4'], 
            width=0.65, whis=1.25)  # boxplot to study outliers

for s in subs:  # save each subject grades distribution histogram
    fig, ax = plt.subplots()
    df.hist(column=s, bins=40, ax=ax)
    fig.savefig('hist'+str(subs.index(s))+'.png')

# Subjects registeration density
counts = [df[s].count() for s in subs]  # Number of enrolled students for each subject 
fig, ax = plt.subplots()    # Initialize figure & axis
sns.barplot(x=subs, y=counts, ax=ax)
fig.savefig('reg_density.png')  # Save barplot

# Subjects/student GPA represented in lineplot
sns.lineplot(data=df, x='stat1', y='gpa', hue='lvl')    # Mostly picked by level1
#   v
#   v
#   v
sns.lineplot(data=df, x='gp', y='gpa', hue='lvl')   # Mostly picked by level 3,4

# To beter understand Subjects/student GPA categories in 2017
sns.scatterplot(data=df, x='pl1', y='gpa', hue='lvl')
sns.scatterplot(data=df, x='logic', y='gpa', hue='lvl', legend=False)

# GPA of each level seprately distribution
sns.set(style='darkgrid')   # set style to darker grid style
sns.distplot(df1['gpa'], hist=False, label='Level1 GPA')
sns.distplot(df2['gpa'], hist=False, label='Level2 GPA')
sns.distplot(df3['gpa'], hist=False, label='Level3 GPA')
sns.distplot(df4['gpa'], hist=False, label='Level4 GPA')

# Summary of gpa distributions
sns.pointplot(data=df, x='lvl', y='gpa', order=['Level1','Level2','Level3','Level4'])

# Create new DataFrame cotains all diffrenet sizes of samples mean
samples_means = pd.DataFrame({'samples_10': [df.gpa.sample(10).mean() for i in range(50)],
                              'samples_20': [df.gpa.sample(20).mean() for i in range(50)],
                              'samples_40': [df.gpa.sample(40).mean() for i in range(50)],
                              'samples_80': [df.gpa.sample(80).mean() for i in range(50)]
                              })
                              
# samples mean & variance
print(samples_means.mean())
print(samples_means.var())
sns.pointplot(data={'mean':samples_means.mean(), 'size':[10, 20, 40, 80]}, 
                    x='size', y='mean') # Pointplot of sample size over GPA mean

# Hypothesis Test (Compare cs selected2 students gpa to other subjects)
subs_except_sele2 = subs.copy()     # cs selected2 not removed yet
subs_except_sele2.remove('cs selected2')
mean_gpa = [df.drop(columns=subs_except_sele2).dropna()['gpa'].mean()]
mean_gpa.append(df3.gpa.mean())
sns.barplot(x=['CS Selected 2 mean GPA', 'Level 3 mean GPA'], y=mean_gpa)

# Save dataset after analysis and edits
df.to_pickle('post-analysis-dataset')