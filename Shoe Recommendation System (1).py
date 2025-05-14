#!/usr/bin/env python
# coding: utf-8

# In[188]:


import pandas as pd


shoes = pd.read_csv('/Users/sathishkosalram/Downloads/finished_shoe_data.csv')


# In[189]:


import re

def clean_shoe_name(shoe_name):
    return re.sub("[^a-zA-Z0-9 ]", "", shoe_name)


# In[190]:


shoes['clean_shoe_name'] = shoes['Name'].apply(clean_shoe_name)


# In[191]:


if 'name' in shoes.columns:
    # Drop the last occurrence of 'name' by selecting its index
    last_name_index = shoes.columns.get_loc('name')
    shoes = shoes.drop(shoes.columns[last_name_index], axis=1)
shoes.columns = ['shoeid', 'Name', 'Genre', 'URL', 'Image URL', 'clean_shoe_name']
print(shoes.columns)


# In[150]:


from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(shoes['clean_shoe_name'])


# In[197]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def search(name):  
    name = clean_shoe_name(name)
    query_vec = vectorizer.transform([name])
    similarity = cosine_similarity(query_vec, tfidf).flatten()
    indices = np.argpartition(similarity, -5)[-5:]
    results = shoes.iloc[indices][['shoeid', 'Name', 'Genre', 'URL', 'Image URL', 'clean_shoe_name']][::-1]
    return results


# In[198]:


results


# In[72]:


import ipywidgets as widgets
from IPython.display import display

shoe_input = widgets.Text(
    values = "Nike", 
    description="Shoe Name:", 
    disabled=False 
)
shoe_list = widgets.Output()

def on_type(change):
    with shoe_list:
        shoe_list.clear_output()
        name = change['new']
        if len(name) > 5:
            display(search(name))

shoe_input.observe(on_type, names='value')

display(shoe_input, shoe_list)


# In[82]:


ratings = pd.read_csv('/Users/sathishkosalram/Downloads/new_ratings.csv')


# In[83]:


shoe_id = 1


# In[106]:


similar_users = ratings[(ratings['shoeid'] == shoe_id) & (ratings['ratings'] >= 2.5)]['userids'].unique()


# In[107]:


similar_users


# In[118]:


similar_user_recs = ratings[(ratings['userids'].isin(similar_users)) & (ratings['ratings'] >= 2.5)]['shoeid']


# In[119]:


similar_user_recs


# In[124]:


similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

similar_user_recs = similar_user_recs[similar_user_recs > .1]


# In[125]:


similar_user_recs


# In[126]:


all_users = ratings[ratings['shoeid'].isin(similar_user_recs.index) & (ratings['ratings'] > 3)]


# In[127]:


all_users


# In[128]:


all_user_recs = all_users['shoeid'].value_counts() / len(all_users['userids'].unique())


# In[129]:


all_user_recs


# In[131]:


rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
rec_percentages.columns = ['similar', 'all']


# In[132]:


rec_percentages


# In[133]:


rec_percentages['score'] = rec_percentages['similar'] / rec_percentages['all']


# In[134]:


rec_percentages = rec_percentages.sort_values('score', ascending=False) 


# In[135]:


rec_percentages


# In[164]:


rec_percentages.head(10).merge(shoes, left_index=True, right_on='shoeid')


# In[205]:


def find_similar_shoes(shoe_id):
    similar_users = ratings[(ratings['shoeid'] == shoe_id) & (ratings['ratings'] >= 2)]['userids'].unique()
    similar_user_recs = ratings[(ratings['userids'].isin(similar_users)) & (ratings['ratings'] >= 2)]['shoeid']
    
    similar_user_recs = similar_user_recs.value_counts() / len(similar_users)
    similar_user_recs = similar_user_recs[similar_user_recs > .1]
    
    all_users = ratings[ratings['shoeid'].isin(similar_user_recs.index) & (ratings['ratings'] > 2)]
    all_user_recs = all_users['shoeid'].value_counts() / len(all_users['userids'].unique())
    
    rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
    rec_percentages.columns = ['similar', 'all']
    
    rec_percentages['score'] = rec_percentages['similar'] / rec_percentages['all']
    rec_percentages = rec_percentages.sort_values('score', ascending=False)
    
    return rec_percentages.head(10).merge(shoes, left_index=True, right_on='shoeid')[['score', 'Name', 'Genre']]


# In[210]:


shoe_input_name = widgets.Text(
    values = "Nike", 
    description="Shoe Name:", 
    disabled=False 
)

recommendation_list = widgets.Output()

def on_type(data):
    with recommendation_list:
        recommendation_list.clear_output()
        name = data['new']
        if len(name) > 5:
            results = search(name)
            shoe_id = results.iloc[0]['shoeid']
            display(find_similar_shoes(shoe_id))

shoe_input_name.observe(on_type, names='value')
display(shoe_input_name, recommendation_list)


# In[ ]:




