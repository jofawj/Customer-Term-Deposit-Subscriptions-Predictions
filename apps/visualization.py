import plotly.express as px
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc
from datetime import datetime
from datetime import date
from sklearn.preprocessing import StandardScaler
import joblib
from app import app #change this line

#SkLearn

# Data Preprocessing
df = pd.read_csv('bank-additional-full.csv', delimiter=";")

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(
                html.H1("Customer's Form",
                className="text-center"),
                className="mt-5")
        ]),
        dbc.Alert(
            "The Consumer will not subscribe the term deposit.",
            id="alert-fade",
            dismissable=True,
            is_open=False,
        ),
        dbc.Alert(
            "The Consumer will subscribe the term deposit.",
            id="alert-fade2",
            dismissable=True,
            is_open=False,
        ),
        dbc.Row([
            dbc.Col(
                html.H3(children="Personal Information",                        #PERSONAL ROW
                className="text-left"),
                className="mb-3 mt-4"),
        ]),
        dbc.Row([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("Age", addon_type="prepend", style={"background-color":"#000000"}),
                dbc.Input(id="input-age", placeholder="17-98", type="number", min=df['age'].min(), max=df['age'].max(), step=1),
                dbc.InputGroupAddon("Job", addon_type="prepend"),
                dbc.Select(id="input-job",
                    options=[
                        {"label": "Admin", "value": "0"},
                        {"label": "Blue-Collar", "value": "1"},
                        {"label": "Technician", "value": "9"},
                        {"label": "Services", "value": "7"},
                        {"label": "Management", "value": "4"},
                        {"label": "Retired", "value": "5"},
                        {"label": "Entrepreneur", "value": "2"},
                        {"label": "Self-Employed", "value": "6"},
                        {"label": "Housemaid", "value": "3"},
                        {"label": "Unemployed", "value": "10"},
                        {"label": "Student", "value": "student"}
                    ], placeholder="Choose Job"
                ),
            ],
            className="mb-3 ml-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Education", addon_type="prepend"),
                dbc.Select(id="input-education",
                    options=[
                        {"label": "University Degree", "value": "6"},
                        {"label": "Professional Course", "value": "5"},
                        {"label": "High School", "value": "high.3"},
                        {"label": "Basic 9 Years", "value": "2"},
                        {"label": "Basic 6 Years", "value": "1"},
                        {"label": "Basic 4 Years", "value": "0"},
                        {"label": "Illiterate", "value": "4"}
                    ], placeholder="Choose Last Education"
                ),
                dbc.InputGroupAddon("Marital", addon_type="prepend"),
                dbc.Select(id="input-marital",
                    options=[
                        {"label": "Married", "value": "1"},
                        {"label": "Divorced", "value": "0"},
                        {"label": "Single", "value": "2"}
                    ], placeholder="Choose Marital Status"
                ),

            ],
            className="mb-3 ml-3"
        )
        ]),
        dbc.Row([
            dbc.Col(
                html.H3(children="Financial Data",                               #FINANCIAL ROW
                className="text-left"),
                className="mb-3 mt-4")
        ]),
        dbc.Row([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("Default", addon_type="prepend"),
                dbc.Select(id="input-default",
                    options=[
                        {"label": "No", "value": "0"},
                        {"label": "Yes", "value": "1"}
                    ], placeholder="Has Credit in Default ?"
                ),

            ],
            className="mb-3 ml-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Housing", addon_type="prepend"),
                dbc.Select(
                    id="input-housing",
                    options=[
                        {"label": "No", "value": "0"},
                        {"label": "Yes", "value": "1"}
                    ], placeholder="Has Housing Loan ?"
                ),
                dbc.InputGroupAddon("Loan", addon_type="prepend"),
                dbc.Select(id="input-loan",
                    options=[
                        {"label": "No", "value": "0"},
                        {"label": "Yes", "value": "1"}
                    ], placeholder="Has Personal Loan ?"
                ),

            ],
            className="mb-3 ml-3"
        )
        ]),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H3(children="Campaign History",                               #Campaign ROW
                className="text-left"),
                className="mb-3 mt-4")
        ]),
        dbc.Row([
            dbc.Label("Communication Type :", className="text-left ml-3"),
            dbc.RadioItems(id="input-commtype",
                options=[
                    {"label": "Cellular", "value": '0'},
                    {"label": "Telephone", "value": '1'}
                ],
                inline=True,
                style={"margin-left":"25px", "margin-bottom":"30px",'border-color': '#000000'},
            )
        ]),
        dbc.Row([
            html.H5(children="Last Contacted ", className="text-left ml-3 mb-3")
        ]
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Day", addon_type="prepend"),
                dbc.Select(id="input-lastcon",
                    options=[
                        {"label": "Monday", "value": "1"},
                        {"label": "Tuesday", "value": "3"},
                        {"label": "Wednesday", "value": "4"},
                        {"label": "Thursday", "value": "2"},
                        {"label": "Friday", "value": "0"},
                    ], placeholder="Choose Day of Week"
                ),
                dbc.InputGroupAddon("Month", addon_type="prepend"),
                dbc.Select(id="input-month",
                    options=[
                        {"label": "January", "value": "10"},
                        {"label": "February", "value": "11"},
                        {"label": "March", "value": "5"},
                        {"label": "April", "value": "0"},
                        {"label": "May", "value": "6"},
                        {"label": "June", "value": "4"},
                        {"label": "July", "value": "3"},
                        {"label": "August", "value": "1"},
                        {"label": "September", "value": "9"},
                        {"label": "October", "value": "8"},
                        {"label": "November", "value": "7"},
                        {"label": "Desember", "value": "2"},
                    ], placeholder="Choose Month"
                ),
                dbc.InputGroupAddon("Duration (secs)", addon_type="prepend"),
                dbc.Input(id="input-duration",placeholder="Contact Duration", type="number", min=0,  step=1),
            ],
            className="mb-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("#", addon_type="prepend"),
                dbc.Input(id="input-ncon",placeholder="Number of contacts performed during this campaign and for this client", type="number", min=0,  step=1),
                dbc.InputGroupAddon("contacts", addon_type="append"),
            ],
            className="mb-3"
        ),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.H3(children="Additional Information",                               #Additional ROW
                className="text-left"),
                className="mb-3 mt-4")
        ]),
        dbc.Row([
            dbc.InputGroup(
            [
                dbc.InputGroupAddon("Previous Outcome Campaign", addon_type="prepend"),
                dbc.Select(id="input-poutcome",
                    options=[
                        {"label": "Failure", "value": "0"},
                        {"label": "Non-Existent", "value": "1"},
                        {"label": "Success", "value": "2"},
                    ], placeholder="Outcome of the previous marketing campaign"
                ),

            ],
            className="mb-3 ml-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("#", addon_type="prepend"),
                dbc.Input(id="input-numcon",placeholder="Number of contacts performed before this campaign and for this client", type="number", min=0,  step=1),
                dbc.InputGroupAddon("contacts", addon_type="append"),
            ],
            className="mb-3 ml-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("#", addon_type="prepend"),
                dbc.Input(id="input-numdays",placeholder="Number of days that passed by after the client was last contacted from a previous campaign", type="number", min=0,  step=1),
                dbc.InputGroupAddon("days", addon_type="append"),
            ],
            className="mb-3 ml-3"
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Employment Variation Rate", addon_type="prepend"),
                dbc.Input(id="input-evr",placeholder="Employment variation rate ", type="number", min=0,  step=0.00001),
                dbc.InputGroupAddon("Quarterly Indicator", addon_type="append"),
            ],
            className="mb-3 ml-3"
        ),
        ]),

    html.Button('Submit', id='submit-val',formMethod='POST', className='button button2', n_clicks=0, style={'background-color': '#2002DE',
    'border': 'none',
    'color': 'white',
    'font-family': 'Lato',
    'padding': '10px 15px',
    'text-align': 'center',
    'text-decoration': 'none',
    'display': 'inline-block',
    'font-size': '16px',
    'border-radius': '8px',
    'margin-bottom':'5px',
    'width':'150px',
    'align':'center'},
    ),

    html.Footer(html.P(children="Copyright Jofa WJ 2021", className="text-center", style={'color':'white'}),
        style={"position": "absolute",
        "left": 0,
        "right": 0,
        "padding": "1rem 1rem",
        "background-color": "black",
        'margin-top':'10px',
        'height':'50px'}
        )
]),
], style={'display': 'flex', 'justify-content': 'center'})

