import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels as sms
from tabulate import tabulate 
import re
import patsy
import xlrd
import openpyxl

df1 = pd.read_csv('/Users/kritikarai/Desktop/PrisonData/PrisonData_2015_1.csv')
df1 = df1.drop('ID_Check',axis=1)
df1 = df1.iloc[:144]
df2 = pd.read_csv('/Users/kritikarai/Desktop/PrisonData/PrisonData_2014.csv')
df = pd.concat([df1,df2] ,join = 'outer', ignore_index = True)

new = open('/Users/kritikarai/Desktop/finaldata.csv','w')
df.to_csv(new)
new.close()

columns_drop = ['AM','EC','IF','S0','SC','TM','NewPreQ1','NewQ15','NewQ17','NewQ19','NewQ22','NewQ24','NewQ25','NewQ26','filter_$']
df = df.drop(columns_drop,axis =1)

cols = df1.columns.values

df = df[['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'PreQ1','PreQ2a', 'PreQ2b', 'PreQ2c', 'PreQ2d', 'PreQ2e', 'PreQ3a',
       'PreQ3b', 'PreQ3c', 'PreQ3d', 'PreQ3e', 'PreQ3f', 'PreQ3g','PreQ3h', 'PreQ4', 'PreQ5a', 'PreQ5b', 'PreQ5c', 'PreQ5d', 'PreQ6',
       'PreQ7', 'PreQ8', 'PreQ9a', 'PreQ9b', 'PReQ9c', 'PreQ9d', 'PreQ9e','PreQ10a', 'PreQ10b', 'PreQ10c', 'PreQ10d', 'PreQ10e', 'PreQ10f',
       'PreQ11a', 'PreQ11b', 'PreQ11c', 'PreQ11d', 'PreQ11e', 'PreQ11f','PreQ11g', 'PreQ11h', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28', 'PostQ30','PostQ1', 'PostQ2a', 'PostQ2b', 'PostQ2c', 'PostQ2d',
       'PostQ2e', 'PostQ3a', 'PostQ3b', 'PostQ3c', 'PostQ3d', 'PostQ3e','PostQ3f', 'PostQ3g', 'PostQ3h', 'PostQ4', 'PostQ5a', 'PostQ5b',
       'PostQ5c', 'PostQ5d', 'PostQ6', 'PostQ7', 'PostQ8a', 'PostQ8b','PostQ8c', 'PostQ8d', 'PostQ8e', 'PostQ8f', 'PostQ8g', 'PostQ8h',
       'PostQ8i', 'PostQ8j', 'PostQ9', 'PostQ10a', 'PostQ10b', 'PostQ10c','PostQ10d', 'PostQ10e', 'PostQ11a', 'PostQ11b', 'PostQ11c',
       'PostQ11d', 'PostQ12a', 'PostQ12b', 'PostQ12c', 'PostQ12d','PostQ12e', 'PostQ12f', 'PostQ12g', 'PostQ12h']]
       
columns_to_keep = ['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples', 'PreQ4','PreQ1', 'PostQ1','Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17',
       'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28', 'PostQ30']
attitudinal_scales_df = pd.DataFrame(df,columns = columns_to_keep)

first = re.compile('Strongly Agree',re.IGNORECASE)
second = re.compile('Somewhat Agree',re.IGNORECASE)
third = re.compile('Not Sure',re.IGNORECASE)
fourth = re.compile('Somewhat Disagree',re.IGNORECASE)
fifth = re.compile('Strongly Disagree',re.IGNORECASE)

for column in ['Q12', 'Q13', 'Q14', 'Q16','Q18', 'Q20', 'Q21', 'Q23','Q27', 'Q28', 'PostQ30']:
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(first,1)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(second,2)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(third,3)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fourth,4)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fifth,5)

for column in ['Q15','Q17','Q19','Q22', 'Q24','Q25','Q26']:
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(first,5)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(second,4)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(third,3)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fourth,2)
    attitudinal_scales_df[column] = attitudinal_scales_df[column].replace(fifth,1)

