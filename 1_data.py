import pandas as pd
import matplotlib.pyplot as plt

# load data in annual-unemployment-region
UK_gender = pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Gender', header=[0, 1], index_col=0, nrows=20).dropna(axis=1, how='all')
LDN_gender =  pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Gender', header=[0, 1], index_col=0, skiprows=23).dropna(axis=1, how='all')
UK_dis =  pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Disability', header=[0, 1], index_col=0, nrows=20).dropna(axis=1, how='all')
LDN_dis =  pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Disability', header=[0, 1], index_col=0, skiprows=23).dropna(axis=1, how='all')
UK_eth = pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Ethnicity', header=[0, 1], index_col=0, nrows=20).dropna(axis=1, how='all')
LDN_eth = pd.read_excel('annual-unemployment-region.xlsx', sheet_name='Ethnicity', header=[0, 1], index_col=0, skiprows=23).dropna(axis=1, how='all')
LDN_eth = LDN_eth.iloc[:-3,:]

def check_data_quality(df):
    df = df.replace('-', pd.NA)
    missing_values_per_row = df.isnull().sum(axis=1)
    
    problematic_rows = missing_values_per_row[missing_values_per_row > 0]
    print(f"Rows with more than 0 missing values:")
    if not problematic_rows.empty:
        print(problematic_rows)
    else:
        print("No rows with excessive missing values.\n")

df_list = [UK_gender, LDN_gender, UK_dis, LDN_dis, UK_eth, LDN_eth]
name = ['UK_gender', 'LDN_gender', 'UK_dis', 'LDN_dis', 'UK_eth', 'LDN_eth']
for i in range(6):
    print(name[i])
    check_data_quality(df_list[i])

UK_dis = UK_dis.dropna(axis=0, how='all')
LDN_dis = LDN_dis.dropna(axis=0, how='all')

def explore_data(df):
    print('df info: ', df.info())
    #print(df.shape)
    #print(df.columns)
    #print('df type: ', df.dtypes)
    print(df.describe())
    

for i in range(6):
    print('##################################')
    print(name[i])
    explore_data(df_list[i])




male_data = LDN_gender['Unemployment rate males - aged 16+']['percent'].rename('male')
female_data = LDN_gender['Unemployment rate females - aged 16+']['percent'].rename('female')
ratio = (male_data/female_data).rename('m/f ratio')

q1 = pd.concat([male_data, female_data, ratio], axis=1)
q1.to_csv('q1.csv', index=True)
print(q1.describe())

def barplot(x, save_file_name):
    plt.figure(figsize=(3, 4))
    plt.boxplot(x,  patch_artist=True, boxprops=dict(facecolor='lightblue'))  #vert=False,
    plt.ylabel('Value')
    plt.xticks([1],[x.name])
    #plt.show()
    plt.savefig(save_file_name+'.png', bbox_inches='tight')
barplot(q1['m/f ratio'], 'q1')

uk_data = UK_gender['Unemployment rate - aged 16+']['percent'].rename('UK')
ldn_data = LDN_gender['Unemployment rate - aged 16+']['percent'].rename('LDN')
ratio = (uk_data/ldn_data).rename('U/L ratio')
q2 = pd.concat([uk_data, ldn_data, ratio], axis=1)
print(q2.describe())
q2.to_csv('q2.csv', index=True)

barplot(q2['U/L ratio'],'q2')

def plot(df):
    df.index = df.index.map(lambda x:x[-4:])
    df.plot()
    plt.ylim(0,10)
    plt.savefig('q3.png', bbox_inches='tight')
plot(ldn_data)