@app.callback(
    Output("alert-fade", "is_open"),
    [Input("submit-val", "n_clicks")],
    [Input("input-age", "value")],
    [Input("input-job", "value")],
    [Input("input-education", "value")],
    [Input("input-marital", "value")],
    [Input("input-default", "value")],
    [Input("input-housing", "value")],
    [Input("input-loan", "value")],
    [Input("input-commtype", "value")],
    [Input("input-lastcon", "value")],
    [Input("input-month", "value")],
    [Input("input-duration", "value")],
    [Input("input-ncon", "value")],
    [Input("input-poutcome", "value")],
    [Input("input-numcon", "value")],
    [Input("input-numdays", "value")],
    [Input("input-evr", "value")],
    [State("alert-fade", "is_open")],
    [State("alert-fade2", "is_open")],
)
def toggle_alert(n, age, job, education, marital, default, housing, loan, commtype, lastcon, month, duration, ncon, poutcome, numcon, numdays, evr, is_open, is_open2):
    d = {'age': [age], 'job': [job], 'education': [education], 'marital': [marital], 'default': [default], 'housing': [housing], 'loan': [loan], 'commtype': [commtype], 'lastcon': [lastcon], 'month': [month], 'duration': [duration], 'ncon': [ncon], 'poutcome': [poutcome], 'numcon': [numcon], 'numdays': [numdays], 'evr': [evr]}
    list_mod = np.array([age, job, education, marital, default, housing, loan, commtype, lastcon, month, duration, ncon, poutcome, numcon, numdays, evr])
    if __name__ == '__main__':
        model = joblib.load('xgb_model_fix.pkl')

    new_df = pd.DataFrame(
        data=d
    )
    if (new_df.any() == False):
        try:
            model = joblib.load('xgb_model_fix.pkl')
            X_sample = new_df.values
            scaler = StandardScaler()
            X_sample = scaler.fit_transform(X_sample)
            y_pred = model.predict(X_sample)[0]
            if y_pred:
                return is_open2
            return is_open
        except ValueError:
            return 'Unable to give years of experience'
    
    #Proses Scaling dari data