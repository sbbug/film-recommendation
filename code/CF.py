import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from surprise import Reader, Dataset, SVD, evaluate
import warnings
warnings.filterwarnings("ignore")

# Skip date
data = pd.read_csv("../data/data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

data['rating'] = data['rating'].astype(float)

print('Dataset 1 shape: {}'.format(data.shape))
print('-Dataset examples-')
print(data.iloc[::5000000, :])


data.index = np.arange(0,len(data))
print('Full dataset shape: {}'.format(data.shape))
print('-Dataset examples-')
print(data.iloc[::5000000, :])

p = data.groupby('rating')['rating'].agg(['count'])

# get movie count
movie_count = data.isnull().sum()[1]

# get customer count
cust_count = data['userid'].nunique() - movie_count

# get rating count
rating_count = data['userid'].count() - movie_count

ax = p.plot(kind = 'barh', legend = False, figsize = (15,10))
plt.title('Total pool: {:,} Movies, {:,} customers, {:,} ratings given'.format(movie_count, cust_count, rating_count), fontsize=20)
plt.axis('off')

for i in range(1,6):
    ax.text(p.iloc[i-1][0]/4, i-1, 'Rating {}: {:.0f}%'.format(i, p.iloc[i-1][0]*100 / p.sum()[0]), color = 'white', weight = 'bold')

df_nan = pd.DataFrame(pd.isnull(data.rating))
df_nan = df_nan[df_nan['rating'] == True]
df_nan = df_nan.reset_index()

movie_np = []
movie_id = 1

for i,j in zip(df_nan['index'][1:],df_nan['index'][:-1]):
    # numpy approach
    temp = np.full((1,i-j-1), movie_id)
    movie_np = np.append(movie_np, temp)
    movie_id += 1

f = ['count','mean']

df_movie_summary = data.groupby('itemid')['rating'].agg(f)
df_movie_summary.index = df_movie_summary.index.map(int)
movie_benchmark = round(df_movie_summary['count'].quantile(0.8),0)
drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index

print('Movie minimum times of review: {}'.format(movie_benchmark))

df_cust_summary = data.groupby('userid')['rating'].agg(f)
df_cust_summary.index = df_cust_summary.index.map(int)
cust_benchmark = round(df_cust_summary['count'].quantile(0.8),0)
drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index

print('Customer minimum times of review: {}'.format(cust_benchmark))

print('Original Shape: {}'.format(data.shape))
df = data[~data['itemid'].isin(drop_movie_list)]
df = df[~df['userid'].isin(drop_cust_list)]
print('After Trim Shape: {}'.format(df.shape))
print('-Data Examples-')
print(df.iloc[::5000000, :])

df_p = pd.pivot_table(df,values='rating',index='userid',columns='itemid')

print(df_p.shape)

reader = Reader()

# get just top 100K rows for faster run time
#data = Dataset.load_from_df(df[['userid', 'itemid', 'rating']], reader)
# data.split(n_folds=3)
#
svd = SVD()
# evaluate(svd, data, measures=['RMSE', 'MAE'])

user_5 = data[(data['userid'] == 10) & (data['rating'] ==5 )]
#print(user_5)
user_5 = user_5.set_index('itemid')


user_5 = user_5.reset_index()
user_5 = user_5[~user_5['itemid'].isin(drop_movie_list)]

# getting full dataset
data = Dataset.load_from_df(df[['userid', 'itemid', 'rating']], reader)

trainset = data.build_full_trainset()
svd.train(trainset)

user_5['Estimate_Score'] = user_5['itemid'].apply(lambda x: svd.predict(10, x).est)

#user_785314 = user_5.drop('Movie_Id', axis = 1)

user_5 = user_5.sort_values('Estimate_Score', ascending=False)
print(user_5.head(10))

