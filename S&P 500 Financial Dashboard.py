#==============================================================================
# S&P 500 Financial Dashboard Script - Fajar Tri Anggoro
#==============================================================================

#==============================================================================
# Importing Packages
#==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import yahoo_fin.stock_info as si
import streamlit as st
import re
import mplfinance as mpf

#==============================================================================
# Tab 1 - Company Profile
#==============================================================================

def tab1():
    
    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Company profile')
    
    # Add table to show stock data
    @st.cache
    def GetCompanyInfo(ticker):
        return si.get_company_info(ticker)
    
    if ticker != '-':
        info = GetCompanyInfo(ticker)
        info['Value'] = info['Value'].astype(str)
        st.dataframe(info, height=1000)

#==============================================================================
# Tab 2 - Chart
#==============================================================================

def tab2():
    
    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Stock Price Chart')
    
    # Add table to show stock data
    @st.cache
    def GetStockData(tickers, start_date, end_date, interval = "1d"):
        return pd.concat([si.get_data(tick, start_date, end_date, interval = interval) for tick in tickers])

    # Define default variables
    if ticker != '-':
        col1, col2 = st.columns(2)    
        
        sd = col1.date_input("Start date", datetime.today().date() - timedelta(days=180), key = 1)
        ed = col2.date_input("End date", datetime.today().date(), key = 1)
        title_sum = ticker + ' adjusted close Price & Volume'
        
        interval_selection = col1.selectbox( 'Select Interval',
                             ('Daily', 'Weekly', 'Monthly'))
        
        plot_selection = col2.selectbox( 'Select Plot Type',
                             ('Line', 'Candle'))
        
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        
        if interval_selection == 'Weekly':
            selected_interval = "1wk"
        elif interval_selection == 'Monthly':
            selected_interval = "1mo"
        else:
            selected_interval = "1d"
            
        stock_price = GetStockData([ticker], sd, ed, selected_interval)
        
        
        # Time values will change accordingly
        
        if col1.button('1M'):
            sd = datetime.today().date() - timedelta(days=30)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 1 Month'
        

        if col2.button('3M'):
            sd = datetime.today().date() - timedelta(days=90)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 3 Months'
        

        
        if col3.button('6M'):
            sd = datetime.today().date() - timedelta(days=180)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 6 Months'
        

        if col4.button('YTD'):
            Y = datetime.today().date().year
            sd = datetime(Y, 1, 1)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Year to Date'
        
        
        if col5.button('1Y'):
            sd = datetime.today().date() - timedelta(days=365)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 1 Year'
            

        if col6.button('3Y'):
            sd = datetime.today().date() - timedelta(days=1095)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 3 Years'
        
            
        if col7.button('5Y'):
            sd = datetime.today().date() - timedelta(days=1825)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed, selected_interval)
            title_sum = ticker + ' adjusted close Price & Volume Last 5 Years'
          
            
        if col8.button('Max'):
            stock_price = GetStockData([ticker], start_date = None, end_date = None, interval = selected_interval)
            title_sum = 'All time ' + ticker + ' adjusted close Price & Volume'
            
        # Line plot
        if plot_selection == 'Line':
            fig, ax = plt.subplots(figsize=(15, 5))
            for tick in [ticker]:
                stock_df = stock_price[stock_price['ticker'] == tick]
                stock_df['SMA_50'] = stock_df['adjclose'].rolling(window=50).mean()
            
                if stock_df['adjclose'][-1] >= stock_df['open'][-1]:
                    col = 'green'
                else:
                    col = 'red'
                
                up = stock_df[stock_df['adjclose'] >= stock_df['open']]
                down = stock_df[stock_df['adjclose'] < stock_df['open']]
                ax.bar(up.index, up['volume'], color = 'green')
                ax.bar(down.index, down['volume'], color = 'red')
                ax.set(yticklabels=[])  
                ax.tick_params(left=False)
            
            
                ax2 = ax.twinx()
                ax2.plot(stock_df['adjclose'], label=tick, color = col)
                ax2.plot(stock_df['SMA_50'], label='SMA_50', color = 'blue')
                ax.set_ylim(stock_df['volume'].min(), stock_df['volume'].max()*1.75)
                ax2.set_ylim(stock_df['adjclose'].min()*0.8, stock_df['adjclose'].max()*1.01)
            ax2.set_ylabel("Adjusted Closing Price")
            ax2.legend()
            fig.suptitle(title_sum)
            st.pyplot(fig)
            
            
        # Candlestick plot    
        elif plot_selection == 'Candle':
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.write(title_sum)
            st.pyplot(mpf.plot(stock_price, type='candle', style='yahoo', volume = True, mav = 50))
        


