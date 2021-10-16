import dash_html_components as html
import dash_bootstrap_components as dbc


first_card = dbc.Container([
            dbc.Card(
            [
                dbc.CardImg(src="/assets/images/prediction3.jpg", top=True, className='image'),
                html.P(
                            "This page contains prediction about Customer's Term Deposit Supscription with XGBoost algorithm  ",
                            className="middle2",
                        ),
                dbc.Button("Let's Predict", color="info", href = '/apps/visualization', className='middle'),
                html.H4("Predict Customer's Term Deposit Supscription", className="card-title"),
                ]),
            ], className='containerhover mt-2')

second_card = dbc.Container([
            dbc.Card(
            [
                dbc.CardImg(src="/assets/images/dataset2.jpg", top=True, className='image'),
                html.P(
                            "This page contains original Bank Marketing Datasets by UCI Machine Learning Repository ",
                            className="middle2",
                        ),
                dbc.Button("Dataset", color="info", href = 'https://archive.ics.uci.edu/ml/datasets/Bank+Marketing', className='middle'),
                html.H4("Dataset by UCI Machine Learning Repository", className="card-title"),
                ]),
            ], className='containerhover mt-2')

third_card = dbc.Container([
            dbc.Card(
            [
                dbc.CardImg(src="/assets/images/profile.jpg", top=True, className='image'),
                html.P(
                            "This page contains author's Linkedin profile page",
                            className="middle2",
                        ),
                dbc.Button("Linkedin", color="info", href = 'https://linkedin.com/in/jofawj', className='middle'),
                html.H4("Author's Linkedin Profile Page", className="card-title"),
                ]),
            ], className='containerhover mt-2')

layout = html.Div([
    dbc.Container([
        dbc.Row([
        dbc.Col(
            html.H1("Welcome to My Predictions",
            className="text-center"),
            className="mt-3")
    ]),
        dbc.Row([
            dbc.Col(
                dbc.Row(
            [
                dbc.Col(first_card, width=4),
                dbc.Col(second_card, width=4),
                dbc.Col(third_card, width=4)
            ]
        )
            ),
        ]),
    ]),
])