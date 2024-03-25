from data_preprocess import Dataset
from cbr import CBR

def mainly():
    print("""
        --- Display feature ---
          Mau melihat data apa ?
          1. Universitas
          2. Jurusan
          3. Nilai tertinggi Saintek tahun lalu
          4. Nilai tertinggi Soshum tahun lalu
          5. CEK PASSING GRADE
          0. BACK
    """)

    try:
        ask_require_data = int(input('Kemana anda ingin menjelajah: '))
        if ask_require_data == 1:
            myData = Dataset('universitas')
            myData = myData.update_field_process()

        elif ask_require_data == 2:
            myData = Dataset('jurusan')
            myData = myData.update_field_process()

        elif ask_require_data == 3:
            myData = Dataset('science')
            myData = myData.saintek()
        
        elif ask_require_data == 4:
            myData = Dataset('humanity')
            myData = myData.soshum()
        
        elif ask_require_data == 5:
            ask_more_type = str(input('tipe jurusan (science/humanity) ? : '))
            ask_more_major = str(input('Apakah jurusan tujuanmu ? : ')).upper()
            ask_more_univ = str(input('Apakah universitas tujuanmu ? : ')).upper()
            ask_more_result = list(input('List nilai ? : '))
            myData = CBR(ask_more_result, ask_more_type, ask_more_major, ask_more_univ)
            myData = myData.suggest_euclidean()
        else:
            return False

        if ask_require_data in [1, 2]:
            ask_more_searching = str(input('Mau mencari jurusan ? : '))
            if ask_require_data == 1:
                result = myData[myData['Nama Universitas'].str.contains(rf'{ask_more_searching}')]
            else: 
                result = myData[myData['Nama Jurusan'].str.contains(rf'{ask_more_searching}')]

            return result
        else:
            return myData
        
    except ValueError:
        return mainly()

if __name__ == '__main__':
    not_stop = True
    while not_stop == True:
        running = mainly()
        if running is False:
            not_stop = running

        print(running)