import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
import statistics

class InvalidDim(Exception):
    '''
    Raises Exception when given an array with more than 1-Dimension
    '''
    pass


##Tabla Distribucion de Frecuencias##
def crear_tabla_integros(dataframe: pd.DataFrame,index = 1)->pd.DataFrame:
    """
    Crea una tabla de distribucion de frecuencias dado un indice de columna y un Dataframe de Pandas, las clases se dividen por cada valor unico
        
        Parametros:
            dataframe: Dataframe de Pandas para realizar tabla, valor default = None

            index: indice de la tabla con los datos, valor default = 1

        Regresa:
            table: Pandas Dataframe
    """
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
    """
    Crea una tabla de distribucion de frecuencias con rango e intervalos predefinidos
    Parametros:

            dataframe: Dataframe de Pandas para realizar tabla, valor default = None
            start_val: Valor donde iniciar las clases
            end_val:  Valor donde terminar las clases
            intervalo: Valor por el que deben ir separadas las clases
            index: indice de la tabla con los datos, valor default = 1

        Regresa:
            table: Pandas Dataframe
    """
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
    """
    Toma valores de un DataFrame y saca la media aritmetica de los valores

    Parametros:
        dataframe: DataFrame de Pandas de donde sacar los valores
        index: indice donde esta la columna con los datos

    Regresa:
        Numpy array con el valor de la media (puede ser transformado a float simple)    
    """
    return np.mean(dataframe.iloc[:,index].values)

def media_geometrica(dataframe: pd.DataFrame, index = 1)->np.ndarray:
    """
    Toma valores de un DataFrame y saca la media geometrica de los valores

    Parametros:
        dataframe: DataFrame de Pandas de donde sacar los valores
        index: indice donde esta la columna con los datos

    Regresa:
        Numpy array con el valor de la media (puede ser transformado a float simple)    
    """
    return gmean(dataframe.iloc[:,index].values)

def mediana(dataframe: pd.DataFrame,index = 1)->np.ndarray:
    """
    Toma valores de un DataFrame y saca la mediana de los valores (no importa si no son pares)
    NOTA: No usar con datos agrupados, ver funcion "mediana_agrupada"

    Parametros:
        dataframe: DataFrame de Pandas de donde sacar los valores
        index: indice donde esta la columna con los datos

    Regresa:
        Numpy array con el valor de la mediana (puede ser transformado a float simple)    
    """
    return np.median(dataframe.iloc[:,index].values)

def moda(dataframe: pd.DataFrame,index = 1)->np.ndarray:
    """
    Toma valores de un DataFrame y saca la moda de los valores
    NOTA: No usar con datos agrupados, ver funcion "moda_agrupada_mismos_intervalos" o "moda_agrupada_rangos_diferentes"

    Parametros:
        dataframe: DataFrame de Pandas de donde sacar los valores
        index: indice donde esta la columna con los datos

    Regresa:
        Numpy array con el valor de la moda (puede ser transformado a float o int simple)    
    """
    moda_list = list(dataframe.iloc[:,index].values)
    return statistics.mode(moda_list)

def media_ponderada(dataframe: pd.DataFrame,valores_idx = 1, pesos_idx = 2)->np.ndarray:
    """
    Toma valores de un DataFrame y saca la media ponderada de los valores, de acuerdo a los pesos asignados

    Parametros:
        dataframe: DataFrame de Pandas de donde sacar los valores
        valores_idx: indice donde esta la columna con los datos a los cuales sacar la media
        pesos_idx: indice de la columna donde estan los pesos con los cuales calcular la media ponderada

    Regresa:
        Numpy array con el valor de la media ponderada(puede ser transformado a float simple)    
    """
    return np.average(dataframe.iloc[:,valores_idx].values,weights=dataframe.iloc[:,pesos_idx].values)

def anadir_estimaciones(df: pd.DataFrame, value_idx: int, media: float, media_tipo = 'aritmetica')-> pd.DataFrame:
    """
    Toma los valores del dataframe y la media de crecimiento que se le quiera asignar, añadira una fila nueva para que quepan las estimaciones.
    También añadira una columna para poner las estimaciones.

    Parametros:
        df: DataFrame de Pandas con los datos
        value_idx: Indice de la columna con los valores a multiplicar
        media: media *precalculada* con la cual hacer los calculos
        media_tipo: el tipo de media con el se aplicaran los calculos, esto es para referencia de texto del programa solamente, valor default='aritmetica'.

    Regresa:
        Dataframe con los datos añadidos
    """
    cols = df.columns
    vals = df.iloc[:,value_idx].values
    df2 = pd.DataFrame({cols[0]:['x'],cols[value_idx]:['NA']})
    df = pd.concat([df,df2],join='inner')
    estimaciones = [0]
    for val in vals:
        estimaciones.append(val*((media/100)+1))
    txt_est = 'Estimaciones media '+media_tipo
    df[txt_est] = estimaciones
    return df

