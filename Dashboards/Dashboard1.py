import pandas as pd
import plotly.express as px
from dash import html, dcc
import dash_bootstrap_components as dbc

consumables = pd.read_csv("DatasetLimpios/Consumables.csv")

def layout():
    total_consumables = len(consumables)
    ingrediente_mas_frecuente = consumables['ingredients'].str.split(", ").explode().value_counts().idxmax()
    subclase_mas_comun = consumables['subclass'].value_counts().idxmax()

    # Contar cuántos consumibles hay por subclase
    counts = consumables['subclass'].value_counts().reset_index()
    counts.columns = ['subclass', 'count']

    fig = px.bar(
        data_frame=counts,
        x='subclass',
        y='count',
        labels={'subclass': 'Subclase', 'count': 'Cantidad'},
        title='Cantidad de Consumibles por Subclase',
        text='count',
        color='subclass',
        color_discrete_sequence=[
            '#4da4e0',
            '#f0c949',
            '#2f4e3c',
            '#d14836',
            '#e6e6e6'
        ]
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        template='plotly_dark',
        font=dict(
            family="'Press Start 2P', cursive",
            size=11,
            color="#e6e6e6"
        ),
        title_font=dict(
            family="'Press Start 2P', cursive",
            size=20,
            color="#f0c949"
        ),
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e"
    )

    return html.Div([
        html.H2("Consumables (Elixires)", style={'textAlign': 'center'}),
        dbc.Row([
            dbc.Col(dbc.Card([
                dbc.CardHeader("Total de Consumibles"),
                dbc.CardBody(html.H3(total_consumables, className='card-title'))
            ], color="primary", inverse=True), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Ingrediente Más Frecuente"),
                dbc.CardBody(html.H4(ingrediente_mas_frecuente, className='card-text'))
            ], color="success", inverse=True), width=4),

            dbc.Col(dbc.Card([
                dbc.CardHeader("Subclase Más Común"),
                dbc.CardBody(html.H4(subclase_mas_comun, className='card-text'))
            ], color="info", inverse=True), width=4)
        ], className="mb-4"),

        dcc.Graph(figure=fig),
        html.Div([
            html.Img(
                src="https://cdn.wikimg.net/en/zeldawiki/images/0/0a/TotK_Bright_Elixir_Icon.png",
                style={
                    "width": "80px",
                    "display": "block",
                    "margin": "30px auto 10px auto"
                }
            ),
            html.P(
                "Un simple elixir puede marcar la diferencia entre la derrota y la victoria.",
                style={
                    "textAlign": "center",
                    "fontStyle": "italic",
                    "color": "#cccccc",
                    "fontSize": "16px",
                    "marginBottom": "40px"
                }
            )
        ])

    ], style={'padding': '20px'})

