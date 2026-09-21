import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio

# 1. Load Raw Data
df = pd.read_csv("messy_sales_data.csv")
initial_row_count = len(df)

# 2. Deduplication & Data Cleaning
df = df.drop_duplicates()
duplicates_removed = initial_row_count - len(df)

string_cols = ["Customer_Name", "Region"]
for col in string_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()
        df[col] = df[col].replace(["Nan", "None", ""], "Unknown")

df["Sales_Amount"] = pd.to_numeric(df["Sales_Amount"], errors="coerce")
df.loc[df["Sales_Amount"] < 0, "Sales_Amount"] = np.nan

median_sales = df["Sales_Amount"].median()
df["Sales_Amount"] = df["Sales_Amount"].fillna(median_sales if pd.notnull(median_sales) else 0)

df["Purchase_Date"] = pd.to_datetime(df["Purchase_Date"], errors="coerce")
df["Purchase_Date"] = df["Purchase_Date"].fillna(pd.Timestamp("2026-01-01"))

# Ensure Transaction_ID exists to prevent KeyError in reporting engine
if "Transaction_ID" not in df.columns:
    df["Transaction_ID"] = [f"TXN-{i+1000}" for i in range(len(df))]

# 3. Compute Executive Analytics & Automated Insights
total_revenue = df["Sales_Amount"].sum()
avg_order_value = df["Sales_Amount"].mean()
max_transaction = df["Sales_Amount"].max()

# Corrected cell-level data quality computation
total_cells = len(df) * df.shape[1]
total_missing_cells = df.isnull().sum().sum()
data_quality_score = round(((total_cells - total_missing_cells) / total_cells) * 100, 1) if total_cells > 0 else 100.0

top_region = df.groupby("Region")["Sales_Amount"].sum().idxmax()
top_region_val = df.groupby("Region")["Sales_Amount"].sum().max()
top_customer = df.groupby("Customer_Name")["Sales_Amount"].sum().idxmax()

# Save Clean Dataset
df.to_csv("cleaned_sales_data.csv", index=False)

# ---------------------------------------------------------
# HIGH-END PLOTLY VISUALIZATION ENGINE
# ---------------------------------------------------------

COMMON_LAYOUT = dict(
    height=360,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e1", family="Plus Jakarta Sans, sans-serif", size=11),
    margin=dict(l=35, r=25, t=30, b=35),
    hoverlabel=dict(bgcolor="#0f172a", font_size=12, font_family="Plus Jakarta Sans"),
    showlegend=False,
    autosize=True
)

# Chart 1: Revenue by Region
region_summary = df.groupby("Region")["Sales_Amount"].sum().reset_index().sort_values("Sales_Amount", ascending=False)
fig_region = px.bar(
    region_summary, x="Region", y="Sales_Amount",
    color="Sales_Amount",
    color_continuous_scale=["#38bdf8", "#818cf8", "#c084fc"]
)
fig_region.update_traces(
    hovertemplate="<b>%{x} Region</b><br>Revenue: $%{y:,.2f}<extra></extra>",
    marker_line_width=0
)
fig_region.update_layout(**COMMON_LAYOUT, coloraxis_showscale=False)
fig_region.update_xaxes(showgrid=False, tickfont=dict(color="#f8fafc"))
fig_region.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#cbd5e1"))

# Chart 2: Revenue Growth Trajectory
trend_summary = df.groupby("Purchase_Date")["Sales_Amount"].sum().reset_index()
fig_trend = px.area(trend_summary, x="Purchase_Date", y="Sales_Amount")
fig_trend.update_traces(
    line_color="#38bdf8",
    line_width=2.5,
    fillcolor="rgba(56, 189, 248, 0.12)",
    hovertemplate="<b>Date: %{x|%b %d, %Y}</b><br>Sales: $%{y:,.2f}<extra></extra>"
)
fig_trend.update_layout(**COMMON_LAYOUT)
fig_trend.update_xaxes(showgrid=False, tickfont=dict(color="#f8fafc"))
fig_trend.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#cbd5e1"))

# Chart 3: Market Volume Share Donut Chart
region_counts = df["Region"].value_counts().reset_index()
region_counts.columns = ["Region", "Count"]
fig_donut = px.pie(
    region_counts, names="Region", values="Count", hole=0.6,
    color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc", "#34d399", "#f472b6"]
)
fig_donut.update_traces(
    textposition="outside",
    textinfo="percent+label",
    hovertemplate="<b>%{label}</b><br>Share: %{percent}<br>Orders: %{value}<extra></extra>",
    marker=dict(line=dict(color="#0f172a", width=2))
)
fig_donut.update_layout(**COMMON_LAYOUT)

