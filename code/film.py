import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from surprise import Reader, Dataset, SVD, evaluate
import warnings
warnings.filterwarnings("ignore")



def predict(user_id,topk):

    #读取数据
    data = pd.read_csv("../data/data.dat",sep="\t",names=['userid','itemid','rating','timestamp'])

    #数据类型转换
    data['rating'] = data['rating'].astype(float)

    #数据分析，获取数据大小
    print('Dataset 1 shape: {}'.format(data.shape))

    #重建索引
    data.index = np.arange(0,len(data))
    print('Full dataset shape: {}'.format(data.shape))

    #计数
    p = data.groupby('rating')['rating'].agg(['count'])

    # 获取电影总数
    movie_count = data.isnull().sum()[1]

    # 获取用户总数
    cust_count = data['userid'].nunique() - movie_count

    # 获取评分总数
    rating_count = data['userid'].count() - movie_count

    #总体用户喜好分析
    ax = p.plot(kind = 'barh', legend = False, figsize = (15,10))
    plt.title('Total pool: {:,} Movies, {:,} customers, {:,} ratings given'.format(movie_count, cust_count, rating_count), fontsize=20)
    plt.axis('off')

    for i in range(1,6):
        ax.text(p.iloc[i-1][0]/4, i-1, 'Rating {}: {:.0f}%'.format(i, p.iloc[i-1][0]*100 / p.sum()[0]), color = 'white', weight = 'bold')


    '''
    影片ID是一个混乱的导入!通过dataframe循环添加电影ID列会使内核耗尽内存，
    因为它的效率太低。所以首先创建一个正确长度的numpy数组，
    然后将整个数组作为列添加到主数据dataframe中!
    '''
    df_nan = pd.DataFrame(pd.isnull(data.rating))
    df_nan = df_nan[df_nan['rating'] == True]
    df_nan = df_nan.reset_index()

    movie_np = []
    movie_id = 1

    for i,j in zip(df_nan['index'][1:],df_nan['index'][:-1]):

        temp = np.full((1,i-j-1), movie_id)
        movie_np = np.append(movie_np, temp)
        movie_id += 1

    '''
    现在的数据集非常庞大,所以需要进行数据预处理
    删除评论过少的电影(它们相对不受欢迎)
    删除评论过少的客户(他们相对不活跃)
    在matrix的观点中，不受欢迎的电影和不活跃的客户与受欢迎的电影和活跃的客户所占的数量相同
    '''
    #筛选出评分很少的电影
    f = ['count','mean']
    #将数据按照itemid进行分组，然后根据rating对数据聚合，求count,mean
    df_movie_summary = data.groupby('itemid')['rating'].agg(f)
    #设置处理后的数据索引数据类型
    df_movie_summary.index = df_movie_summary.index.map(int)
    movie_benchmark = round(df_movie_summary['count'].quantile(0.8),0)
    #筛选出不活跃的电影
    drop_movie_list = df_movie_summary[df_movie_summary['count'] < movie_benchmark].index
    print('Movie minimum times of review: {}'.format(movie_benchmark))

    #筛选出不活跃的用户
    df_cust_summary = data.groupby('userid')['rating'].agg(f)
    df_cust_summary.index = df_cust_summary.index.map(int)
    cust_benchmark = round(df_cust_summary['count'].quantile(0.8),0)
    drop_cust_list = df_cust_summary[df_cust_summary['count'] < cust_benchmark].index
    print('Customer minimum times of review: {}'.format(cust_benchmark))


    print('Original Shape: {}'.format(data.shape))
    df = data[~data['itemid'].isin(drop_movie_list)]
    df = df[~df['userid'].isin(drop_cust_list)]
    print('After Trim Shape: {}'.format(df.shape))
    df_p = pd.pivot_table(df,values='rating',index='userid',columns='itemid')



    #开始训练算法模型
    reader = Reader()

    #定义算法模型
    svd = SVD()

    #指定所需用户
    user_some = data[(data['userid'] == user_id) & (data['rating'] >3 )]
    user_some = user_some.set_index('itemid')
    user_some = user_some.reset_index()
    user_some = user_some[~user_some['itemid'].isin(drop_movie_list)]

    #将所有的数据集载入到data里面
    data = Dataset.load_from_df(df[['userid', 'itemid', 'rating']], reader)

    #将数据集转换为训练的数据集合
    trainset = data.build_full_trainset()
    svd.train(trainset)

    user_some['Estimate_Score'] = user_some['itemid'].apply(lambda x: svd.predict(user_id, x).est)
    user_some = user_some.sort_values('Estimate_Score', ascending=False)

    return user_some.head(topk)

if __name__ =="__main__":
    print(predict(12,10))
