import numpy as np


#获取用户喜好的电影
def predict(user_id,topk):

    print("加载模型开始预测")
    film_topic = np.loadtxt("./theta_end.txt")
    topic_user = np.loadtxt("./phi_end.txt")

    #获取该用户下的主题分布
    user_topic = topic_user[:,user_id]
    #获取用户最喜欢的主题
    topic = np.argmax(user_topic)
    #索引该用户在这个主题下的所有电影
    films = film_topic[:,topic]
    films_index = np.argsort(films)
    films_index = films_index+1


    return list(films_index[:topk])

if __name__ =="__main__":
    print(getLikedFilms(1,3))
