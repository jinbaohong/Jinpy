# coding: utf-8
import pandas as pd
import numpy as np

def bcf(year, buyer):
    freqTable = buyer['國別'][buyer['展覽年度']==year].value_counts()
    freqTable = pd.DataFrame({ 'country' : list(freqTable.index),
                   'Freq' : list(freqTable)})
    return freqTable

if __name__ == '__main__':
    buyer = pd.read_csv("~/EH2/srv/buyer0407.csv")
    buyer = buyer.drop(['序號','TTS代碼','經度','緯度'], axis=1)
    print(' bcf(2017, buyer) : \n', bcf(2017, buyer))
    print(' bcf(2011, buyer) : \n', bcf(2011, buyer))