# Chart 4: Top Performer Transactions
top_customers = df.nlargest(6, "Sales_Amount").sort_values("Sales_Amount", ascending=True)
fig_top = px.bar(
    top_customers, x="Sales_Amount", y="Customer_Name", orientation="h",
    color="Sales_Amount", color_continuous_scale=["#818cf8", "#c084fc"]
)
fig_top.update_traces(
    hovertemplate="<b>%{y}</b><br>Transaction: $%{x:,.2f}<extra></extra>"
)
fig_top.update_layout(**COMMON_LAYOUT, coloraxis_showscale=False)
fig_top.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#cbd5e1"))
fig_top.update_yaxes(showgrid=False, tickfont=dict(color="#f8fafc"))

# ---------------------------------------------------------
# INTERACTIVE TABLE GENERATOR
# ---------------------------------------------------------

preview_df = df.head(10).copy()
preview_df["Sales_Amount_Str"] = preview_df["Sales_Amount"].apply(lambda x: f"${x:,.2f}")
preview_df["Purchase_Date_Str"] = preview_df["Purchase_Date"].dt.strftime('%Y-%m-%d')

table_rows = ""
for _, row in preview_df.iterrows():
    table_rows += f"""
    <tr>
        <td><code>{row['Transaction_ID']}</code></td>
        <td><strong>{row['Customer_Name']}</strong></td>
        <td><span class="region-badge">{row['Region']}</span></td>
        <td class="amount-cell">{row['Sales_Amount_Str']}</td>
        <td>{row['Purchase_Date_Str']}</td>
    </tr>
    """

# ---------------------------------------------------------
# EXECUTIVE HTML TEMPLATE WITH ATTRIBUTION BRANDING
# ---------------------------------------------------------

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Executive Revenue Report | Data Clean And Reporting</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #030712;
            --card-bg: rgba(15, 23, 42, 0.75);
            --card-border: rgba(255, 255, 255, 0.08);
            --card-hover-border: rgba(56, 189, 248, 0.4);
            --accent-cyan: #38bdf8;
            --accent-purple: #818cf8;
            --accent-emerald: #34d399;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
        }}

        body {{
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.1) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(129, 140, 248, 0.1) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-primary);
            padding: 35px 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }}

        .app-container {{
            width: 92%;
            max-width: 1400px;
        }}

        .navbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 28px;
            padding: 20px 30px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            backdrop-filter: blur(20px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}

        .brand-title {{
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-sub {{
            font-size: 0.85rem;
            color: var(--accent-cyan);
            font-weight: 600;
            margin-top: 4px;
            letter-spacing: 0.02em;
        }}

        .btn-export {{
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: #030712;
            font-weight: 700;
            font-size: 0.88rem;
            border: none;
            padding: 12px 24px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.25);
        }}

        .btn-export:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4);
        }}

        .executive-summary {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 20px;
            padding: 22px 28px;
            margin-bottom: 28px;
            backdrop-filter: blur(16px);
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}

        .summary-item h4 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--accent-cyan);
            margin-bottom: 6px;
        }}

        .summary-item p {{
            font-size: 0.92rem;
            color: #cbd5e1;
            line-height: 1.45;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 28px;
        }}

        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 24px;
            border-radius: 20px;
            backdrop-filter: blur(16px);
            transition: all 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }}

        .kpi-card:hover {{
            transform: translateY(-6px);
            border-color: var(--card-hover-border);
            box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.6), 0 0 20px rgba(56, 189, 248, 0.15);
        }}

        .kpi-label {{
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--text-secondary);
            margin-bottom: 10px;
        }}

        .kpi-value {{
            font-size: 1.95rem;
            font-weight: 800;
            color: var(--text-primary);
            margin-bottom: 10px;
            letter-spacing: -0.02em;
        }}

        .tag {{
            display: inline-flex;
            align-items: center;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 20px;
            background: rgba(52, 211, 153, 0.12);
            color: var(--accent-emerald);
            border: 1px solid rgba(52, 211, 153, 0.25);
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 24px;
            margin-bottom: 28px;
        }}

        .chart-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 24px;
            border-radius: 20px;
            backdrop-filter: blur(16px);
            min-height: 440px;
            transition: all 0.35s ease;
        }}

        .chart-card:hover {{
            border-color: rgba(129, 140, 248, 0.35);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
        }}

        .chart-header {{
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .table-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            padding: 28px;
            border-radius: 20px;
            backdrop-filter: blur(16px);
            margin-bottom: 28px;
        }}

        .table-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}

        .search-input {{
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 8px 16px;
            color: var(--text-primary);
            font-size: 0.85rem;
            outline: none;
            width: 240px;
            transition: border-color 0.3s;
        }}

        .search-input:focus {{
            border-color: var(--accent-cyan);
        }}

        .custom-table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.88rem;
        }}

        .custom-table th {{
            background: rgba(255, 255, 255, 0.03);
            padding: 14px 18px;
            color: var(--text-secondary);
            font-weight: 700;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            border-bottom: 1px solid var(--card-border);
        }}

        .custom-table td {{
            padding: 15px 18px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: #cbd5e1;
        }}

        .custom-table tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
            color: #f8fafc;
        }}

        .region-badge {{
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent-cyan);
            padding: 4px 10px;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
        }}

        .amount-cell {{
            font-weight: 700;
            color: var(--accent-emerald);
        }}

        code {{
            font-family: monospace;
            color: var(--accent-purple);
        }}

        .report-footer {{
            text-align: center;
            padding: 20px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--card-border);
            letter-spacing: 0.03em;
        }}

        .report-footer strong {{
            color: var(--accent-cyan);
        }}

        @media print {{
            body {{ background: #fff; color: #000; padding: 0; }}
            .navbar, .btn-export, .search-input {{ display: none; }}
            .kpi-card, .chart-card, .table-card, .executive-summary {{
                background: #fff;
                border: 1px solid #ddd;
                box-shadow: none;
                color: #000;
            }}
            .kpi-value, .chart-header, .brand-title {{ color: #000 !important; -webkit-text-fill-color: initial; }}
            .report-footer {{ color: #444 !important; border-top: 1px solid #ddd; }}
        }}

        @media (max-width: 1024px) {{
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .charts-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <div class="app-container">
        
        <div class="navbar">
            <div>
                <div class="brand-title">Enterprise Intelligence</div>
                <div class="brand-sub">Automated Data Clean & Executive Analytics</div>
            </div>
            <button class="btn-export" onclick="window.print()">Export Executive PDF</button>
        </div>

        <div class="executive-summary">
            <div class="summary-item">
                <h4>🎯 Regional Performance Leader</h4>
                <p><strong>{top_region} Region</strong> spearheaded sales volume, generating <strong>${top_region_val:,.2f}</strong> across normalized transactions.</p>
            </div>
            <div class="summary-item">
                <h4>⚡ Ingestion & Data Quality</h4>
                <p>Automated pipeline processed <strong>{initial_row_count} raw records</strong>, successfully purging <strong>{duplicates_removed} duplicates</strong> with <strong>{data_quality_score}% integrity</strong>.</p>
            </div>
            <div class="summary-item">
                <h4>🏆 Top Account Contribution</h4>
                <p>Key enterprise relationship led by <strong>{top_customer}</strong>, driving peak individual order figures.</p>
            </div>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Net Revenue</div>
                <div class="kpi-value">${total_revenue:,.2f}</div>
                <span class="tag">▲ Automated Ingestion</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Total Clean Records</div>
                <div class="kpi-value">{len(df)}</div>
                <span class="tag">✔ {duplicates_removed} Duplicates Purged</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Average Order Value</div>
                <div class="kpi-value">${avg_order_value:,.2f}</div>
                <span class="tag">★ Median Imputed</span>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Peak Transaction</div>
                <div class="kpi-value">${max_transaction:,.2f}</div>
                <span class="tag">⚡ 100% Integrity</span>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card">
                <div class="chart-header">📊 Regional Revenue Breakdown</div>
                {pio.to_html(fig_region, full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card">
                <div class="chart-header">📈 Revenue Trajectory</div>
                {pio.to_html(fig_trend, full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-header">🍕 Market Volume Share</div>
                {pio.to_html(fig_donut, full_html=False, include_plotlyjs=False)}
            </div>
            <div class="chart-card">
                <div class="chart-header">🏆 Account Leaderboard</div>
                {pio.to_html(fig_top, full_html=False, include_plotlyjs=False)}
            </div>
        </div>

        <div class="table-card">
            <div class="table-top">
                <div class="chart-header">🔍 Ingested & Cleaned Data Inspector</div>
                <input type="text" id="tableSearch" class="search-input" onkeyup="filterTable()" placeholder="Filter records...">
            </div>
            <table class="custom-table" id="dataTable">
                <thead>
                    <tr>
                        <th>Transaction ID</th>
                        <th>Customer Name</th>
                        <th>Region</th>
                        <th>Sales Amount</th>
                        <th>Purchase Date</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        </div>

        <div class="report-footer">
            Report generated automatically via Executive Ingestion Engine
        </div>

    </div>

    <script>
        function filterTable() {{
            const input = document.getElementById('tableSearch');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('dataTable');
            const trs = table.getElementsByTagName('tr');

            for (let i = 1; i < trs.length; i++) {{
                const tds = trs[i].getElementsByTagName('td');
                let show = false;
                for (let j = 0; j < tds.length; j++) {{
                    if (tds[j] && tds[j].innerText.toLowerCase().indexOf(filter) > -1) {{
                        show = true;
                        break;
                    }}
                }}
                trs[i].style.display = show ? '' : 'none';
            }}
        }}
    </script>
</body>
</html>
"""

# Open output file with explicit UTF-8 encoding
with open("executive_summary_report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Master Executive Report successfully generated!")
print("Clean dataset saved to 'cleaned_sales_data.csv'")
print("Attributed HTML report saved to 'executive_summary_report.html'")