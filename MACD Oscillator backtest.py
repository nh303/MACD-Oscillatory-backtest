
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf



def macd(signals):
    
    
    signals['ma1']=signals['Close'].rolling(window=ma1,min_periods=1,center=False).mean()
    signals['ma2']=signals['Close'].rolling(window=ma2,min_periods=1,center=False).mean()
    
    return signals


def signal_generation(df,method):
    
    signals=method(df)
    signals['positions']=0

    
    signals['positions'][ma1:]=np.where(signals['ma1'][ma1:]>=signals['ma2'][ma1:],1,0)

   
    signals['signals']=signals['positions'].diff()

    
    signals['oscillator']=signals['ma1']-signals['ma2']

    return signals



def plot(new, ticker):
    
    
    fig=plt.figure()
    ax=fig.add_subplot(111)
    
    new['Close'].plot(label=ticker)
    ax.plot(new.loc[new['signals']==1].index,new['Close'][new['signals']==1],label='LONG',lw=0,marker='^',c='g')
    ax.plot(new.loc[new['signals']==-1].index,new['Close'][new['signals']==-1],label='SHORT',lw=0,marker='v',c='r')

    plt.legend(loc='best')
    plt.grid(True)
    plt.title('Positions')
    
    plt.show()
    
    
    fig=plt.figure()
    cx=fig.add_subplot(211)

    new['oscillator'].plot(kind='bar',color='r')

    plt.legend(loc='best')
    plt.grid(True)
    plt.xticks([])
    plt.xlabel('')
    plt.title('MACD Oscillator')

    bx=fig.add_subplot(212)

    new['ma1'].plot(label='ma1')
    new['ma2'].plot(label='ma2',linestyle=':')
    
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()

    


def main():
    
    
    
    global ma1,ma2,stdate,eddate,ticker,slicer

    
    ma1=int(input('ma1:'))
    ma2=int(input('ma2:'))
    stdate=input('start date in format yyyy-mm-dd:')
    eddate=input('end date in format yyyy-mm-dd:')
    ticker=input('ticker:')

    
    slicer=int(input('slicing:'))

   
    df=yf.download(ticker,start=stdate,end=eddate)
    
    new=signal_generation(df,macd)
    new=new[slicer:]
    plot(new, ticker)





if __name__ == '__main__':
    main()