#==============================================================================
# Tab 3 - Summary
#==============================================================================

def tab3():
    
    # Add dashboard title and description
    st.title("Welcome to S&P 500 Financial Dashboard")
    st.write("to begin, please select a ticker from the dropdown")
    
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")

    st.header('Summary - ' + ticker)
    
    # Add table to show stock data
    @st.cache
    def GetStockData(tickers, start_date = None, end_date = None):
        return pd.concat([si.get_data(tick, start_date, end_date) for tick in tickers])
    

    if ticker != '-':
        col1, col2 = st.columns(2)
        res = si.get_quote_table(ticker)
        df_summary = pd.DataFrame.from_dict(res, orient = 'index')
        df_summary.columns = ['Data']
        df_summary = df_summary.astype(str)
        df1 = df_summary.iloc[:9]
        df2 = df_summary.iloc[9:]
        col1.write(df1)
        col2.write(df2)
        
    # Add a line plot
    if ticker != '-':
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        
        # Define default variables
        
        sd = datetime.today().date() - timedelta(days=30)
        ed = datetime.today().date()
        stock_price = GetStockData([ticker], sd , ed)
        title_sum = ticker + ' adjusted close Price Last 1 Month'
        
        
        # Time variables will change accordingly
        if col1.button('1M'):
            sd = datetime.today().date() - timedelta(days=30)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 1 Month'
        
            
        if col2.button('3M'):
            sd = datetime.today().date() - timedelta(days=90)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 3 Months'
        
            
        if col3.button('6M'):
            sd = datetime.today().date() - timedelta(days=180)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 6 Months'
        
            
        if col4.button('YTD'):
            Y = datetime.today().date().year
            sd = datetime(Y, 1, 1)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Year to Date'
        
        
        if col5.button('1Y'):
            sd = datetime.today().date() - timedelta(days=365)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 1 year'
        
            
        if col6.button('3Y'):
            sd = datetime.today().date() - timedelta(days=1095)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 3 years'
        
        
        if col7.button('5Y'):
            sd = datetime.today().date() - timedelta(days=1825)
            ed = datetime.today().date()
            stock_price = GetStockData([ticker], sd, ed)
            title_sum = ticker + ' adjusted close Price Last 5 years'
        

        if col8.button('Max'):
            stock_price = GetStockData([ticker])
            title_sum = 'All time ' + ticker + ' adjusted close Price'
        
        if stock_price['adjclose'][-1] >= stock_price['open'][-1]:
            col = 'green'
        else:
            col = 'red'
        
        
        fig, ax = plt.subplots(figsize=(15, 5))
        for tick in [ticker]:
            stock_df = stock_price[stock_price['ticker'] == tick]
            ax.fill_between(stock_price.index, stock_price['adjclose'],color=col, alpha = 0.5)
            ax.plot(stock_df['adjclose'], label=tick, color = col)
        ax.legend()
        fig.suptitle(title_sum)
        st.pyplot(fig)
            
#==============================================================================
# Tab 4 - Statistics
#==============================================================================