def mediana_agrupada(tabla_dist: pd.DataFrame, frec_abs_idx = 1)->float:
    """
    Toma valores de un DataFrame agrupado en una distribucion de frecuencias y saca la mediana

    NOTAS:
        No usar con datos separados, ver funcion "mediana"
        La primera columna debe representar los rangos de la clase de la siguiente manera: p.ej [12-18], [18-26],etc... esto es para que el algoritmo pueda usar estos rangos en forma de texto y convertirlos al numero.
    
    Parametros:
        tabla_dist: DataFrame en formato de distribucion de frecuencias
        frec_abs_idx: integro con la columna en la que estan las frecuencias absolutas

    Regresa:
        mediana en forma de float
    """
    values = tabla_dist.iloc[:,frec_abs_idx].values
    total_frec_abs = np.sum(values)
    count = 0
    for idx,value in enumerate(values): 
        prev_count = count
        count += value
        if count > (total_frec_abs/2):
            median_index = idx
            break
    rango = tabla_dist.iloc[median_index,0].split('-')
    first_arg = int(rango[0])
    second_arg = int(rango[1])
    a = second_arg-first_arg
    mediana_agrup = first_arg+((((np.sum(values))/2)-values[median_index-1])/(values[median_index]))*a
    return round(mediana_agrup,2)

def moda_agrupada_mismos_intervalos(tabla_dist: pd.DataFrame,frec_abs_idx = 1)->float:
    """
    Toma valores de un DataFrame agrupado en una distribucion de frecuencias y saca la moda para intervalos iguales

    NOTAS:
        No usar con datos separados, ver funcion "moda"
        La primera columna debe representar los rangos de la clase de la siguiente manera: p.ej [12-18], [18-26],etc... esto es para que el algoritmo pueda usar estos rangos en forma de texto y convertirlos al numero.
        Los intervalos deben ser *iguales*, de tener datos agrupados con intervalos diferentes  ver funcion "moda_agrupada_rangos_diferentes"
    Parametros:
        tabla_dist: DataFrame en formato de distribucion de frecuencias
        frec_abs_idx: integro con la columna en la que estan las frecuencias absolutas

    Regresa:
        moda en forma de float
    """
    values = tabla_dist.iloc[:,frec_abs_idx].values
    max_val = np.argmax(values)[0]
    rango = tabla_dist.iloc[max_val,0].split('-')
    first_arg = rango[0]
    second_arg = rango[1]
    a = int(second_arg)-int(first_arg)
    moda_agmi = first_arg+((values[max_val]+1)/(values[max_val-1]+values[max_val+1]))*a
    return moda_agmi

def moda_agrupada_intervalos_diferentes(tabla_dist: pd.DataFrame, frec_abs_idx = 1)->float:
    """
    Toma valores de un DataFrame agrupado en una distribucion de frecuencias y saca la moda para intervalos distintos

    NOTAS:
        No usar con datos separados, ver funcion "moda"
        La primera columna debe representar los rangos de la clase de la siguiente manera: p.ej [12-18], [18-26],etc... esto es para que el algoritmo pueda usar estos rangos en forma de texto y convertirlos al numero.
        Esta funcion utiliza la funcion para intervalos distintos, de tener datos agrupados con intervalos iguales  ver funcion "moda_agrupada_mismos_intervalos"
    Parametros:
        tabla_dist: DataFrame en formato de distribucion de frecuencias
        frec_abs_idx: integro con la columna en la que estan las frecuencias absolutas

    Regresa:
        moda en forma de float
    """
    values = tabla_dist.iloc[:,frec_abs_idx].values
    ranges = [(int(r.split('-')[1])-int(r.split('-')[0])) for r in tabla_dist.iloc[:,0].values]
    frecuencia_normalizada = []
    for idx,i in enumerate(ranges):
        frecuencia_normalizada.append(values[idx]/i)
    frecuencia_normalizada = np.array(frecuencia_normalizada)
    moda_indice = np.argmax(frecuencia_normalizada)[0]
    lim_inf_mod = (tabla_dist.iloc[moda_indice,0].split('-'))[0]
    moda_id = lim_inf_mod+((frecuencia_normalizada[moda_indice]-frecuencia_normalizada[moda_indice-1]) \
    /((frecuencia_normalizada[moda_indice]-frecuencia_normalizada[moda_indice-1])+ \
    (frecuencia_normalizada[moda_indice]-frecuencia_normalizada[moda_indice+1])))*ranges[moda_indice]
    return moda_id


