import numpy as np, pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from data_preprocess import Dataset

class CBR:
    def __init__(self, query_user=None, type_jurusan=None, nama_jurusan=None, nama_univ=None):
        self.iterasi = 2
        self.query_user = query_user 
        self.type_jurusan = type_jurusan
        self.nama_jurusan = nama_jurusan
        self.nama_univ = nama_univ
    
    def databaseChecking(self):
        nama_file = 'score_science.csv' if self.type_jurusan == 'science' else 'score_humanities.csv'
        myData = pd.read_csv('dataset/' + nama_file)
        return myData 

    def filter_major(self):
        # db
        db = self.databaseChecking()

        # read jurusan and filter
        df_jurusan = pd.read_csv('dataset/majors.csv')
        df_jurusan = df_jurusan[df_jurusan['type'] == self.type_jurusan]
        df_jurusan = df_jurusan[df_jurusan['major_name'].str.contains(rf'{self.nama_jurusan}')]
        
        df_univ = pd.read_csv('dataset/universities.csv')

        df_all = pd.merge(df_jurusan, df_univ, on='id_university')
        df_all = df_all[df_all['university_name'] == self.nama_univ]
        
        return df_all['id_major'].values
        
    def suggest_euclidean(self):
         # db for filter major get major id
        db_major = self.filter_major()
        
        # db for result
        db_result = self.databaseChecking()
        
        cols_to_exclude = ['id_first_major', 'id_first_university', 
                   'id_second_major', 'id_second_university', 'id_user']
        
        db_result = db_result[db_result['id_first_major'].isin(db_major)]
        cols = [col for col in db_result.columns if col not in cols_to_exclude]
        db_result = db_result[cols]


        return db_result

# Dummy numerical data (replace this with your actual numerical data)
# database_data = np.random.rand(100, 10)  # feature

# Feature extraction: Use the raw numerical data as features
# database_features = database_data

# Query processing: Generate a random query instance
# query_instance = np.random.rand(10)  # Query with 10 numerical features

# Similarity measurement: Compute similarity scores using Euclidean distance
# distances = euclidean_distances([query_instance], database_features)[0]

# Result retrieval: Retrieve top k most similar instances
k = 5
# most_similar_indices = np.argsort(distances)[:k]
# most_similar_instances = database_data[most_similar_indices]

# Display the most similar instances
# print("Most similar instances:")
# print(most_similar_instances)
