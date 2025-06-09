import sys
import importlib.util
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Función para importar módulos desde archivos arbitrarios
def import_dashboard(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

# Importamos los dashboards desde archivos
consumables = import_dashboard("Dashboards/Dashboard1.py", "consumables")
equipament = import_dashboard("Dashboards/Dashboard2.py", "equipament")
materials = import_dashboard("Dashboards/Dashboard3.py", "materials")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "240px",
    "padding": "20px",
    "background-color": "#264d3b",
    "color": "white",
    "borderRight": "2px solid #264d3b"
}



CONTENT_STYLE = {
    "margin-left": "260px",
    "margin-right": "20px",
    "padding": "20px",
    "background-color": "#1e1e1e",
    "min-height": "100vh"
}



sidebar = html.Div([
    html.H2("Zelda Dashboards", style={"textAlign": "center", "color": "#f2d13f"}),
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Inicio", href="/inicio", id="page-home-link", active="exact"),
            dbc.NavLink("Consumables", href="/consumables", id="page-1-link", active="exact"),
            dbc.NavLink("Equipament", href="/equipament", id="page-2-link", active="exact"),
            dbc.NavLink("Materials", href="/materials", id="page-3-link", active="exact"),
        ],
        vertical=True,
        pills=True,
    ),
], style=SIDEBAR_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id="page-content", style=CONTENT_STYLE)
], style={"fontFamily": "'Press Start 2P', cursive"})


@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/" or pathname == "/inicio":
        return html.Div([
            html.H1("Bienvenido a los Dashboards de Zelda", style={
                "color": "#f0c949",
                "textAlign": "center",
                "fontSize": "40px",
                "marginBottom": "30px"
            }),
            html.Img(
                src="https://www.playerreset.com/wp-content/uploads/2016/06/tumblr_o8rt8k99sd1qzp9weo5_1280.gif",
                style={
                    "display": "block",
                    "margin": "0 auto 30px auto",
                    "width": "320px",
                    "borderRadius": "10px",
                    "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.5)"
                }
            ),

            html.Hr(),

            html.P(
                "Cada gráfico cuenta una historia, cada dato es un artefacto. Estos dashboards son nuestra propia aventura en el mundo de la programación y Zelda.",
                style={"fontSize": "18px", "textAlign": "justify", "marginBottom": "20px"}),

            html.Div([
                html.Hr(),

                html.H4("Enlaces útiles :D", style={"color": "#f2d13f", "textAlign": "center", "marginBottom": "20px"}),

                html.Ul([
                    html.Li(
                        html.A("Conoce el Universo de Zelda",
                               href="https://www.zelda.com/",
                               target="_blank",
                               style={"color": "#4da4e0", "textDecoration": "none", "fontWeight": "bold"})
                    ),
                    html.Li(
                        html.A("Accede al Reporte de nuestro Proyecto",
                               href="https://www.canva.com/design/DAGpu06v9is/wJbdlRRFWQ8DvOCpDiChfQ/edit?utm_content=DAGpu06v9is&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton",
                               target="_blank",
                               style={"color": "#4da4e0", "textDecoration": "none", "fontWeight": "bold"})
                    )
                ], style={"listStyle": "none", "textAlign": "center", "padding": 0})
            ]),


            html.Hr(),

            html.P([
                "Puedes ver los distintos elementos del juego como ",
                html.Span("consumibles", style={"color": "lightgreen", "fontWeight": "bold"}),
                ", ",
                html.Span("equipamiento", style={"color": "skyblue", "fontWeight": "bold"}),
                " y ",
                html.Span("materiales", style={"color": "lightcoral", "fontWeight": "bold"}),
                " usando el menú de la izquierda."
            ], style={"fontSize": "17px", "textAlign": "justify"}),

            html.Div("¡Que la Trifuerza te acompañe!",
                     style={"marginTop": "40px", "textAlign": "center", "fontStyle": "italic"})
        ])
    elif pathname == "/consumables":
        return consumables.layout()
    elif pathname == "/equipament":
        return equipament.layout()
    elif pathname == "/materials":
        return materials.layout()

    return dbc.Jumbotron([
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"La ruta {pathname} no existe.")
    ])


# Registrar callbacks
materials.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