df = df.replace(' ',np.nan)
for column, series in df.iteritems():
    if not column in ['Name', 'Prison_ID', 'ID']:
        df[column] = df[column].astype('category')

attitudinal_scales_df = attitudinal_scales_df.replace('33',3)
attitudinal_scales_df = attitudinal_scales_df.replace(' ',np.nan)

for column, series in df.iteritems():
    if column in ['Prison','Gender', 'Group', 'Data_Round', 'Samples']:
        df[column] = df[column].astype('category')

#creating a column for previous art experience
attitudinal_scales_df['art_experience'] = attitudinal_scales_df['PostQ1']
for index, values in attitudinal_scales_df['PreQ1'].iteritems():
    if values in ['Yes, both studied and practiced', 'Yes, practiced', 'Yes, studied' ]:
        attitudinal_scales_df.loc[index, 'art_experience'] = 'Yes'
        
    elif values == "No, I haven't":
        attitudinal_scales_df.loc[index, 'art_experience'] ='No'    

for column,questions in [('Time Management',['Q12','Q17','Q22']),
                ('Achievement Motivation',['Q13','Q18','Q16' ]),
                ('Intellectual Flexibility',['Q14','Q19','Q24','Q26']),
                ('Emotional Control',['Q15','Q20']),
                ('Self Confidence',['Q21']),
                ('Social Competence', ['Q23','Q25','Q27','Q28'])]:
    
    attitudinal_scales_df[column] = attitudinal_scales_df[questions].mean(axis=1,skipna=False)
    
attributes =  ['Time Management', 'Achievement Motivation', 'Intellectual Flexibility' , 'Emotional Control','Self Confidence' ,'Social Competence']
pre_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Pre Program']
post_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Post-Program']

columns_atscales = ['Prison', 'Name', 'Prison_ID', 'ID', 'Gender', 'Group', 'Data_Round', 'Samples','art_experience','Time Management',
 'Achievement Motivation', 'Intellectual Flexibility', 'Emotional Control',
 'Self Confidence', 'Social Competence']

pre_df = pd.DataFrame(pre_df, columns = columns_atscales)
post_df = pd.DataFrame(post_df, columns = columns_atscales)

def hist():
    post = post_df[attributes].dropna()
    pre=  pre_df[attributes].dropna()
    pre[attributes].hist()
    plt.suptitle("Pre-Program")
    
    post[attributes].hist()
    plt.suptitle("Post-Program")   
    plt.show()

def qqplot():
    return sm.qqplot(post_df['Time Management'],line = '45')
    
def test_normality():
    #for column in attributes:
    #     print column, sp.stats.shapiro(post_df[column])
    
    post_table = [["Time Management", 0.7989435195922852, 1.7665534833566365e-12],
                  ["Intellectual Flexibility", 0.8067236542701721, 3.310084845109529e-12],
                  ["Achievement Motivation" ,0.5009009838104248, 1.0594767746240141e-19],
                  ["Emotional Control", 0.8851432800292969, 6.317574907654944e-09],
                  ["Self Confidence", 0.609407901763916, 1.4120606676629398e-17],
                  ["Social Competence", 0.8981918692588806, 3.001261816848455e-08]]
    post = tabulate(post_table,headers = ["Attribute", "W stat", "p value"], floatfmt = ".2f", tablefmt = 'rst')

    #for column in attributes:
    #    print column, sp.stats.shapiro(pre_df[column])
    
    pre_table = [["Time Management", 0.9098374843597412, 8.103528159608686e-08],
                 ["Intellectual Flexibility", 0.9260804057121277, 8.383431122638285e-07],
                 ["Achievement Motivation" ,0.7117029428482056, 1.8042233763319697e-15],
                 ["Emotional Control", 0.9423717856407166, 1.190870170830749e-05,],
                 ["Self Confidence", 0.7873598337173462, 3.5050795274028934e-13],
                 ["Social Competence", 0.9072498083114624, 5.7175618906057935e-08]]

    pre = tabulate(pre_table,headers = ["Attribute", "W stat", "p value"], floatfmt = ".2f", tablefmt = 'rst')

    return (post, pre)

