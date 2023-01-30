from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

DATASET_PATH = "assets/kc_house_data.csv"

# Carregadar o dataset
# (1) carregar o dataset
df = pd.read_csv(DATASET_PATH)
data_mapa = df[["id", "lat", "long", "price", "bedrooms"]]

# (2) Operações necessárias

list_bed = df.bedrooms.unique()
list_bed.sort()

app = Dash(__name__)

# Definir o layout do dashboard aqui!!!!

app.layout = html.Div(
    [
        html.H1(
            "CORRETORA KINGS!",
            style={"textAlign": "center"},
        ),
        html.Div(
            [
                "Preço",
                # Primeiro Slider, Price
                dcc.RangeSlider(
                    df["price"].min(),
                    df["price"].max(),
                    value=[df["price"].min(), df["price"].max()],
                    id="price_range",
                ),
            ]
        ),
        html.Div(
            ["Quartos", dcc.Dropdown(options=list_bed, value=list_bed[0], id="quartos")]
        ),
        html.H2("Casas a venda"),
        dcc.Graph(id="figura1"),
    ]
)

# definir a callback
@app.callback(
    Output("figura1", "figure"),
    Input("price_range", "value"),
    Input("quartos", "value"),
)

def update_graph(price_r, quartos):
    print(
        f"o minimo é {price_r[0]} e o maximo {price_r[1]} e o numero de quartos {quartos}"
    )
    fig1 = px.scatter_mapbox(
        data_mapa[(data_mapa.price>=price_r[0]) & (data_mapa.price<price_r[1]) & (data_mapa.bedrooms == quartos)],
        lat="lat",
        lon="long",
        hover_name="id",
        hover_data=["price", "bedrooms"],
        color_discrete_sequence=["fuchsia"],
        zoom=8,
        height=500,
        mapbox_style="open-street-map",
    )
    return fig1


if __name__ == "__main__":
    app.run_server(debug=True)
