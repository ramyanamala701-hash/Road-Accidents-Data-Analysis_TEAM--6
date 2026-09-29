"""Dependency-light SVG charts from observed accident records."""
from html import escape
from pathlib import Path
import pandas as pd

from .data_aggregation import build_aggregations, MONTH_ORDER
from .utils import FIGURES_DIR

BLUE = "#2878B5"
ORANGE = "#E58936"


def _text(x, y, label, size=13, anchor="start", color="#253247"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial,sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(str(label))}</text>'


def _doc(width, height, title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
            '<rect width="100%" height="100%" fill="white"/>'
            + _text(width / 2, 30, title, 19, "middle") + body + "</svg>")


def _bar(table: pd.DataFrame, category: str, metric: str, title: str, path: Path, limit=20):
    data = table.dropna(subset=[category, metric]).sort_values(metric, ascending=False, kind="stable").head(limit)
    labels = data[category].astype(str).tolist()
    values = pd.to_numeric(data[metric], errors="coerce").fillna(0).tolist()
    width, row_h, left, right, top = 1000, 29, 250, 80, 65
    height = max(180, top + row_h * len(labels) + 35)
    max_value = max(values, default=0) or 1
    chart_w = width - left - right
    body = []
    for i, (label, value) in enumerate(zip(labels, values)):
        y = top + i * row_h
        bar_w = chart_w * value / max_value
        body.append(_text(left - 10, y + 17, label, 12, "end"))
        body.append(f'<rect x="{left}" y="{y}" width="{bar_w:.1f}" height="19" rx="3" fill="{BLUE}"/>')
        body.append(_text(left + bar_w + 7, y + 15, f"{value:,.0f}", 11))
    body.append(_text(left + chart_w / 2, height - 8, metric.replace("_", " ").title(), 12, "middle"))
    path.write_text(_doc(width, height, title, "".join(body)), encoding="utf-8")


def _monthly(table: pd.DataFrame, path: Path):
    data = table.copy()
    data["_order"] = data.month.map(MONTH_ORDER)
    data = data.sort_values("_order")
    width, height, left, right, top, bottom = 960, 470, 75, 40, 65, 65
    values = data.accident_count.astype(float).tolist()
    labels = data.month.astype(str).tolist()
    maximum = max(values, default=1) or 1
    plot_w, plot_h = width-left-right, height-top-bottom
    points = []
    body = []
    for i, (label, value) in enumerate(zip(labels, values)):
        x = left + plot_w * i / max(1, len(values)-1)
        y = top + plot_h - plot_h * value / maximum
        points.append((x, y))
        body.append(_text(x, height-bottom+23, label, 11, "middle"))
        body.append(_text(x, y-10, f"{value:.0f}", 10, "middle"))
    body.insert(0, '<polyline fill="none" stroke="' + BLUE + '" stroke-width="3" points="' + " ".join(f"{x:.1f},{y:.1f}" for x,y in points) + '"/>')
    body.extend(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{ORANGE}"/>' for x,y in points)
    body.append(_text(width/2, height-13, "Month", 12, "middle"))
    path.write_text(_doc(width, height, "Recorded accidents by month", "".join(body)), encoding="utf-8")


def _speed_scatter(df: pd.DataFrame, path: Path):
    xvals = pd.to_numeric(df.speed_limit_kmph, errors="coerce")
    yvals = pd.to_numeric(df.estimated_speed_kmph, errors="coerce")
    valid = xvals.notna() & yvals.notna()
    xvals, yvals = xvals[valid], yvals[valid]
    width, height, left, top, bottom, right = 760, 560, 80, 65, 75, 35
    xlo, xhi = min(xvals.min(), 0), max(xvals.max(), 1)
    ylo, yhi = min(yvals.min(), 0), max(yvals.max(), 1)
    plot_w, plot_h = width-left-right, height-top-bottom
    body = []
    for x, y in zip(xvals, yvals):
        sx = left + (x-xlo)/(xhi-xlo or 1)*plot_w
        sy = top + plot_h - (y-ylo)/(yhi-ylo or 1)*plot_h
        body.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="4" fill="{BLUE}" fill-opacity="0.55"/>')
    # The equality line is a visual reference, not a fitted relationship.
    low, high = max(xlo, ylo), min(xhi, yhi)
    if low < high:
        x1 = left + (low-xlo)/(xhi-xlo or 1)*plot_w
        y1 = top + plot_h - (low-ylo)/(yhi-ylo or 1)*plot_h
        x2 = left + (high-xlo)/(xhi-xlo or 1)*plot_w
        y2 = top + plot_h - (high-ylo)/(yhi-ylo or 1)*plot_h
        body.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 5"/>')
    body.append(_text(width/2, height-20, "Listed speed limit (km/h)", 12, "middle"))
    body.append(_text(18, height/2, "Estimated speed (km/h)", 12, "middle"))
    body.append(_text(width-right-5, top+18, "Dashed line: estimated speed equals limit", 11, "end", ORANGE))
    path.write_text(_doc(width, height, "Estimated speed and listed speed limit", "".join(body)), encoding="utf-8")


def create_visualizations(df: pd.DataFrame, output_dir: Path = FIGURES_DIR) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    tables = build_aggregations(df)
    for old_name in ["yearly_accident_trend.svg", "top_states_accidents.svg",
                     "state_2016_vs_2019.svg", "state_accident_trends.svg",
                     "yearly_accident_trend.png", "top_states_accidents.png",
                     "state_2016_vs_2019.png", "state_accident_trends.png"]:
        (output_dir / old_name).unlink(missing_ok=True)
    definitions = [
        ("accidents_by_year", "year", "accident_count", "Recorded accidents by year", "accidents_by_year.svg", 20),
        ("accidents_by_state_ut", "state_ut", "accident_count", "Recorded accidents by State/UT", "accidents_by_state_ut.svg", 20),
        ("accidents_by_severity", "severity", "accident_count", "Recorded severity distribution", "severity_distribution.svg", 20),
        ("accidents_by_primary_cause", "primary_cause", "accident_count", "Recorded primary causes", "primary_cause_distribution.svg", 20),
        ("accidents_by_vehicle_type", "vehicle_type", "accident_count", "Vehicle types in records", "vehicle_type_distribution.svg", 20),
        ("accidents_by_road_type", "road_type", "accident_count", "Recorded accidents by road type", "accidents_by_road_type.svg", 20),
        ("accidents_by_weather", "weather", "accident_count", "Recorded accidents by weather", "accidents_by_weather.svg", 20),
        ("accidents_by_lighting", "lighting", "accident_count", "Recorded accidents by lighting", "accidents_by_lighting.svg", 20),
        ("fatalities_by_state_ut", "state_ut", "fatalities", "Recorded fatalities by State/UT", "fatalities_by_state_ut.svg", 20),
        ("accidents_by_alcohol_involvement", "alcohol_involved", "accident_count", "Records by alcohol involvement", "alcohol_involvement.svg", 20),
        ("accidents_by_pedestrian_involvement", "pedestrians_involved", "accident_count", "Records involving pedestrians", "pedestrian_involvement.svg", 20),
    ]
    paths = []
    for table_name, category, metric, title, filename, limit in definitions:
        path = output_dir / filename
        _bar(tables[table_name], category, metric, title, path, limit)
        paths.append(path)
    month_path = output_dir / "accidents_by_month.svg"
    _monthly(tables["accidents_by_month"], month_path)
    paths.append(month_path)
    speed_path = output_dir / "speed_limit_vs_estimated_speed.svg"
    _speed_scatter(df, speed_path)
    paths.append(speed_path)
    return paths
