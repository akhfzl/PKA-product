import pandas as pd

class Dataset:
    def __init__(self, dataset):
        self.dataset = dataset
        self.folder = 'dataset/'
        self.folder_target = self.folder + ('majors.csv' if dataset == 'jurusan' else 'score_humanities.csv' if dataset == 'humanity' else 'score_science.csv' if dataset == 'science' else 'universities.csv')
    
    def read_csv(self):
        df = pd.read_csv(self.folder_target)
        return df
    
    def saintek(self):
        df = self.read_csv() 
        df = df[['score_bio', 'score_fis', 'score_kmb', 'score_kpu', 'score_kua', 'score_mat', 'score_ppu']]

        df['mean'] = df.sum(axis=1) / 7
        return df.sort_values(by='mean', ascending=False).head(10)
    
    def soshum(self):
        df = self.read_csv() 
        df = df[['score_eko', 'score_geo', 'score_kmb', 'score_kpu', 'score_kua', 'score_mat', 'score_ppu', 'score_sej', 'score_sos']]

        df['mean'] = df.sum(axis=1) / 7
        return df.sort_values(by='mean', ascending=False).head(10)
    
    def update_field_process(self):
        myData = self.read_csv()
        if self.dataset == 'jurusan':
            df_univ = pd.read_csv(self.folder + 'universities.csv')
            myData = pd.merge(myData, df_univ, on='id_university')
            myData = myData[['major_name', 'university_name', 'type', 'capacity']]
            myData.rename(columns={'major_name': 'Nama Jurusan', 'capacity': 'kapasitas', 'university_name': 'Nama Universitas'}, inplace=True)
        else:
            myData.rename(columns={'university_name': 'Nama Universitas'}, inplace=True)
            myData = myData[['id_university', 'Nama Universitas']]
        
        return myData
    