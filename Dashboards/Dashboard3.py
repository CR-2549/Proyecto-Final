import pandas as pd
from dash import dcc, html, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc

# Cargar datos
df = pd.read_csv("DatasetLimpios//Materials.csv")
df['id'] = df.index  # ID único por fila

# Opciones para el filtro
subclass_options = [{'label': s, 'value': s} for s in sorted(df['subclass'].dropna().unique())]

# Layout
def layout():
    return html.Div([
        html.Div([
            html.H2("Explorador de Materiales", style={
                "color": "#f2d13f",
                "textAlign": "center",
                "display": "inline-block",
                "marginRight": "15px"
            }),
            html.Img(
                src="https://assets.nintendo.eu/image/upload/f_auto,c_limit,w_992,q_auto:low/MNS/NOE/70010000000023/SQ_NSwitch_TheLegendOfZeldaBreathOfTheWild_E",
                style={
                    "width": "90px",
                    "verticalAlign": "middle"
                }
            )
        ], style={"textAlign": "center", "marginBottom": "30px"}),

        # Buscador y Filtro
        dbc.Row([
            dbc.Col(dcc.Input(
                id='material-search', type='text', placeholder='Buscar por nombre...',
                debounce=True, className='form-control'
            ), md=6),
            dbc.Col(dcc.Dropdown(
                id='subclass-filter',
                options=subclass_options,
                placeholder='Filtrar por subclass',
                className='text-dark'
            ), md=6)
        ], className='mb-4', justify="center"),

        # Tabla visual
        html.Div([
            dbc.Row([
                dbc.Col(html.Div("ITEM NAME", style={
                    "fontWeight": "bold",
                    "border": "2px solid #f2d13f",
                    "padding": "8px",
                    "backgroundColor": "#2f2f2f",
                    "color": "#f2d13f",
                    "fontFamily": "'Press Start 2P', cursive",
                    "fontSize": "12px",
                    "textAlign": "center"
                }), width=9),
                dbc.Col(html.Div("VIEW DESCRIPTION", style={
                    "fontWeight": "bold",
                    "border": "2px solid #f2d13f",
                    "padding": "8px",
                    "backgroundColor": "#2f2f2f",
                    "color": "#f2d13f",
                    "fontFamily": "'Press Start 2P', cursive",
                    "fontSize": "12px",
                    "textAlign": "center"
                }), width=3),
            ], style={"margin": "0"}),

            html.Div(id='material-list')
        ], style={"width": "70%", "margin": "auto"}),

        dbc.Offcanvas(
            id="material-description",
            title="Descripción del Material",
            is_open=False,
            placement="end",
            style={"backgroundColor": "#1b3a2d", "color": "white"},
        )
    ], style={"padding": "20px"})

# Callbacks
def register_callbacks(app):
    @app.callback(
        Output("material-list", "children"),
        Input("material-search", "value"),
        Input("subclass-filter", "value")
    )
    def update_list(search, subclass):
        filtered = df.copy()
        if search:
            filtered = filtered[filtered['name'].str.contains(search, case=False, na=False)]
        if subclass:
            filtered = filtered[filtered['subclass'] == subclass]

        if filtered.empty:
            return [html.P("No se encontraron materiales.", style={"color": "gray", "padding": "10px"})]

        items = []
        for _, row in filtered.iterrows():
            items.append(
                dbc.Row([
                    dbc.Col(html.Div(row['name'], style={
                        "border": "1px solid #ccc",
                        "padding": "8px",
                        "color": "white",
                        "fontFamily": "'Press Start 2P', cursive",
                        "fontSize": "11px"
                    }), width=9),
                    dbc.Col(html.Div(
                        dbc.Button("Ver", id={'type': 'view-button', 'index': row['id']}, size="sm", color="warning"),
                        style={"border": "1px solid #ccc", "padding": "4px", "textAlign": "center"}
                    ), width=3)
                ], style={"margin": "0"})
            )
        return items

    @app.callback(
        Output("material-description", "is_open"),
        Output("material-description", "title"),
        Output("material-description", "children"),
        Input({'type': 'view-button', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def show_description(n_clicks_list):
        triggered = ctx.triggered_id
        if triggered and 'index' in triggered:
            idx = triggered['index']
            row = df.loc[df['id'] == idx].iloc[0]
            return True, row['name'], html.P(row['description'])
        return False, "", ""