def tab4():
    
    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Statistics - ' + ticker)
    
    if ticker != '-':
        col1, col2 = st.columns(2)
        stat = si.get_stats(ticker)
        stat_val = si.get_stats_valuation(ticker)
        
        # Index the Data Accordingly
        
        df_Stock_Price_History = stat.iloc[:7]
        df_Stock_Price_History = df_Stock_Price_History.set_index('Attribute')
        
        df_Share_Statistics = stat.iloc[7:19]
        df_Share_Statistics = df_Share_Statistics.set_index('Attribute')
        
        df_Dividends_Splits = stat.iloc[19:29]
        df_Dividends_Splits = df_Dividends_Splits.set_index('Attribute')
        
        df_Fiscal_Year = stat.iloc[29:31]
        df_Fiscal_Year = df_Fiscal_Year.set_index('Attribute')
        
        df_profitability = stat.iloc[31:33]
        df_profitability = df_profitability.set_index('Attribute')
        
        df_management_effectiveness = stat.iloc[33:35]
        df_management_effectiveness = df_management_effectiveness.set_index('Attribute')
        
        df_Income_Statement = stat.iloc[35:43]
        df_Income_Statement = df_Income_Statement.set_index('Attribute')

        df_Balance_Sheet = stat.iloc[43:49]
        df_Balance_Sheet = df_Balance_Sheet.set_index('Attribute')
        
        df_cashflow = stat.iloc[49:]
        df_cashflow = df_cashflow.set_index('Attribute')
        
        df_valuation = stat_val
        df_valuation.columns = ['Attribute', 'Value']
        df_valuation = df_valuation.set_index('Attribute')
        
        col1.write('Valuation Measures')
        col1.write(df_valuation)
        
        col1.subheader('Financial Highlights')
        col1.write('Fiscal Year')
        col1.write(df_Fiscal_Year)
        
        col1.write('Profitability')
        col1.write(df_profitability)
        
        col1.write('Management Effectiveness')
        col1.write(df_management_effectiveness)
        
        col1.write('Income Statement')
        col1.write(df_Income_Statement)
        
        col1.write('Balance Sheet')
        col1.write(df_Balance_Sheet)
        
        col1.write('Cash Flow Statement')
        col1.write(df_cashflow)
        
        col2.subheader('Trading Information')
        col2.write('Stock Price History')
        col2.write(df_Stock_Price_History)
        
        col2.write('Share Statistics')
        col2.write(df_Share_Statistics)
        
        col2.write('Dividends & Splits')
        col2.write(df_Dividends_Splits)
        
        
        # Add Footnotes
        col2.subheader('Footnotes')
        col2.write('1 : Data provided by Refinitiv.')
        col2.write('2 : Data provided by EDGAR Online.')
        col2.write('3 : Data derived from multiple sources or calculated by Yahoo Finance.')
        col2.write('4 : Data provided by Morningstar, Inc.')
        col2.write('5 : Shares outstanding is taken from the most recently filed quarterly or annual report and Market Cap is calculated using shares outstanding.')
        col2.write('6 : Implied Shares Outstanding of common equity, assuming the conversion of all convertible subsidiary equity into common.')
        col2.write('7 : EBITDA is calculated by S&P Global Market Intelligence using methodology that may differ from that used by a company in its reporting.')
        col2.write("8 :  A company's float is a measure of the number of shares available for trading by the public. It's calculated by taking the number of issued and outstanding shares minus any restricted stock, which may not be publicly traded.")

#==============================================================================
# Tab 5 - Financials
#==============================================================================

