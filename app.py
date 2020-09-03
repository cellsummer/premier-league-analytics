import dash
import dash_table
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash_table.Format import Format, Scheme, Sign, Symbol
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_proc import SeasonSummary
import h2h_cards as cards
from news import get_latest_news, generate_news_card

# external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
external_stylesheets = [dbc.themes.SANDSTONE]

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-sMcale=1"}],
    external_stylesheets=external_stylesheets,
)
# app = dash.Dash(__name__)
# data model
all_df = pd.read_csv("data/bet_data.csv", low_memory=False)

seasons = all_df["season"].unique().tolist()
seasons.sort()
dropdown_seasons = [{"label": season, "value": season} for season in seasons]

teams = all_df["HomeTeam"].unique().tolist()
teams.sort()
dropdown_teams = [{"label": team, "value": team} for team in teams]

big_6 = [
    "Liverpool",
    "Arsenal",
    "Chelsea",
    "Man United",
    "Man City",
    "Tottenham",
]


# navigation bar

tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    label="League Tables",
                    tab_id="tab-league-tables",
                    tabClassName="ml-auto",
                    labelClassName="text-primary",
                ),
                dbc.Tab(
                    label="Results Matrix",
                    tab_id="tab-results-matrix",
                    labelClassName="text-primary",
                    # tabClassName="tab-pane fade active show",
                ),
                dbc.Tab(
                    label="Stats", tab_id="tab-stats", labelClassName="text-primary",
                ),
                dbc.Tab(
                    label="Head-to-head",
                    tab_id="tab-h2h",
                    labelClassName="text-primary",
                ),
                dbc.Tab(
                    label="Goals & Scores",
                    tab_id="tab-goals-n-scores",
                    labelClassName="text-primary",
                ),
                dbc.Tab(
                    label="Latest News",
                    tab_id="tab-latest-news",
                    labelClassName="text-primary",
                ),
            ],
            id="tabs",
            active_tab="tab-league-tables",
        ),
        html.Div(id="content"),
    ]
)

banner = html.A(
    id="banner",
    children=[
        html.Img(
            src=app.get_asset_url("Barclays_PL.png"),
            style={"height": "2rem", "width": "auto",},
        ),
    ],
    href="https://www.premierleague.com/",
)

desc_card = html.Div(
    id="description-card",
    children=[
        html.H5("Premier League Analytics", className="text-primary"),
        html.H4("Welcome to the Premier League Dashboard", className="text-primary"),
        html.Div(
            id="intro",
            children="Explore historical results for the Premier League season and see the analytics and betting odds for your favourite team.",
        ),
    ],
)

drop_down_card = html.Div(
    id="control-card",
    children=[
        html.H5("Select your season:", className="text-primary"),
        dcc.Dropdown(
            id="dropdown_season",
            options=dropdown_seasons,
            value=seasons[-1],
            placeholder=seasons[-1],
            clearable=False,
        ),
        html.Br(),
        html.Br(),
        html.H5("Select home team:", className="text-primary"),
        dcc.Dropdown(
            id="dropdown_home_team",
            options=dropdown_teams,
            value=big_6[0],
            placeholder=big_6[0],
            clearable=False,
        ),
        html.Br(),
        html.H5("Select away team:", className="text-primary"),
        dcc.Dropdown(
            id="dropdown_away_team",
            options=dropdown_teams,
            value=big_6[1],
            placeholder=big_6[1],
            clearable=False,
        ),
        html.Br(),
    ],
)

