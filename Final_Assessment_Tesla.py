#!/usr/bin/env python
# coding: utf-8

# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
                      height=900,
                      title=stock,
                      xaxis_rangeslider_visible=True)
    fig.show()


# In[4]:


Tesla = yf.Ticker('TSLA')
tesla_data = Tesla.history(period = "max")
tesla_data.reset_index(inplace = True)
tesla_data.head()


# In[5]:


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text


# In[6]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all("tbody")


# In[7]:


tesla_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])


# In[8]:


for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")


# In[11]:


tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)
tesla_revenue.dropna(inplace =True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] !=""]
tesla_revenue.tail(5)


# In[20]:


make_graph(tesla_data, tesla_revenue, 'Tesla')

