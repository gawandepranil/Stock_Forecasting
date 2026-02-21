import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ──────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPER
# ──────────────────────────────────────────────────────────────────────────────

def _clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flatten yfinance MultiIndex columns and ensure a plain 'Date' column.
    Sorts MultiIndex BEFORE any slicing to avoid PerformanceWarning.
    """
    df = df.copy()

    # Move Date/Datetime index to a column
    if df.index.name in ("Date", "Datetime"):
        df = df.reset_index()

    # Sort FIRST — prevents PerformanceWarning on non-lexsorted MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df = df.sort_index(axis=1)

    # Flatten MultiIndex -> plain strings
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(x) for x in col if x not in ("", None)]).strip("_")
            for col in df.columns
        ]
    else:
        df.columns = [
            "_".join(map(str, c)) if isinstance(c, tuple) else str(c)
            for c in df.columns
        ]

    # Strip stray underscores left by empty MultiIndex levels
    df.columns = [c.strip("_") for c in df.columns]

    # Recover 'Date' column if reset_index named it 'index'
    if "Date" not in df.columns and "index" in df.columns:
        df = df.rename(columns={"index": "Date"})

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    return df


# ──────────────────────────────────────────────────────────────────────────────
# PUBLIC FUNCTIONS
# ──────────────────────────────────────────────────────────────────────────────

def interactive_plot(df: pd.DataFrame, title: str = "Stock Prices") -> go.Figure:
    """Plot all numeric columns (except 'Date') as Plotly line traces."""
    df = _clean_columns(df)

    if "Date" not in df.columns:
        raise ValueError(
            "Date column not found after cleaning. "
            "Columns present: " + str(list(df.columns))
        )

    fig = go.Figure()

    for col in df.columns:
        if col == "Date":
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        fig.add_scatter(x=df["Date"], y=df[col], mode="lines", name=str(col))

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode="x unified",
        legend_title="Series",
        margin=dict(l=10, r=10, t=50, b=10),
    )

    return fig


def normalize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Divide every numeric column (except 'Date') by its first value
    so all series start at 1.0 for fair visual comparison.

    FIX: original used df.columns[1:] which silently skips 'Date' by position —
    breaks if column order changes. Now explicitly checks col != 'Date'.
    Uses .loc for Copy-on-Write safety.
    """
    df = _clean_columns(df)
    df_copy = df.copy()

    for col in df_copy.columns:
        if col == "Date":
            continue
        if not pd.api.types.is_numeric_dtype(df_copy[col]):
            continue
        first = df_copy[col].iloc[0]
        if pd.notna(first) and first != 0:
            df_copy.loc[:, col] = df_copy[col] / first   # CoW-safe

    return df_copy


def daily_return(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute % daily returns for every numeric column except 'Date'.

    FIX 1: original row-by-row loop was O(n x cols) — very slow on 1yr+ data.
    FIX 2: df_daily_return[col][row] = ... triggers ChainedAssignmentError
            under pandas Copy-on-Write mode.
    Solution: vectorised pct_change() + single-step .loc assignment.
    """
    df = _clean_columns(df)
    df_daily = df.copy()

    for col in df_daily.columns:
        if col == "Date":
            continue
        if not pd.api.types.is_numeric_dtype(df_daily[col]):
            continue

        pct = df_daily[col].pct_change() * 100       # vectorised, fast
        df_daily.loc[:, col] = pct                    # CoW-safe single step
        df_daily.loc[df_daily.index[0], col] = 0.0   # first row = 0

    return df_daily


def calculate_beta(stock_daily_return: pd.DataFrame, stock: str) -> tuple[float, float]:
    """
    Calculate Beta and Alpha for *stock* vs the 'sp500' column using OLS.

    FIX: original flattened MultiIndex with col[0] which kept the Price label
    ('Close') instead of the Ticker name — produced wrong column names.
    Now delegates column cleaning to _clean_columns() instead.

    Returns
    -------
    (beta, alpha) : tuple[float, float]
    """
    df = _clean_columns(stock_daily_return)

    if "sp500" not in df.columns:
        raise ValueError("'sp500' column not found in daily-returns DataFrame.")
    if stock not in df.columns:
        raise ValueError(f"'{stock}' column not found in daily-returns DataFrame.")

    data   = df[["sp500", stock]].dropna()
    market = data["sp500"].astype(float)
    stk    = data[stock].astype(float)

    beta, alpha = np.polyfit(market, stk, 1)
    return round(float(beta), 4), round(float(alpha), 4)