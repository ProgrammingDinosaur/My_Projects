#Import Pandas and Excel library for DataFrame and Workbook manipulation

import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import statistics

class TablaDistribucionFrecuencias:
    
    def crear_tabla_integros(self,dataframe: pd.DataFrame):
        table = pd.DataFrame()
        uniques = dataframe.iloc[:,1].sort_values().unique()
        frec_abs = []
        for value in uniques:
            frec_abs.append((dataframe.iloc[:,1] == value).sum())
        total = np.sum(np.array(frec_abs))
        table['Valores'] = uniques
        table['Frec Abs'] = frec_abs
        table['Frec Rel'] = 0
        table['Frec Abs Ac'] = 0
        table['Frec Rel Ac'] = 0
        for idx,value in enumerate(frec_abs):
            table.iloc[idx,2] = str(round(value/total,2))
        print(frec_abs)
        for idx,value in enumerate(frec_abs):
            table.iloc[idx,3] = value if idx == 0 else value + table.iloc[idx-1,3]
            table.iloc[idx,4] = str(round(value/total,2)) if idx == 0 else (float(round(value/total,2)) + float(table.iloc[idx-1,4]))

        return table
    
    def crear_tabla_por_intervalos(self,dataframe: pd.DataFrame,start_val:int,end_val: int, intervalo: int):
        table = pd.DataFrame()
    
        frec_abs = []
        rangos = []
        for i in range(start_val,end_val+1,intervalo):
            values = dataframe.iloc[:,1]
            total = 0
            for value in values:
                if value < i+intervalo and value >= i:
                    total +=1
            frec_abs.append(total)
            
            rangos.append(str(i)+"-"+str(i+intervalo))
        total_values = np.sum(np.array(frec_abs))
        print(rangos)
        table['Valores'] = rangos
        table['Frec Abs'] = frec_abs
        table['Frec Rel'] = 0
        table['Frec Abs Ac'] = 0
        table['Frec Rel Ac'] = 0
        for idx,value in enumerate(frec_abs):
            table.iloc[idx,2] = str(round(value/total_values,2))
        for idx,value in enumerate(frec_abs):
            table.iloc[idx,3] = value if idx == 0 else value + table.iloc[idx-1,3]
            table.iloc[idx,4] = str(round(value/total_values,2)) if idx == 0 else (float(round(value/total_values,2)) + float(table.iloc[idx-1,4]))

        return table
        
class MedidasEstadistica:
    
    def media_arit(self,dataframe: pd.DataFrame, index = 1):
        return np.mean(dataframe.iloc[:,index].values)

    def media_geometrica(self,dataframe: pd.DataFrame, index = 1):
        return gmean(dataframe.iloc[:,index].values)

    def mediana(self,dataframe: pd.DataFrame,index = 1):
        return np.median(dataframe.iloc[:,index].values)
    
    def moda(self,dataframe: pd.DataFrame,index = 1):
        moda_list = list(dataframe.iloc[:,index].values)
        return statistics.mode(moda_list)


