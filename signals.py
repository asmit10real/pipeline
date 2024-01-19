import pandas as pd
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL) #Debug or Critical are used

#We calculate and return number of positions in this function because it
#saves time having to loop elsewhere in the code.
#Calculate the signal based on the various conditions below
#Current implementation is to buy when the trend makes a new low and sell when it makes a new high
def signal(data: pd.DataFrame, strategy = 1):
    if(strategy == 1):
        logger.warning('Attempting to calc signal. Set data = data.copy()')
        data = data.copy()
        signal = np.zeros(len(data['Close']))
        last_sig = 0
        curr_sig = 0
        numpos = 0
        logger.warning('Attempting to calculate signal for each step in timeseries')
        for i in range(len(data['Close'])):
            #If the signal is active and the resistance slope has yet to make new highs in the 
            #rolling window, stay long
            if(last_sig == 1):
                if(data['resist_slope'][i] < data['slopehighr'][i]):
                    signal[i] = 1
                    curr_sig = 1
                    last_sig = 1
                #If signal was triggered last time and we continue to trend down, assume we were
                #wrong and exit the position
                if(data['resist_slope'][i] < data['slopelowr'][i]):
                    signal[i] = 0
                    curr_sig = 0
                    last_sig = 0
            #Once the resistance slope trends higher than (window) highs, exit position
            if(data['resist_slope'][i] > data['slopehighr'][i]):
                signal[i] = 0
                curr_sig = 0
                last_sig = 0

            #If resist slope is making new lows in the window, activate signal and go long
            if(data['resist_slope'][i] < data['slopelowr'][i]):
                signal[i] = 1
                curr_sig = 1
                last_sig = 1
                numpos += 1
    elif(strategy == 2):
        logger.warning('Attempting to calc signal. Set data = data.copy()')
        data = data.copy()
        signal = np.zeros(len(data['Close']))
        last_sig = 0
        curr_sig = 0
        numpos = 0
        logger.warning('Attempting to calculate signal for each step in timeseries')
        for i in range(len(data['Close'])):
            #If the signal is active and the resistance slope has yet to make new lows in the 
            #rolling window, stay long
            x = ((data['resist_slope'][i] + data['support_slope'][i]) / 2)
            y = data['slopeqnt'][i]
            if(x > 0):
                signal[i] = 1
                curr_sig = 1
                if(curr_sig != last_sig):
                    numpos += 1
                last_sig = 1
            #Get quantile average
            #qnt = data['resist_slope']
            #Once the resistance slope trends higher than (window) highs, enter position
            if(x < y):
                signal[i] = 0
                curr_sig = 0
                last_sig = 0
            if(x == 0):
                signal[i] = last_sig
    elif(strategy == 3):
        logger.warning('Attempting to calc signal. Set data = data.copy()')
        data = data.copy()
        signal = np.zeros(len(data['Close']))
        last_sig = 0
        curr_sig = 0
        numpos = 0
        logger.warning('Attempting to calculate signal for each step in timeseries')
        for i in range(len(data['Close'])):
            #If the signal is active and the resistance slope has yet to make new lows in the 
            #rolling window, stay long
            x = ((data['resist_slope'][i] + data['support_slope'][i]) / 2)
            if(data['Close'][i] > data['AVWAP'][i] and x > 0):
                signal[i] = 1
                curr_sig = 1
                if(last_sig == 0):
                    numpos += 1
                last_sig = 1
            else:
                signal[i] = 0
                curr_sig = 0
                last_sig = 0
    #logger.warning('Returning signal')
    #logger.critical(f'NUM POSITIONS: {debug}')
    return signal, numpos