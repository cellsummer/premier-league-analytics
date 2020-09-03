import dash
import dash_table
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash_table.Format import Format, Scheme, Sign, Symbol


def generate_cards_h2h(team, is_home=True):
    """generates the key components for the h2h page"""
    card_head = html.H5(
        team,
        id="h2h-header-home" if is_home else "h2h-header-away",
        className="card-title text-primary",
    )
    # data table styles
    dt_styles = {
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
    # summary
    cols = [
        {"name": "General Data", "id": "category"},
        {"name": "MP", "id": "mp"},
        {"name": "W", "id": "win"},
        {"name": "D", "id": "draw"},
        {"name": "L", "id": "lost"},
        {"name": "GS", "id": "gs"},
        {"name": "GC", "id": "gc"},
    ]

    dt_summary = dash_table.DataTable(
        id="h2h-summary-home" if is_home else "h2h-summary-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    # general
    cols = [
        {"name": "General Data", "id": "category"},
        {"name": "League pos.", "id": "position"},
        {"name": "Points", "id": "points"},
        {
            "name": "Avg. points",
            "id": "avg_points",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
    ]
    dt_general = dash_table.DataTable(
        id="h2h-general-home" if is_home else "h2h-general-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    # goals
    cols = [
        {"name": "GOALS", "id": "category"},
        {
            "name": "Scored",
            "id": "avg_gs",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "Conceded",
            "id": "avg_gc",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "Total",
            "id": "avg_goals",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
    ]
    dt_goals = dash_table.DataTable(
        id="h2h-goals-home" if is_home else "h2h-goals-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    # corners
    cols = [
        {"name": "CORNERS", "id": "category"},
        {
            "name": "FOR",
            "id": "corners_for",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "AGAINST",
            "id": "corners_against",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "Total",
            "id": "corners_total",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
    ]

    dt_corners = dash_table.DataTable(
        id="h2h-corners-home" if is_home else "h2h-corners-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    # shots on goal
    cols = [
        {"name": "SHOTS ON GOAL", "id": "category"},
        {
            "name": "FOR",
            "id": "shots_on_goal_f",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "AGAINST",
            "id": "shots_on_goal_a",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
    ]

    dt_shots_on_goal = dash_table.DataTable(
        id="h2h-sog-home" if is_home else "h2h-sog-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    # fouls
    cols = [
        {"name": "FOULS", "id": "category"},
        {
            "name": "Commited",
            "id": "fouls_commited",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "SUFFERED",
            "id": "fouls_suffered",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
        {
            "name": "Total",
            "id": "fouls_total",
            "type": "numeric",
            "format": Format(precision=2, scheme=Scheme.fixed),
        },
    ]

    dt_fouls = dash_table.DataTable(
        id="h2h-fouls-home" if is_home else "h2h-fouls-away",
        columns=cols,
        # data=data_home_team.to_dict("records"),
        **dt_styles,
    )

    cards = [
        dbc.Card(dbc.CardBody(card_head), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_summary), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_general), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_goals), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_corners), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_shots_on_goal), className="mb-3"),
        dbc.Card(dbc.CardBody(dt_fouls), className="mb-3"),
    ]

    return cards
