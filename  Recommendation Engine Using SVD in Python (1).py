#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


data = pd.read_csv('/Users/sathishkosalram/Downloads/ratings.csv', usecols = ['userId', 'movieId', 'rating', 'timestamp'])


# In[3]:


data1 = pd.read_csv('/Users/sathishkosalram/Downloads/movies.csv', usecols = ['movieId', 'title', 'genres'])


# In[4]:


data1.head()


# In[5]:


data.head()


# In[10]:


n_users = data.userId.unique().shape[0]
n_movies = data.movieId.unique().shape[0]
print(f'Number of users = {n_users} and Numbers of movies = {n_movies}')


# In[11]:


Data = data.pivot(index = 'userId', columns = 'movieId', values = 'rating').fillna(0)


# In[12]:


Data.head()


# In[18]:


from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
reader = Reader()
data2 = Dataset.load_from_df(data[['userId', 'movieId', 'rating']], reader)
svd = SVD()
cross_validate(svd, data, measures = ['RMSE', 'MAE'], cv = 3, verbose = True)


# In[19]:


data_1 = data[(data['userId'] == 5) & (data['rating'] == 5)]
data_1 = data_1.set_index('movieId')
data_1 = data_1.join(movies)['title']
data_1.head(10)


# In[21]:


data_5 = data1.copy()
data_5 = data1.reset_index()
data_6 = Dataset.load_from_df(data[['userId','movieId','rating']],reader)


# In[22]:


trainset = data_6.build_full_trainset()
svd.fit(trainset)


# In[23]:


data_5['Estimate_Score'] = data_5['movieId'].apply(lambda x: svd.predict(1,x).est)
data_5 = data_5.drop(['movieId', 'genres', 'index'], axis = 1)
data_5 = data_5.sort_values('Estimate_Score', ascending = False)
print(data_5.head(10))


# In[ ]:




