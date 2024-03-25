import pandas as pd

def alpha_beta(df):
    
    df.loc[df['Alpha']<0 , 'weights'] +=0 
    df.loc[df['Alpha']>0 , 'weights'] +=1 
    df.loc[df['Alpha']>1.5, 'weights']+=1 
    df.loc[df['Alpha']>3 , 'weights'] +=1 
    df.loc[df['Alpha']>7 , 'weights'] +=1 

    
    df.loc[df['Beta']<0.5 , 'weights'] +=1 
    df.loc[df['Beta']<1 , 'weights'] +=1 
    df.loc[df['Beta']<1.5, 'weights']+=1 
    df.loc[df['Beta']<2 , 'weights'] +=1 
    df.loc[df['Beta']>2 , 'weights'] +=0 

def Market_Cap(df):
    df.loc[df['Market Cap.']>45000 , 'weights'] +=0
    df.loc[df['Market Cap.']>100000 , 'weights'] +=1 
    df.loc[df['Market Cap.']>300000 , 'weights'] +=1  
    df.loc[df['Market Cap.']>500000 , 'weights'] +=1 

def ROE(df):
    df.loc[df['ROE']>0 , 'weights'] +=0 
    df.loc[df['ROE']>12 , 'weights'] +=1
    df.loc[df['ROE']>15 , 'weights'] +=1 
    df.loc[df['ROE']>25 , 'weights'] +=1 

def NPM(df):
    df.loc[df['Net profit margin']>0 , 'weights'] +=0 
    df.loc[df['Net profit margin']>10 , 'weights'] +=1 
    df.loc[df['Net profit margin']>15 , 'weights'] +=1 
    df.loc[df['Net profit margin']>20 , 'weights'] +=1 


def Current(df):
    df.loc[df['Current ratio']>0 , 'weights'] +=0 
    df.loc[df['Current ratio']>0.5 , 'weights'] +=1 
    df.loc[df['Current ratio']>1 , 'weights'] +=1 
    df.loc[df['Current ratio']>1.5 , 'weights'] +=1 
    df.loc[df['Current ratio']>3 , 'weights'] +=1 

def PE(df):
    df.loc[(df['PE']-df['SectorPE'])>5 , 'weights'] +=0
    df.loc[(df['PE']-df['SectorPE'])<5 , 'weights'] +=0.25
    df.loc[(df['PE']-df['SectorPE'])<0 , 'weights'] +=0.50
    df.loc[(df['PE']-df['SectorPE'])<-5 , 'weights'] +=0.75
    df.loc[(df['PE']-df['SectorPE'])<-10 , 'weights'] +=1

def EBIDTA(df):
    df.loc[df['DiffEBIDTA']<0 , 'weights'] +=0
    df.loc[df['DiffEBIDTA']>0 , 'weights'] +=0.25
    df.loc[df['DiffEBIDTA']>1000 , 'weights'] +=0.5
    df.loc[df['DiffEBIDTA']>2000 , 'weights'] +=0.75
    df.loc[df['DiffEBIDTA']>3500 , 'weights'] +=1