results_matrix = html.Div(
    id="card-results-matrix",
    children=[
        html.H5("Results Matrix", className="text-primary"),
        html.Hr(),
        # data_table,
        dash_table.DataTable(
            id="results-matrix",
            # columns=[{"name": col, "id": col} for col in data_result_matrix.columns],
            # data=data_result_matrix.to_dict("records"),
            css=[{"selector": ".row", "rule": "margin: 0"}],
            style_cell={
                "textAlign": "center",
                "color": "var(--dark)",
                "whiteSpace": "normal",
                # "overflow": "hidden",
                "textOverflow": "ellipsis",
                "font_size": "12px",
            },
            style_data={
                "minWidth": "60px",
                "width": "60px",
                "maxWidth": "60px",
                # "height": "auto",
            },
            style_header={
                "backgroundColor": "var(--primary)",
                "fontWeight": "bold",
                "color": "var(--light)",
            },
            # fixed_columns={"headers": True, "data": 1},
            # # fixed_rows={"headers": True, "data": 1},
            # number of rows to show per page
            page_size=25,
            # style_as_list_view=True,
            style_cell_conditional=[{"if": {"column_id": "Teams"}, "width": "90px"},],
            style_header_conditional=[{"if": {"column_id": "Teams"}, "width": "90px"},],
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgba(0, 0, 0, 0.075)",}
            ],
            style_table={"minWidth": "100%", "overflowX": "auto",},
        ),
    ],
    # style={"display": "none"},
)

# Page : Stats
stats_page_style = {
    "css": [{"selector": ".row", "rule": "margin: 0"}],
    "style_cell": {
        "textAlign": "center",
        "color": "var(--primary)",
        "whiteSpace": "normal",
        "textOverflow": "ellipsis",
        "font_size": "14px",
        "maxWidth": "3rem",
    },
    "style_header": {
        "backgroundColor": "var(--primary)",
        "fontWeight": "bold",
        "color": "var(--light)",
    },
    "style_table": {"minWidth": "100%", "overflowX": "auto",},
}