def tab5():

    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Financials - ' + ticker)

    
    if ticker != '-':
        option = st.selectbox( 'Select Data',
                             ('Income Statement', 'Balance Sheet', 'Cash Flow'))
        
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
        
        if option == 'Income Statement':
            
            T_select = st.radio("Select Timeframe",
                                ('Annually', 'Quarterly'), key = 1)
            
            if T_select == 'Annually':
                st.subheader('Income Statement - Annually')
                st.write("All numbers in thousands")
                inc_stat_y = si.get_income_statement(ticker, yearly = True)
                
                # Data Preprocessing, Filling NA
                inc_stat_y = inc_stat_y.reset_index()
                inc_stat_y['Breakdown'] = inc_stat_y['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                inc_stat_y['Breakdown'] = inc_stat_y['Breakdown'].apply(lambda row: ' '.join(row))
                inc_stat_y = inc_stat_y.set_index('Breakdown')
                inc_stat_y = inc_stat_y.fillna(0)
                inc_stat_y = inc_stat_y / 1000
                inc_stat_y = inc_stat_y.astype('int')
                
                # Processing Column Names
                for i in inc_stat_y.columns:
                    inc_stat_y.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(inc_stat_y.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")
                
            if T_select == 'Quarterly':
                st.subheader('Income Statement - Quarterly')
                st.write("All numbers in thousands")
                inc_stat_q = si.get_income_statement(ticker, yearly = False)
                
                # Data Preprocessing, Filling NA
                inc_stat_q = inc_stat_q.reset_index()
                inc_stat_q['Breakdown'] = inc_stat_q['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                inc_stat_q['Breakdown'] = inc_stat_q['Breakdown'].apply(lambda row: ' '.join(row))
                inc_stat_q = inc_stat_q.set_index('Breakdown')
                inc_stat_q = inc_stat_q.fillna(0)
                inc_stat_q = inc_stat_q / 1000
                inc_stat_q = inc_stat_q.astype('int')
                
                # Processing Column Names
                for i in inc_stat_q.columns:
                    inc_stat_q.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(inc_stat_q.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")             
        
        if option == 'Balance Sheet':
            
            T_select = st.radio("Select Timeframe",
                                ('Annually', 'Quarterly'), key = 2)
                
            if T_select == 'Annually':
                st.subheader('Balance Sheet - Annually')
                st.write("All numbers in thousands")
                bal_sheet_y = si.get_balance_sheet(ticker, yearly = True)
                
                # Data Preprocessing, Filling NA
                bal_sheet_y = bal_sheet_y.reset_index()
                bal_sheet_y['Breakdown'] = bal_sheet_y['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                bal_sheet_y['Breakdown'] = bal_sheet_y['Breakdown'].apply(lambda row: ' '.join(row))
                bal_sheet_y = bal_sheet_y.set_index('Breakdown')
                bal_sheet_y = bal_sheet_y.fillna(0)
                bal_sheet_y = bal_sheet_y / 1000
                bal_sheet_y = bal_sheet_y.astype('int')
                
                # Processing Column Names
                for i in bal_sheet_y.columns:
                    bal_sheet_y.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(bal_sheet_y.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")
                
            if T_select == 'Quarterly':
                st.subheader('Balance Sheet - Quarterly')
                st.write("All numbers in thousands")
                bal_sheet_q = si.get_balance_sheet(ticker, yearly = False)
                
                # Data Preprocessing, Filling NA
                bal_sheet_q = bal_sheet_q.reset_index()
                bal_sheet_q['Breakdown'] = bal_sheet_q['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                bal_sheet_q['Breakdown'] = bal_sheet_q['Breakdown'].apply(lambda row: ' '.join(row))
                bal_sheet_q = bal_sheet_q.set_index('Breakdown')
                bal_sheet_q = bal_sheet_q.fillna(0)
                bal_sheet_q = bal_sheet_q / 1000
                bal_sheet_q = bal_sheet_q.astype('int')
                
                # Processing Column Names
                for i in bal_sheet_q.columns:
                    bal_sheet_q.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(bal_sheet_q.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")
                
        if option == 'Cash Flow':
            
            T_select = st.radio("Select Timeframe",
                                ('Annually', 'Quarterly'), key = 3)
                
            if T_select == 'Annually':
                st.subheader('Cash Flow - Annually')
                st.write("All numbers in thousands")
                cash_flow_y = si.get_cash_flow(ticker, yearly = True)
                
                # Data Preprocessing, Filling NA
                cash_flow_y = cash_flow_y.reset_index()
                cash_flow_y['Breakdown'] = cash_flow_y['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                cash_flow_y['Breakdown'] = cash_flow_y['Breakdown'].apply(lambda row: ' '.join(row))
                cash_flow_y = cash_flow_y.set_index('Breakdown')
                cash_flow_y = cash_flow_y.fillna(0)
                cash_flow_y = cash_flow_y / 1000
                cash_flow_y = cash_flow_y.astype('int')
                
                # Processing Column Names
                for i in cash_flow_y.columns:
                    cash_flow_y.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(cash_flow_y.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")
                
            if T_select == 'Quarterly':
                st.subheader('Cash Flow - Quarterly')
                st.write("All numbers in thousands")
                cash_flow_q = si.get_cash_flow(ticker, yearly = False)
                
                # Data Preprocessing, Filling NA
                cash_flow_q = cash_flow_q.reset_index()
                cash_flow_q['Breakdown'] = cash_flow_q['Breakdown'].apply(lambda row: re.split(r'([A-Z][a-z]*\d*)', row))
                cash_flow_q['Breakdown'] = cash_flow_q['Breakdown'].apply(lambda row: ' '.join(row))
                cash_flow_q = cash_flow_q.set_index('Breakdown')
                cash_flow_q = cash_flow_q.fillna(0)
                cash_flow_q = cash_flow_q / 1000
                cash_flow_q = cash_flow_q.astype('int')
                
                # Processing Column Names
                for i in cash_flow_q.columns:
                    cash_flow_q.rename(columns={i: i.date()}, inplace=True)
                
                # Use proper Formatting
                st.dataframe(cash_flow_q.style.format("{:,d}"))
                st.subheader('Footnote:')
                st.write("0 means the data is currently Not Available")            
                

#==============================================================================
# Tab 6 - Analysis
#==============================================================================

def tab6():
    
    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Analysis - ' + ticker)
    
    if ticker != '-':
        st.write('Currency in USD')
        
        an = si.get_analysts_info(ticker)
        df_an = pd.DataFrame.from_dict(an, columns = ['Earnings Estimate'], orient = 'index')
        
        # Subset the data accordingly
        
        st.subheader('Earnings Estimate')
        Earnings_Estimate = df_an.iloc[0,0]
        Earnings_Estimate = Earnings_Estimate.set_index('Earnings Estimate')
        st.write(Earnings_Estimate)
        
        st.subheader('Revenue Estimate')
        Revenue_Estimate = df_an.iloc[1,0]
        Revenue_Estimate = Revenue_Estimate.set_index('Revenue Estimate')
        st.write(Revenue_Estimate)
        
        st.subheader('Earnings History')
        Earnings_History = df_an.iloc[2,0]
        Earnings_History = Earnings_History.set_index('Earnings History')
        st.write(Earnings_History)
        
        st.subheader('EPS Trend')
        EPS_Trend = df_an.iloc[3,0]
        EPS_Trend = EPS_Trend.set_index('EPS Trend')
        st.write(EPS_Trend)

        st.subheader('EPS Revisions')
        EPS_revisions = df_an.iloc[4,0]
        EPS_revisions = EPS_revisions.set_index('EPS Revisions')
        st.write(EPS_revisions)
        
        st.subheader('Growth Estimates')
        Growth_Estimates = df_an.iloc[5,0]
        Growth_Estimates = Growth_Estimates.set_index('Growth Estimates')
        st.write(Growth_Estimates)
        

#==============================================================================
# Tab 7 - Simulation
#==============================================================================

def tab7():
    
    # Add dashboard title and description
    st.title("S&P 500 Financial Dashboard")
    col1, col2 = st.columns(2)
    col1.write("Data source: Yahoo Finance")
    col2.write("Created by: Fajar Tri Anggoro")
    st.header('Monte Carlo Simulation - ' + ticker)
    col1, col2 = st.columns(2)
    
    @st.cache
    def GetStockData(tickers, start_date = None, end_date = None):
        return pd.concat([si.get_data(tick, start_date, end_date) for tick in tickers])
    
    if ticker != '-':
        sd = datetime.today().date() - timedelta(days=180)
        ed = datetime.today().date()
        stock_price = GetStockData([ticker], sd, ed)
        
        # Take the close price
        close_price = stock_price['close']
        
        # The returns ((today price - yesterday price) / yesterday price)
        daily_return = close_price.pct_change()
        
        # The volatility (high value, high risk)
        daily_volatility = np.std(daily_return)
        
        # Setup the Monte Carlo simulation
        #np.random.seed(123)
        simulations = col1.selectbox( 'Number of Simulations',
                                 (200, 500, 1000))
        time_horizon = col2.selectbox( 'Time Horizon',
                                 (30, 60, 90))
    
        # Run the simulation
        simulation_df = pd.DataFrame()
    
        for i in range(simulations):
        
            # The list to store the next stock price
            next_price = []
        
            # Create the next stock price
            last_price = close_price[-1]
        
            for j in range(time_horizon):
                # Generate the random percentage change around the mean (0) and std (daily_volatility)
                future_return = np.random.normal(0, daily_volatility)
    
                # Generate the random future price
                future_price = last_price * (1 + future_return)
    
                # Save the price and go next
                next_price.append(future_price)
                last_price = future_price
        
            # Store the result of the simulation
            simulation_df[i] = next_price
            
        # Get the ending price 
        ending_price = simulation_df.iloc[-1:, :].values[0, ]
        
        # Price at 95% confidence interval
        future_price_95ci = np.percentile(ending_price, 5)
        
        # Value at Risk
        VaR = close_price[-1] - future_price_95ci
        st.write('Value at Risk at 95% confidence interval is: ' + str(np.round(VaR, 2)) + ' USD')
        
        # Plot the simulation stock price in the future
        fig, ax = plt.subplots()
        fig.set_size_inches(15, 10, forward=True)
    
        plt.plot(simulation_df)
        plt.title('Monte Carlo simulation for ' + ticker + ' stock price in next ' + str(time_horizon) + ' days')
        plt.xlabel('Day')
        plt.ylabel('Price')
    
        plt.axhline(y=close_price[-1], color='red')
        plt.legend(['Current stock price is: ' + str(np.round(close_price[-1], 2))])
        ax.get_legend().legendHandles[0].set_color('red')
        st.pyplot(fig)
    
    
#==============================================================================
# Main body
#==============================================================================

def run():
    
    # Add the ticker selection on the sidebar
    # Get the list of stock tickers from S&P500
    ticker_list = ['-'] + si.tickers_sp500()
    
    # Add selection box
    global ticker
    ticker = st.sidebar.selectbox("Select a ticker", ticker_list)
    
    # Add function to convert df into csv
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    
    def GetStockData(tickers, start_date = None, end_date = None):
        return pd.concat([si.get_data(tick, start_date, end_date) for tick in tickers])
    
    
    if ticker != '-':
        
        col1, col2 = st.sidebar.columns(2)
        
        csv = convert_df(GetStockData(ticker))
    
        col1.download_button(
            label="Download Stock Data as CSV",
            data=csv,
            file_name= ticker + '_data.csv',
            mime='text/csv')
        
        if col2.button('Refresh Data'):
            st.experimental_rerun()
    
    # Add a radio box
    select_tab = st.sidebar.radio("Select Page", ['Summary', 'Chart', 'Statistics', 'Financials', 'Analysis', 'Simulation', 'Company Profile'])
    
    # Show the selected tab
    if select_tab == 'Summary':
        # Run tab 3
        tab3()
    elif select_tab == 'Chart':
        # Run tab 2
        tab2()
    elif select_tab == 'Statistics':
        # Run tab 4
        tab4()
    elif select_tab == 'Financials':
        # Run tab 5
        tab5()
    elif select_tab == 'Analysis':
        # Run tab 6
        tab6()
    elif select_tab == 'Simulation':
        # Run tab 7
        tab7()
    elif select_tab == 'Company Profile':
        # Run tab 1
        tab1()
        
if __name__ == "__main__":
    run()
    
###############################################################################
# END
###############################################################################
