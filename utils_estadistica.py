#Import Pandas and Excel library for DataFrame and Workbook manipulation

import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import statistics

class InvalidDim(Exception):
    pass


##Tabla Disttribucion de Frec.##
def crear_tabla_integros(dataframe: pd.DataFrame,index = 1):
    table = pd.DataFrame()
    uniques = dataframe.iloc[:,index].sort_values().unique()
    frec_abs = []
    for value in uniques:
        frec_abs.append((dataframe.iloc[:,index] == value).sum())
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
    
def crear_tabla_por_intervalos(dataframe: pd.DataFrame,start_val:int,end_val: int, intervalo: int,index = 1):
    table = pd.DataFrame()

    frec_abs = []
    rangos = []
    for i in range(start_val,end_val,intervalo):
        values = dataframe.iloc[:,index]
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
    

##Medidas Estadistica##
def media_arit(dataframe: pd.DataFrame, index = 1):
    return np.mean(dataframe.iloc[:,index].values)

def media_geometrica(dataframe: pd.DataFrame, index = 1):
    return gmean(dataframe.iloc[:,index].values)

def mediana(dataframe: pd.DataFrame,index = 1):
    return np.median(dataframe.iloc[:,index].values)

def moda(dataframe: pd.DataFrame,index = 1):
    moda_list = list(dataframe.iloc[:,index].values)
    return statistics.mode(moda_list)

def media_ponderada(dataframe: pd.DataFrame,valores_idx = 1, pesos_idx = 2):
    return np.average(dataframe.iloc[:,valores_idx].values,weights=dataframe.iloc[:,pesos_idx].values)

def calcular_tasa(rango_valores: np.ndarray,media_tipo = 'arit'):
    media_tipos = ['arit','gmean']
    if ((len(rango_valores.shape)) > 1):
        raise InvalidDim("The passed ndarray should be 1-dimensional")
    if media_tipo not in media_tipos:
        raise ValueError("Argument 'media_tipo' should be either 'arit' or 'gmean'")
    value_hist = []
    for idx,i in enumerate(rango_valores):
        if idx != 1:
            value_hist.append(i/rango_valores[idx-1])
    value_hist = np.array(value_hist)
    return np.mean(value_hist) if media_tipo == 'arit' else gmean(value_hist)