file1 = open("tables.txt",'w')
file1.write('Shapiro Wilk Test For Normality (Pre-Program)\n')
file1.write(test_normality()[1] + '\n' + 'W stat is significant for all attributes, therefore we can reject the null that the data comes from a normal distribution.\n\n')
file1.write('Shapiro Wilk Test For Normality (Post-Program)\n')
file1.write(test_normality()[0] + '\n' + 'W stat is significant for all attributes, therefore we can reject the null that the data comes from a normal distribution.\n\n\n\n')

#Data is not normal, therefore running non parametric tests. 

# Descriptive stats

def descriptive_stats():
    pre = pre_df[attributes].describe() 
    post = post_df[attributes].describe()
    #pre = tabulate(pre,headers = attributes,
    #                tablefmt = 'rst', floatfmt = '.2f')
    #post = tabulate(post, headers = attributes,
    #                tablefmt = 'rst', floatfmt = '.2f')
    writer = pd.ExcelWriter("stats_base.xlsx")
    pre.to_excel(writer, 'Sheet1')
    post.to_excel(writer, 'Sheet2')
    writer.save()
    
def mannwhitney(Samples = 'Independent'):
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Samples != 'Independent':
        pre_noart = pre_noart.loc[pre_noart['Samples'] == 'Paired']
        pre_art = pre_art.loc[pre_art['Samples'] == 'Paired']
        post_noart= post_noart.loc[post_noart['Samples'] =='Paired']
        post_art= post_art.loc[post_art['Samples'] == 'Paired']
    
    table_noart = []
    for column in attributes:
        u_noart, p_noart = sp.stats.mannwhitneyu(pre_noart[column],post_noart[column], use_continuity = False) 
        table_noart.append([column, u_noart, round(p_noart,4)])
        
    table_art = []
    for column in attributes:
        u_art, p_art = sp.stats.mannwhitneyu(pre_art[column],post_art[column], use_continuity = False) 
        table_art.append([column, u_art, round(p_art,4)])

    return (tabulate(table_noart, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'))

file1.write('Mann Whitney U test - Without Art Experience(Whole Sample)\n')
file1.write(mannwhitney()[0] +'\n\n\n\n')
file1.write('Mann Whitney U test - With Art Experience(Whole Sample)\n')
file1.write(mannwhitney()[1] + '\n\n\n\n')


def wilcoxon():
    ''' Signed Wilcoxon ranked test, only for paired samples
    '''   
    #pre = pre_df.loc[pre_df['Samples'] == 'Paired']
    #post = post_df.loc[post_df['Samples'] == 'Paired']
    
    pre = pre_df.loc[pre_df['Gender'] == 'Female']
    post = post_df.loc[post_df['Gender'] == 'Female']
    
    for column in attributes:        
        #diff = np.subtract(post[column], pre[column])
        t,p = sp.stats.wilcoxon(pre[column], post[column])
        print column, t, round(p,4)

def ranksums(Samples = 'Independent'):
    '''Wilcoxon for independent samples, like mann whitney
    '''
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Samples != 'Independent':
        pre_noart = pre_noart.loc[pre_noart['Samples'] == 'Paired']
        pre_art = pre_art.loc[pre_art['Samples'] == 'Paired']
        post_noart= post_noart.loc[post_noart['Samples'] =='Paired']
        post_art= post_art.loc[post_art['Samples'] == 'Paired']
    
    table_noart = []
    for column in attributes:
        z_noart, p_noart = sp.stats.ranksums(pre_noart[column],post_noart[column])
        table_noart.append([column, z_noart, round(p_noart,4)]) 
    
    table_art = []    
    for column in attributes:
        z_art, p_art = sp.stats.ranksums(pre_art[column],post_art[column])  
        table_art.append([column, z_art, round(p_art,4)]) 
    
    return (tabulate(table_noart, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','U stat', 'p value'], tablefmt = 'rst', floatfmt = '.4f'))

file1.write('Wilcoxon Rank Sums Test - Without Art Experience(Whole Sample)\n')
file1.write(ranksums()[0] +'\n\n\n\n')
file1.write('Wilcoxon Rank Sums Test - With Art Experience(Whole Sample)\n')
file1.write(ranksums()[1] + '\n\n\n\n')

def stats_artexp():
    pre_stats = pre_df.groupby('art_experience')
    grouped_pre = pre_stats[attributes].agg([np.count_nonzero, np.mean, np.std])
    post_stats = post_df.groupby('art_experience')
    grouped_post = post_stats[attributes].agg([np.count_nonzero, np.mean, np.std])
    
    writer = pd.ExcelWriter("stats_artexp.xlsx")
    grouped_pre.to_excel(writer, 'Sheet1')
    grouped_post.to_excel(writer, 'Sheet2')
    writer.save()

def ttest_ind(Gender = 'all'):
    pre_noart = pre_df.loc[pre_df['art_experience'] == 'No']
    pre_art = pre_df.loc[pre_df['art_experience'] == 'Yes']
    post_noart = post_df.loc[post_df['art_experience'] == 'No']
    post_art = post_df.loc[post_df['art_experience'] == 'Yes']
    
    if Gender == 'Male':
        pre_noart = pre_noart.loc[pre_noart['Gender'] == 'Male']
        pre_art = pre_art.loc[pre_art['Gender'] == 'Male']
        post_noart= post_noart.loc[post_noart['Gender'] == 'Male']
        post_art= post_art.loc[post_art['Gender'] == 'Male']
    
    table_noart = []
    for column in attributes:
        t_noart, p_noart = sp.stats.ttest_ind(pre_noart[column].dropna(),post_noart[column].dropna(),equal_var=False) 
        table_noart.append([column, t_noart, p_noart])
 
    table_art = []   
    for column in attributes:
        t_art, p_art = sp.stats.ttest_ind(pre_art[column].dropna(),post_art[column].dropna(),equal_var=False)
        table_art.append([column, t_art, p_art])

    return (tabulate(table_noart, headers = ['Attribute','t stat', 'p value'], tablefmt = "pipe", floatfmt = '.4f'),
            tabulate(table_art, headers = ['Attribute','t stat', 'p value'], tablefmt = "pipe", floatfmt = '.4f'))
        
file1.write('Independent Samples t-test - Without Art Experience(Whole Sample)\n')
file1.write(ttest_ind()[0] +'\n\n\n\n')
file1.write('Independent Samples t-test - With Art Experience(Whole Sample)\n')
file1.write(ttest_ind()[1] + '\n\n\n\n')

#altered for females(for pairing)

def ttest_paired(Gender='Female'):
    pre_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Pre Program']
    post_df = attitudinal_scales_df.loc[attitudinal_scales_df['Group']=='Post-Program']
    pre = pre_df.loc[pre_df['Gender'] == Gender]
    post = post_df.loc[post_df['Gender'] == Gender]
    
    #replacing missing values with 3(neutral score)
    
    for column in ['Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26','Q27', 'Q28',]:
        pre[column] = pre[column].replace(np.nan,3)
        post[column] = post[column].replace(np.nan,3)
    
    for attribute,questions in [('Time Management',['Q12','Q17','Q22']),
                ('Achievement Motivation',['Q13','Q18','Q16' ]),
                ('Intellectual Flexibility',['Q14','Q19','Q24','Q26']),
                ('Emotional Control',['Q15','Q20']),
                ('Self Confidence',['Q21']),
                ('Social Competence', ['Q23','Q25','Q27','Q28'])]:
    
        pre[attribute] = pre[questions].sum(axis=1,skipna=False)
        post[attribute] = post[questions].sum(axis=1,skipna=False)
        
    table = []
    for column in attributes:
        t, p = sp.stats.ttest_rel(pre[column], post[column]) 
        table.append([column, t, p])
    return (tabulate(table, headers = ['Attribute','t stat', 'p value'], tablefmt = "pipe", floatfmt = '.4f'))

file1.write('Paired Samples t-test - (Women Prison Data)\n')
file1.write(ttest_ind()[0] +'\n\n\n\n')
file1.close()
   


def chisq():
    attitudinal_scales_df['Num'] = np.arange(323)
    renamed_df = attitudinal_scales_df.rename(columns = {'PreQ4': 'Pursuing Education' , 'art_experience' : 'Previous Art Experience'})
    pivot = pd.pivot_table(renamed_df, values = ['Num'], index = 'Previous Art Experience', columns = 'Pursuing Education', aggfunc = np.count_nonzero)
    pivot = pivot.apply(lambda x: np.round(((x/x.sum())),4), axis=0)
    writer = pd.ExcelWriter("chisq.xlsx")
    pivot.to_excel(writer, 'Sheet1') 
    
    #computing chi sq without totals columns
    pivot_chisq = pd.pivot_table(renamed_df, values = ['Num'], index = 'Previous Art Experience', columns = 'Pursuing Education', aggfunc = np.count_nonzero)    
    chisq = sp.stats.chi2_contingency(pivot_chisq)
    stats = []
    for i in chisq[:2]:
        stats.append(round(i, 4))
    chi2 = pd.DataFrame(stats, index = ['chi2', 'p-value'])
    chi2.to_excel(writer, 'Sheet2')
    writer.save()

chisq()

# making a dictionary with labels
labels = {}

with open('varnames.txt') as f:
    for line in f:
        ls = line.split()
        #print ls
        labels[ls[0]] = ' '.join(ls[1:])
labels['art_experience'] = 'Previous Art Experience'


df['PreQ11c'] = df['PreQ11c'].replace('11','Yes')

def pre_pivot():  
    df['art_experience'] = df['PostQ1']
    for index, values in df['PreQ1'].iteritems():
        if values in ['Yes, both studied and practiced', 'Yes, practiced', 'Yes, studied' ]:
            df.loc[index, 'art_experience'] = 'Yes'
        elif values == "No, I haven't":
            df.loc[index, 'art_experience'] ='No' 
    
    df['Observations'] = np.arange(323)
    df_renamed = df.rename(columns = {'PreQ4': 'Pursued Education'})
    
    dict = {'PreQ3' : ['PreQ3a','PreQ3b', 'PreQ3c', 'PreQ3d', 'PreQ3e', 'PreQ3f', 'PreQ3g'],
            'PreQ5' : [ 'PreQ5a', 'PreQ5b', 'PreQ5c'],
            'PreQ10' : ['PreQ10a', 'PreQ10b', 'PreQ10c', 'PreQ10d', 'PreQ10e'],
            'PreQ11' : ['PreQ11a', 'PreQ11b', 'PreQ11c', 'PreQ11d', 'PreQ11e', 'PreQ11f', 'PreQ11g']}
    
    i = 0
    writer = pd.ExcelWriter('freq.xlsx')
    for k,v in dict.iteritems():
        i += 1
        ls = []
        for column in v:           
            pivot = pd.pivot_table(df_renamed, values = ['Observations'], columns = 'Pursued Education',
                            index = column, aggfunc = len, dropna = True)   
            ls.append(pivot)

        con = pd.concat(ls, keys = v)
        con = con.groupby(level=0).transform(lambda x: np.round(((x/x.sum())),4))

        renamed = con.rename(index = labels)
        renamed.to_excel(writer, sheet_name='Sheet' + str(i))
    writer.save()

pre_pivot()
def barplots():                              
    prison_count= df['Prison'].value_counts()
    prison_count.plot(kind = 'bar',title = 'Count of Prisons', color = ['r','b','g'] ,fontsize = 12)
    g = sns.factorplot('Prison', data=df , palette = 'Pastel1', legend= True,margin_titles = True)
    print g

def att_barplots():
    pre_df[attributes].plot(kind = 'bar',title = 'Count of Prisons', color = ['r','b','g'] ,fontsize = 12)




