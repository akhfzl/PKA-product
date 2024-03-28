import numpy as np, pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from data_preprocess import Dataset

class CBR:
    def __init__(self, query_user=None, type_jurusan=None, nama_jurusan=None, nama_univ=None):
        self.iterasi = 2
        self.query_user = query_user 
        self.type_jurusan = type_jurusan
        self.nama_jurusan = nama_jurusan
        self.nama_univ = nama_univ
        self.kapasitas_jurusan = 0
        self.total_col = 0
    
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
        df_all = df_all[df_all['university_name'].str.contains(rf'{self.nama_univ}')]
        
        if len(df_all['university_name'].values) == 0:
            print('Univ dan jurusan tidak ditemukan')
    
        self.kapasitas_jurusan = df_all['capacity'].values[0]

        return df_all['id_major'].values
        
    def count_average(self, indexing):
         # db for filter major get major id
        db_major = self.filter_major()
        
        # db for result
        db_result = self.databaseChecking()
        
        cols_to_exclude = ['id_first_major', 'id_first_university', 
                   'id_second_major', 'id_second_university', 'id_user', 'Unnamed: 0']
        
        db_result = db_result[db_result['id_first_major' if indexing < 1 else 'id_second_major'].isin(db_major)]
        cols = [col for col in db_result.columns if col not in cols_to_exclude]
        db_result = db_result[cols]
        db_result['average'] = db_result.sum(axis=1) / 7
        self.total_col = len(db_result.columns) - 1

        return db_result.sort_values(by='average', ascending=False)
    
    def passing_grade(self):
        user_input_avg = np.sum(self.query_user)
        myArr = []

        for i in range(self.iterasi):
            dictionary = {}
            list_data = self.count_average(i)
            avg = user_input_avg / len(list_data.columns)
            listDataAvg = list_data['average'].values 
            listDataAvg = np.append(listDataAvg, avg)
            listDataAvg = sorted(listDataAvg, reverse=True)
            howKnowIndex = listDataAvg.index(avg) + 1
            if howKnowIndex > self.kapasitas_jurusan:
                dictionary[f'Pilihan > {self.kapasitas_jurusan}'] = f'Coba lagi!! \n Berdasarkan jumlah pesaing dan rata-rata, nilai anda belum memenuhi yaitu berada di peringkat {howKnowIndex}/{len(listDataAvg) + 1}'
            if howKnowIndex <= self.kapasitas_jurusan:
                dictionary[f'Pilihan < {self.kapasitas_jurusan}'] = f'Selamat!! \n Berdasarkan jumlah pesaing dan rata-rata, nilai anda telah memenuhi yaitu berada di peringkat {howKnowIndex}/{len(listDataAvg) + 1}'
            
            myArr.append(dictionary)
            
        return dictionary

    def recommendation(self):
        db = self.databaseChecking()
        cols_to_exclude = ['id_first_major', 'id_first_university', 
                   'id_second_major', 'id_second_university', 'id_user', 'Unnamed: 0']
       
        cols = [col for col in db.columns if col not in cols_to_exclude]
        db_result = db[cols]

        # Define two sets of numeric vectors (2D data)
        vectors1 = np.array(db_result.values)
        vectors2 = np.array([self.query_user])

        # Compute cosine similarity
        similarity_matrix = cosine_similarity(vectors1, vectors2)
        max_index = np.argmax(similarity_matrix)
        id_first_major = db['id_first_major'][max_index]
        id_sec_major = db['id_second_major'][max_index]
        list_id_major = [id_first_major, id_sec_major]

        id_first_university = db['id_first_university'][max_index]
        id_second_university = db['id_first_university'][max_index]
        list_id_univ = [id_first_university, id_second_university]

        df_univ = pd.read_csv('dataset/universities.csv')
        
        df_univ = df_univ[df_univ['id_university'].isin(list_id_univ)]

        df_majors = pd.read_csv('dataset/majors.csv')
        df_majors = df_majors[df_majors['id_major'].isin(list_id_major)]

        print('-- Univ rekomendasi -- \n', ' , '.join(df_univ['university_name'].values))
        print('-- Jurusan rekomendasi -- \n', ' , '.join(df_majors['major_name'].values))

