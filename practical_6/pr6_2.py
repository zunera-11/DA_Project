import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

# ---------------------------------------------------------------
# 1. DATA LAYER (replace with your own data source)
# ---------------------------------------------------------------

rng = np.random.default_rng(42)
n = 5000

df = pd.DataFrame(
    {
        "date": pd.to_datetime("2025-01-01")
        + pd.to_timedelta(rng.integers(0, 365, n), unit="D"),
        "region": rng.choice(
            ["North", "South", "East", "West"], n
        ),
        "category": rng.choice(
            ["Electronics", "Clothing", "Home", "Sports"], n
        ),
        "units": rng.integers(1, 10, n),
        "unit_price": rng.uniform(10, 200, n).round(2),
    }
)

df["revenue"] = df["units"] * df["unit_price"]


# ---------------------------------------------------------------
# 2. DASH APP AND LAYOUT
# ---------------------------------------------------------------

app = Dash(__name__)

CARD = {
    "flex": "1",
    "padding": "16px",
    "border": "1px solid #dddddd",
    "borderRadius": "8px",
    "backgroundColor": "#ffffff",
}

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "padding": "20px",
        "backgroundColor": "#f7f7f7",
    },
    children=[
        html.H1("Sales Analytics Dashboard"),

        # ---- Filters ----
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label("Region"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=sorted(df["region"].unique()),
                            value=sorted(df["region"].unique()),
                            multi=True,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label("Category"),
                        dcc.Dropdown(
                            id="category-filter",
                            options=sorted(df["category"].unique()),
                            value=sorted(df["category"].unique()),
                            multi=True,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "250px"},
                    children=[
                        html.Label("Date range"),
                        html.Br(),
                        dcc.DatePickerRange(
                            id="date-filter",
                            min_date_allowed=df["date"].min(),
                            max_date_allowed=df["date"].max(),
                            start_date=df["date"].min(),
                            end_date=df["date"].max(),
                        ),
                    ],
                ),
            ],
        ),

        # ---- KPI cards ----
        html.Div(
            id="kpi-row",
            style={
                "display": "flex",
                "gap": "16px",
                "marginBottom": "20px",
                "flexWrap": "wrap",
            },
        ),

        # ---- Charts ----
        dcc.Graph(id="trend-chart"),

        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
            },
            children=[
                dcc.Graph(
                    id="category-chart",
                    style={"flex": "1", "minWidth": "300px"},
                ),
                dcc.Graph(
                    id="region-chart",
                    style={"flex": "1", "minWidth": "300px"},
                ),
            ],
        ),
    ],
)


# ---------------------------------------------------------------
# 3. HELPERS
# ---------------------------------------------------------------

def filter_data(regions, categories, start, end) -> pd.DataFrame:
    regions = regions or []
    categories = categories or []

    return df[
        df["region"].isin(regions)
        & df["category"].isin(categories)
        & df["date"].between(
            pd.Timestamp(start), pd.Timestamp(end)
        )
    ]


def kpi_card(title: str, value: str) -> html.Div:
    return html.Div(
        style=CARD,
        children=[
            html.Div(title, style={"color": "#666"}),
            html.H2(value, style={"margin": "4px 0 0"}),
        ],
    )


# ---------------------------------------------------------------
# 4. CALLBACKS
# One callback updates all outputs from the filters
# ---------------------------------------------------------------

@app.callback(
    Output("kpi-row", "children"),
    Output("trend-chart", "figure"),
    Output("category-chart", "figure"),
    Output("region-chart", "figure"),
    Input("region-filter", "value"),
    Input("category-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date"),
)
def update_dashboard(regions, categories, start, end):
    d = filter_data(regions, categories, start, end)

    # Edge case: empty selection
    if d.empty:
        empty = px.scatter(
            title="No data for the selected filters"
        )
        return (
            [kpi_card("Total Revenue", "$0")],
            empty,
            empty,
            empty,
        )

    # ---- KPI cards ----
    kpis = [
        kpi_card(
            "Total Revenue",
            f"${d['revenue'].sum():,.0f}",
        ),
        kpi_card(
            "Orders",
            f"{len(d):,}",
        ),
        kpi_card(
            "Avg Order Value",
            f"${d['revenue'].mean():,.2f}",
        ),
        kpi_card(
            "Units Sold",
            f"{d['units'].sum():,}",
        ),
    ]

    # ---- Monthly revenue trend ----
    monthly = (
        d.set_index("date")
        .resample("MS")["revenue"]
        .sum()
        .reset_index()
    )

    fig_trend = px.line(
        monthly,
        x="date",
        y="revenue",
        markers=True,
        title="Monthly Revenue Trend",
    )

    # ---- Revenue by category ----
    by_cat = (
        d.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue")
    )

    fig_cat = px.bar(
        by_cat,
        x="revenue",
        y="category",
        orientation="h",
        title="Revenue by Category",
    )

    # ---- Revenue by region ----
    by_reg = (
        d.groupby("region", as_index=False)["revenue"]
        .sum()
    )

    fig_reg = px.bar(
        by_reg,
        x="region",
        y="revenue",
        title="Revenue by Region",
    )

    return kpis, fig_trend, fig_cat, fig_reg


# ---------------------------------------------------------------
# 5. RUN
# ---------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)