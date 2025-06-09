import pandas as pd
import plotly.express as px
from dash import html, dcc

equipament = pd.read_csv("DatasetLimpios/Equipament.csv")

def layout():
    counts = equipament['class'].value_counts().reset_index()
    counts.columns = ['class', 'count']

    fig = px.pie(
        counts,
        values='count',
        names='class',
        title='Distribución de Equipamiento por Clase',
        color_discrete_sequence=[
            '#4da4e0',
            '#d14836',
            '#00b894',
            '#a29bfe'
        ]
    )

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
        html.H2("Equipament", style={
            'textAlign': 'center',
            'color': '#white',
            'textShadow': '1px 1px 2px black'
        }),

        dcc.Graph(figure=fig),

        html.Div([
            html.Img(
                src="https://www.gamertw.com/totk/armor-set/Phantom.png",
                style={
                    "width": "80px",
                    "display": "block",
                    "margin": "30px auto 10px auto"
                }
            ),
            html.P(
                "Cada pieza de equipo es más que defensa... es preparación. Cada gráfico también.",
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
