#import library
import dash_core_components as dcc
from dash_core_components.Graph import Graph
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_html_components.Br import Br
from dash_html_components.Hr import Hr
from dash_html_components.P import P

import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats
from datetime import date

from app import app 

#load data
df = pd.read_csv("supermarket_sales.csv")

#Convert date column into date type 
df['Date'] = pd.to_datetime(df['Date'])
df['Time'] = pd.to_datetime(df['Time'], format="%H:%M").dt.time
df_HT = df.groupby(['Gender', 'Product line']).count()['Total'].reset_index()
df_status=df_HT.pivot(index="Gender",columns="Product line", values="Total").fillna(0)


####################################################
#define data
var_1 = df[df['Gender'] == 'Male']['Total']
var_2 = df[df['Gender'] == 'Female']['Total']


#calculate independent t-test and p-value
t,p = stats.ttest_ind(var_2, var_1, equal_var=True)

####################################################

#define table statistic
table_header = [
    html.Thead(html.Tr([html.Th("Variable"), html.Th("Value")]))
]

row5 = html.Tr([html.Td("T-Statistic"), html.Td(t)])
row6 = html.Tr([html.Td("P-Value"), html.Td(p)])

table_body = [html.Tbody([row5, row6])]
table = dbc.Table(table_header + table_body, bordered=True)

#Layout and Graph
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1("SUPERMARKET SALES HYPOTHESIS TESTING",
                className="text-center"),
                className="mb-5 mt-5")
            ]),
        dbc.Row([
            dbc.Col(width = 1),
            dbc.Col([
                html.P(children=["Hypothesis testing is an act in statistics whereby an analyst tests an assumption regarding a population parameter. "
                        "The methodology employed by the analyst depends on the nature of the data used and the reason for the analysis. "
                        "In this case study, we use average purchase from Male customer type and Female customer type of SuperMarket Sales Datasets."], className="text-center"),
                html.Hr(),
                html.H4("Hypothesis :"),
                html.Br(),
                html.P("H0 : Sales Mean of Male Customer = Sales Mean of Female Customer ",  className="text-center"),
                html.P("H1 : Sales Mean of Male Customer ≠ Sales Mean of Female Customer ", className="text-center")],
                width=10
            ),
            dbc.Col(width=1)
        ],className="mb-5"),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col([
                html.H4("Hypothesis Testing Type :"),
                html.Br(),
                html.P("Hypothesis Test : Two Tailed Test"),
                html.Br(),
                html.P("Sample Data : Sample Data of Super Market Sales from 1 January 2019  until 30 March 2019."),
                html.Br(),
                html.P("Significance Value : 5% / 0.05.")
            ],width=10),
            dbc.Col(width=1)
        ],className="mb-5"),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col([
                html.H4("Two Tailed Test Calculation Result :"),
                dbc.Table(table_header + table_body, bordered=True,
                hover=True,responsive=True,striped=True)
            ],width=10),
            dbc.Col(width=10)
        ],className="mb-5"),
        dbc.Row([
            dbc.Col(width=1),
            dbc.Col([
                html.H4("Analysis Result :"),
                html.P("From calculation above, we could see that our P-Value has 0.11 score which "
                        "is greater than our defined significance value. It means, "
                        "we accept our defined H0 Hypothesis which is Sales Mean of Male Customer = Sales Mean of Female Customer.")
            ],width=10),
            dbc.Col(width=1)
        ],className="mb-5")

    ])
])