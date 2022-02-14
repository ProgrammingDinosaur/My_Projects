import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import statistics

class InvalidDim(Exception):
    '''
    Raises Exception when given an array with more than 1-Dimension
    '''
    pass


##Tabla Disttribucion de Frec.##
def crear_tabla_integros(dataframe: pd.DataFrame,index = 1)->pd.DataFrame:
    '''
    Crea una tabla de distribucion de frecuencias dado un indice de columna y un Dataframe de Pandas, las clases se dividen por cada valor unico
        
        Parametros:
            dataframe: Dataframe de Pandas para realizar tabla, valor default = None

            index: indice de la tabla con los datos, valor default = 1

        Regresa:
            table: Pandas Dataframe
    '''
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
    
def crear_tabla_por_intervalos(dataframe: pd.DataFrame,start_val:int,end_val: int, intervalo: int,index = 1)->pd.DataFrame:
    '''
    Crea una tabla de distribucion de frecuencias con rango e intervalos predefinidos
    Parametros:

            dataframe: Dataframe de Pandas para realizar tabla, valor default = None
            start_val: Valor donde iniciar las clases
            end_val:  Valor donde terminar las clases
            intervalo: Valor por el que deben ir separadas las clases
            index: indice de la tabla con los datos, valor default = 1

        Regresa:
            table: Pandas Dataframe
    '''
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
def media_arit(dataframe: pd.DataFrame, index = 1)->np.ndarray:
    return np.mean(dataframe.iloc[:,index].values)

def media_geometrica(dataframe: pd.DataFrame, index = 1)->np.ndarray:
    return gmean(dataframe.iloc[:,index].values)

def mediana(dataframe: pd.DataFrame,index = 1)->np.ndarray:
    return np.median(dataframe.iloc[:,index].values)

def moda(dataframe: pd.DataFrame,index = 1)->np.ndarray:
    moda_list = list(dataframe.iloc[:,index].values)
    return statistics.mode(moda_list)

def media_ponderada(dataframe: pd.DataFrame,valores_idx = 1, pesos_idx = 2)->np.ndarray:
    return np.average(dataframe.iloc[:,valores_idx].values,weights=dataframe.iloc[:,pesos_idx].values)

def calcular_tasa(rango_valores: np.ndarray,media_tipo = 'arit')->np.ndarray:
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

def mediana_agrupada(tabla_dist: pd.DataFrame, frec_abs_idx = 1)->float:
    values = tabla_dist.iloc[:,frec_abs_idx].values
    total_frec_abs = np.sum(values)
    count = 0
    for idx,value in enumerate(values): 
        count += value
        if count > total_frec_abs:
            median_index = idx
            break
    rango = tabla_dist.iloc[median_index,0].split('-')
    first_arg = rango[0]
    second_arg = rango[1]
    a = second_arg-first_arg
    mediana_agrup = first_arg+((((np.sum(values))/2)-values[median_index-1])/(values[median_index]))*a
    return mediana_agrup

def moda_agrupada_mismos_intervalos(tabla_dist: pd.DataFrame,frec_abs_idx = 1)->float:
    values = tabla_dist.iloc[:,frec_abs_idx].values
    max_val = np.argmax(values)[0]
    rango = tabla_dist.iloc[max_val,0].split('-')
    first_arg = rango[0]
    second_arg = rango[1]
    a = second_arg-first_arg
    moda_agmi = first_arg+((values[max_val]+1)/(values[max_val-1]+values[max_val+1]))*a
    return moda_agmi