card_corners = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Stats - Corners", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-corners",
                    columns=[
                        {"name": "CORNERS", "id": "index"},
                        {"name": "Count", "id": "corners_cnt"},
                        {"name": "Average per match", "id": "corners_per_game"},
                        {"name": "Maximum in a match", "id": "corners_max"},
                        {"name": "Minimum in a match", "id": "corners_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)

card_fouls = dbc.Card(
    children=[
        # dbc.CardHeader("Stats - Fouls", className="card-title"),
        dbc.CardBody(
            [
                html.H5("Stats - Fouls", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-fouls",
                    columns=[
                        {"name": "FOULS", "id": "index"},
                        {"name": "Count", "id": "fouls_cnt"},
                        {"name": "Average per match", "id": "fouls_per_game"},
                        {"name": "Maximum in a match", "id": "fouls_max"},
                        {"name": "Minimum in a match", "id": "fouls_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)

card_shots = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Stats - Shots", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-shots",
                    columns=[
                        {"name": "SHOTS", "id": "index"},
                        {"name": "Count", "id": "shots_cnt"},
                        {"name": "Average per match", "id": "shots_per_game"},
                        {"name": "Maximum in a match", "id": "shots_max"},
                        {"name": "Minimum in a match", "id": "shots_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)

card_shots_on_target = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Stats - Shots On Target", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-shots-on-target",
                    columns=[
                        {"name": "SHOTS ON TARGET", "id": "index"},
                        {"name": "Count", "id": "shots_on_target_cnt"},
                        {"name": "Average per match", "id": "shots_on_target_per_game"},
                        {"name": "Maximum in a match", "id": "shots_on_target_max"},
                        {"name": "Minimum in a match", "id": "shots_on_target_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)

card_yellow_cards = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Stats - Yellow Cards", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-yellow-cards",
                    columns=[
                        {"name": "YELLOW CARDS", "id": "index"},
                        {"name": "Count", "id": "yellow_cards_cnt"},
                        {"name": "Average per match", "id": "yellow_cards_per_game"},
                        {"name": "Maximum in a match", "id": "yellow_cards_max"},
                        {"name": "Minimum in a match", "id": "yellow_cards_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)

card_red_cards = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Stats - Red Cards", className="card-title text-primary"),
                html.Hr(),
                dash_table.DataTable(
                    id="stats-red-cards",
                    columns=[
                        {"name": "RED CARDS", "id": "index"},
                        {"name": "Count", "id": "red_cards_cnt"},
                        {"name": "Average per match", "id": "red_cards_per_game"},
                        {"name": "Maximum in a match", "id": "red_cards_max"},
                        {"name": "Minimum in a match", "id": "red_cards_min"},
                    ],
                    **stats_page_style,
                ),
            ],
        ),
    ],
)


card_stats = html.Div(
    id="card-stats",
    style={"display": "none"},
    children=[
        dbc.Row([dbc.Col(card_corners, width=6), dbc.Col(card_fouls, width=6)]),
        html.Hr(),
        dbc.Row([dbc.Col(card_shots, width=6), dbc.Col(card_shots_on_target, width=6)]),
        html.Hr(),
        dbc.Row(
            [dbc.Col(card_yellow_cards, width=6), dbc.Col(card_red_cards, width=6)]
        ),
    ],
)
###############################################

# Page: Tables

# dropdown selector for the league table type (overall/home/away)
league_table_selector = dcc.Dropdown(
    id="league-table-selector",
    options=[
        {"label": "Overall Table", "value": "overall"},
        {"label": "Home Table", "value": "home"},
        {"label": "Away Table", "value": "away"},
    ],
    value="overall",
    placeholder="overall",
    clearable=False,
    className="text-primary",
)

league_table_cols = [
    {"name": "Rank", "id": "rank"},
    {"name": "Team", "id": "team"},
    {"name": "Played", "id": "played"},
    {"name": "Won", "id": "won"},
    {"name": "Draw", "id": "draw"},
    {"name": "Lost", "id": "lost"},
    {"name": "Goals scored", "id": "goals_scored"},
    {"name": "Goals conceded", "id": "goals_conceded"},
    {"name": "GD", "id": "gd"},
    {"name": "Points", "id": "points"},
    {
        "name": "Goals scored per game",
        "id": "goals_scored_pg",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Goals conceded per game",
        "id": "goals_conceded_pg",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Corners for",
        "id": "corners_for",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Corners against",
        "id": "corners_against",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Shots made",
        "id": "shots_made",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Shots allowed",
        "id": "shots_allowed",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Shots to score a goal",
        "id": "shots_to_score_a_goal",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Shots to concede a goal",
        "id": "shots_to_concede_a_goal",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Yellow cards",
        "id": "yellow_cards",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {"name": "Red cards TOTAL", "id": "red_cards_total"},
    {
        "name": "Fouls commited",
        "id": "fouls_commited",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
    {
        "name": "Fouls suffered",
        "id": "fouls_suffered",
        "type": "numeric",
        "format": Format(precision=2, scheme=Scheme.fixed),
    },
]
league_tables = html.Div(
    id="card-league-tables",
    children=[
        dbc.Row(
            [
                dbc.Col(html.H5("League Tables", className="text-primary"), width=2),
                dbc.Col(league_table_selector, width=2),
            ]
        ),
        html.Hr(),
        # data_table,
        dash_table.DataTable(
            id="league-tables",
            columns=league_table_cols,
            # data=data_league_tables.to_dict("records"),
            css=[{"selector": ".row", "rule": "margin: 0"}],
            style_cell={
                "textAlign": "center",
                # "color": "var(--primary)",
                "whiteSpace": "normal",
                "textOverflow": "ellipsis",
                "font_size": "12px",
            },
            style_data={
                "minWidth": "50px",
                "width": "50px",
                "maxWidth": "50px",
                "height": "auto",
            },
            style_header={
                "backgroundColor": "var(--primary)",
                "fontWeight": "bold",
                "color": "var(--light)",
            },
            # fixed_columns={"headers": True, "data": 1},
            # number of rows to show per page
            page_size=25,
            # style_as_list_view=True,
            style_cell_conditional=[{"if": {"column_id": "team"}, "width": "90px"},],
            style_header_conditional=[{"if": {"column_id": "team"}, "width": "90px"},],
            style_data_conditional=[
                {"if": {"row_index": "odd"}, "backgroundColor": "rgba(0, 0, 0, 0.075)",}
            ],
            style_table={"minWidth": "100%", "overflowX": "auto"},
        ),
    ],
    # style={"display": "none"},
)
###############################################

# Page: Head-to-Head
cards_h2h = dbc.Row(
    [
        dbc.Col(cards.generate_cards_h2h("Liverpool"), width=6),
        dbc.Col(cards.generate_cards_h2h("Chelsea", False), width=6),
    ],
    id="card-h2h",
)

# Page: Goal spread
cards_goals_spread = html.Div(
    children=[
        html.H5("Full-time Score & Fair Odds", className="text-primary"),
        html.Hr(),
        dcc.Graph(id="graph-goals-spread"),
    ],
    id="card-goals-spread",
)

# Page: Latest news
articles_to_load = 20  # even number
articles = get_latest_news()

cards_latest_news = []
for i in range(int(articles_to_load / 2)):
    article_1 = generate_news_card(articles[2 * i])
    article_2 = generate_news_card(articles[2 * i + 1])

    news_row = dbc.Row([dbc.Col(article_1, width=6), dbc.Col(article_2, width=6)])
    cards_latest_news.append(news_row)

page_news = html.Div(id="page-news", children=cards_latest_news)

# overall layout

left_pannel = html.Div(
    id="left-column",
    className="four columns",
    children=[desc_card, html.Hr(), drop_down_card,],
)

right_pannel = html.Div(
    id="right-column",
    className="eight columns",
    children=[
        results_matrix,
        league_tables,
        card_stats,
        cards_h2h,
        cards_goals_spread,
        page_news,
    ],
)

app.title = "Dash - Premier League Dashboard"
app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        dbc.Row(
            [dbc.Col(banner, width=2, align="center"), dbc.Col(tabs, width=10)],
            style={"padding": "1rem", "background-color": "white"},
        ),
        dbc.Row(
            [dbc.Col(left_pannel, width=2,), dbc.Col(right_pannel, width=10,),],
            style={"padding": "1rem"},
            # no_gutters=True,
        ),
        # hidden div for storing json data
        # html.Div(id="intermediate-value", style={"display": "none"}),
        # html.Div(id="intermediate-goals", style={"display": "none"}),
    ],
)


# col 1: descriptions
descr_summary = html.P(
    "Matches played - Wins-Draws - Losses - Goals Scored - Goals Conceded"
)
descr_general = html.P("League position, total points and average points per match")
descr_goals = html.P("Average goals per match")
descr_corners = html.P("AVERAGE corners per match - For - Against - Total")
descr_shots_on_goal = html.P("AVERAGE shots on goal - For - Against")
descr_fouls = html.P("AVERAGE fouls commited and suffered")

# retrieve intermediate data for the data table
@app.callback(
    [
        Output(component_id="results-matrix", component_property="data"),
        Output(component_id="results-matrix", component_property="columns"),
        Output(component_id="stats-corners", component_property="data"),
        Output(component_id="stats-fouls", component_property="data"),
        Output(component_id="stats-shots", component_property="data"),
        Output(component_id="stats-shots-on-target", component_property="data"),
        Output(component_id="stats-yellow-cards", component_property="data"),
        Output(component_id="stats-red-cards", component_property="data"),
        Output(component_id="league-tables", component_property="data"),
        Output(component_id="h2h-summary-home", component_property="data"),
        Output(component_id="h2h-general-home", component_property="data"),
        Output(component_id="h2h-goals-home", component_property="data"),
        Output(component_id="h2h-corners-home", component_property="data"),
        Output(component_id="h2h-sog-home", component_property="data"),
        Output(component_id="h2h-fouls-home", component_property="data"),
        Output(component_id="h2h-header-home", component_property="children"),
        Output(component_id="h2h-summary-away", component_property="data"),
        Output(component_id="h2h-general-away", component_property="data"),
        Output(component_id="h2h-goals-away", component_property="data"),
        Output(component_id="h2h-corners-away", component_property="data"),
        Output(component_id="h2h-sog-away", component_property="data"),
        Output(component_id="h2h-fouls-away", component_property="data"),
        Output(component_id="h2h-header-away", component_property="children"),
    ],
    [
        Input(component_id="dropdown_season", component_property="value"),
        Input(component_id="dropdown_home_team", component_property="value"),
        Input(component_id="dropdown_away_team", component_property="value"),
        Input(component_id="league-table-selector", component_property="value"),
    ],
)
def update_dt_div(season, home_team, away_team, table_type):
    data_summary = SeasonSummary(data=all_df, season=season)

    data_result_matrix = data_summary.get_result_matrix()
    cols_result_matrix = [
        {"name": col, "id": col} for col in data_result_matrix.columns
    ]

    data_stats = data_summary.summary_stats()

    data_stats_corners = data_stats.iloc[:, 0:5]
    data_stats_shots = data_stats.iloc[:, [0, 5, 6, 7, 8]]
    data_stats_shots_on_target = data_stats.iloc[:, [0, 9, 10, 11, 12]]
    data_stats_yellow_cards = data_stats.iloc[:, [0, 13, 14, 15, 16]]
    data_stats_red_cards = data_stats.iloc[:, [0, 17, 18, 19, 20]]
    data_stats_fouls = data_stats.iloc[:, [0, 21, 22, 23, 24]]

    data_league_tables = data_summary.calc_main_tables(table_type)

    data_h2h_summary_home = data_summary.calc_team_stats(home_team)
    data_h2h_summary_away = data_summary.calc_team_stats(away_team)

    return [
        data_result_matrix.to_dict("records"),
        cols_result_matrix,
        data_stats_corners.to_dict("records"),
        data_stats_fouls.to_dict("records"),
        data_stats_shots.to_dict("records"),
        data_stats_shots_on_target.to_dict("records"),
        data_stats_yellow_cards.to_dict("records"),
        data_stats_red_cards.to_dict("records"),
        data_league_tables.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        data_h2h_summary_home.to_dict("records"),
        home_team,
        data_h2h_summary_away.to_dict("records"),
        data_h2h_summary_away.to_dict("records"),
        data_h2h_summary_away.to_dict("records"),
        data_h2h_summary_away.to_dict("records"),
        data_h2h_summary_away.to_dict("records"),
        data_h2h_summary_away.to_dict("records"),
        away_team
        # cols_stats_corners,
    ]


@app.callback(
    Output(component_id="graph-goals-spread", component_property="figure"),
    [Input(component_id="dropdown_season", component_property="value"),],
)
def update_charts(season):
    data_summary = SeasonSummary(data=all_df, season=season)
    df_goals_spread = data_summary.summary_goal_spread()
    fig = make_subplots(
        rows=1,
        cols=2,
        specs=[[{"type": "domain"}, {"type": "bar"}]],
        subplot_titles=("Percentages - Fulltime Score", "Fair Odds - Fulltime Score"),
    )
    fig.add_trace(
        go.Pie(
            labels=df_goals_spread["index"],
            values=df_goals_spread["match_cnt"],
            name="Percentage",
        ),
        1,
        1,
    )
    fig.add_trace(
        go.Bar(
            x=df_goals_spread["index"],
            y=df_goals_spread["fair_odds"],
            # color=df_goals_spread["index"],
            name="Fair Odds",
        ),
        1,
        2,
    )
    # fig = px.pie(
    #     df_goals_spread,
    #     values="match_cnt",
    #     names="index",
    #     # title=f"Score spread - season {season}",
    #     hover_data=["fair_odds"],
    #     labels={"match_cnt": "Number of Matches", "index": "Score"},
    # )
    fig.update_layout(
        transition_duration=100, xaxis={"categoryorder": "total ascending"}
    )
    return fig


# tabs
@app.callback(
    [
        Output("card-results-matrix", "style"),
        Output("card-stats", "style"),
        Output("card-league-tables", "style"),
        Output("card-h2h", "style"),
        Output("card-goals-spread", "style"),
        Output("page-news", "style"),
    ],
    [Input("tabs", "active_tab")],
)
def tab_content(active_tab):
    style_in_display = {"display": ""}
    style_not_display = {"display": "none"}

    if active_tab == "tab-results-matrix":
        return [
            style_in_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
        ]
    elif active_tab == "tab-stats":
        return [
            style_not_display,
            style_in_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
        ]
    elif active_tab == "tab-league-tables":
        return [
            style_not_display,
            style_not_display,
            style_in_display,
            style_not_display,
            style_not_display,
            style_not_display,
        ]
    elif active_tab == "tab-h2h":
        return [
            style_not_display,
            style_not_display,
            style_not_display,
            style_in_display,
            style_not_display,
            style_not_display,
        ]
    elif active_tab == "tab-goals-n-scores":
        return [
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_in_display,
            style_not_display,
        ]
    elif active_tab == "tab-latest-news":
        return [
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_in_display,
        ]
    else:
        return [
            style_in_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
            style_not_display,
        ]


if __name__ == "__main__":
    app.run_server(debug=True)
