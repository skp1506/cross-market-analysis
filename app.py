import streamlit as st
import mysql.connector
import pandas as pd



# PAGE CONFIG


st.set_page_config(
    page_title="Cross-Market Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)



# CUSTOM CSS


st.markdown("""
<style>

[data-testid="stSidebar"] {
    background-color: #f1f3f8;
}

[data-testid="stSidebar"] .block-container {
    padding-top: 22px;
    padding-left: 18px;
    padding-right: 12px;
}

[data-testid="stSidebar"] * {
    color: #333333 !important;
}

.main-title {
    font-size: 28px;
    font-weight: 700;
    color: #30323d;
}

.subtitle {
    font-size: 11px;
    color: #888888;
    margin-bottom: 18px;
}

.small-text {
    font-size: 11px;
    color: #777777;
}

[data-testid="stMetricLabel"] {
    font-size: 11px !important;
}

[data-testid="stMetricValue"] {
    font-size: 21px !important;
}

div[data-baseweb="select"] {
    font-size: 12px;
}

.stButton button {
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)



# MYSQL CONNECTION


import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# SIDEBAR NAVIGATION


st.sidebar.markdown(
    """
    <div style="
        font-size:16px;
        font-weight:700;
        margin-bottom:8px;
    ">
        📌 Navigation
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div style="
        font-size:10px;
        color:#666666;
        margin-bottom:4px;
    ">
        Go to
    </div>
    """,
    unsafe_allow_html=True
)

page = st.sidebar.radio(
    "",
    [
        "🔴 Market Overview",
        "⚪ SQL Query Runner",
        "🟠 Top 5 Crypto Analysis"
    ],
    index=0,
    label_visibility="collapsed"
)

# PAGE 1 - MARKET OVERVIEW


if page == "🔴 Market Overview":

    # TITLE
    

    st.markdown(
        '<div class="main-title">📊 Cross-Market Overview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Crypto • Oil • Stock Market | SQL-powered analytics'
        '</div>',
        unsafe_allow_html=True
    )


    # 
    # DATE FILTER
    # 

    col1, col2 = st.columns(2)

    with col1:

        st.caption("Start Date")

        start_date = st.date_input(
            "Start Date",
            value=pd.Timestamp("2024-01-01").date(),
            key="market_start",
            label_visibility="collapsed"
        )

    with col2:

        st.caption("End Date")

        end_date = st.date_input(
            "End Date",
            value=pd.Timestamp("2026-01-01").date(),
            key="market_end",
            label_visibility="collapsed"
        )


    if start_date > end_date:

        st.error("Start Date must be before End Date.")
        st.stop()


    
    # BITCOIN AVERAGE
    

    bitcoin_query = """
    SELECT AVG(price_usd) AS average_price
    FROM crypto_prices
    WHERE coin_id = 'bitcoin'
    AND date BETWEEN %s AND %s
    """

    bitcoin_df = pd.read_sql(
        bitcoin_query,
        conn,
        params=(start_date, end_date)
    )

    bitcoin_avg = bitcoin_df["average_price"].iloc[0]

    # OIL AVERAGE
    

    oil_query = """
    SELECT AVG(price_usd) AS average_price
    FROM oil_prices
    WHERE date BETWEEN %s AND %s
    """

    oil_df = pd.read_sql(
        oil_query,
        conn,
        params=(start_date, end_date)
    )

    oil_avg = oil_df["average_price"].iloc[0]



    # S&P 500 AVERAGE
    

    sp_query = """
    SELECT AVG(close) AS average_price
    FROM stock_prices
    WHERE ticker = '^GSPC'
    AND date BETWEEN %s AND %s
    """

    sp_df = pd.read_sql(
        sp_query,
        conn,
        params=(start_date, end_date)
    )

    sp_avg = sp_df["average_price"].iloc[0]


    
    # NIFTY AVERAGE
    
    nifty_query = """
    SELECT AVG(close) AS average_price
    FROM stock_prices
    WHERE ticker = '^NSEI'
    AND date BETWEEN %s AND %s
    """

    nifty_df = pd.read_sql(
        nifty_query,
        conn,
        params=(start_date, end_date)
    )

    nifty_avg = nifty_df["average_price"].iloc[0]


    
    # METRICS
    
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "₿ Bitcoin Avg ($)",
            "No Data"
            if pd.isna(bitcoin_avg)
            else f"{bitcoin_avg:,.2f}"
        )

    with c2:

        st.metric(
            "🛢️ Oil Avg ($)",
            "No Data"
            if pd.isna(oil_avg)
            else f"{oil_avg:,.2f}"
        )

    with c3:

        st.metric(
            "📈 S&P 500 Avg",
            "No Data"
            if pd.isna(sp_avg)
            else f"{sp_avg:,.2f}"
        )

    with c4:

        st.metric(
            "🇮🇳 NIFTY Avg",
            "No Data"
            if pd.isna(nifty_avg)
            else f"{nifty_avg:,.2f}"
        )


    
    # DAILY MARKET SNAPSHOT
    
    st.markdown("---")

    st.subheader("📋 Daily Market Snapshot")


    snapshot_query = """
    SELECT
        c.date,
        c.price_usd AS bitcoin_price,
        o.price_usd AS oil_price,
        sp.close AS sp500,
        nf.close AS nifty

    FROM crypto_prices c

    LEFT JOIN oil_prices o
        ON c.date = o.date

    LEFT JOIN stock_prices sp
        ON c.date = sp.date
        AND sp.ticker = '^GSPC'

    LEFT JOIN stock_prices nf
        ON c.date = nf.date
        AND nf.ticker = '^NSEI'

    WHERE c.coin_id = 'bitcoin'

    AND c.date BETWEEN %s AND %s

    ORDER BY c.date DESC
    """

    snapshot_df = pd.read_sql(
        snapshot_query,
        conn,
        params=(start_date, end_date)
    )


    if snapshot_df.empty:

        st.warning("No data available.")

    else:

        snapshot_df["date"] = pd.to_datetime(
            snapshot_df["date"]
        ).dt.strftime("%Y-%m-%d")

        st.dataframe(
            snapshot_df,
            use_container_width=True,
            hide_index=True
        )



# PAGE 2 - SQL QUERY RUNNER

elif page == "⚪ SQL Query Runner":

    st.markdown(
        '<div class="main-title">🔎 SQL Query Runner</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Predefined analytical SQL queries'
        '</div>',
        unsafe_allow_html=True
    )


    # 30 QUERY NAMES
    
    query_names = [

        "Top 3 Cryptocurrencies by Market Cap",

        "Circulating Supply Above 90%",

        "Coins Within 10% of ATH",

        "Average Market Cap Rank for Volume > $1B",

        "Most Recently Updated Coin",

        "Highest Bitcoin Price in Last 365 Days",

        "Average Ethereum Price in Last 1 Year",

        "Bitcoin Price Trend - January 2025",

        "Coin with Highest Average Price",

        "Bitcoin Percentage Change",

        "Highest Oil Price in Last 5 Years",

        "Average Oil Price Per Year",

        "Oil Price During COVID Crash",

        "Lowest Oil Price in Last 10 Years",

        "Oil Volatility Per Year",

        "S&P 500 Stock Prices",

        "Highest NASDAQ Closing Price",

        "Top 5 S&P 500 Price Differences",

        "Monthly Average Closing Price",

        "Average NSEI Volume in 2024",

        "Bitcoin vs Oil Average Price - 2025",

        "Bitcoin vs S&P 500 Correlation",

        "Ethereum vs NASDAQ - 2025",

        "Oil Price Spikes vs Bitcoin",

        "Top 3 Crypto vs NIFTY",

        "S&P 500 vs Oil",

        "Bitcoin vs Crude Oil Correlation",

        "NASDAQ vs Ethereum",

        "Top 3 Crypto vs Stock Indices",

        "Stock + Oil + Bitcoin Comparison"
    ]


    # QUERY SELECT
    
    st.markdown("📌 **Select a Query**")

    selected_query = st.selectbox(
        "Select Query",
        query_names,
        label_visibility="collapsed"
    )

    query_number = query_names.index(selected_query) + 1

    # SQL QUERIES
   
    queries = {

        1: """
SELECT name, market_cap
FROM cryptocurrencies
ORDER BY market_cap DESC
LIMIT 3;
""",

        2: """
SELECT
    name,
    symbol,
    circulating_supply,
    total_supply
FROM cryptocurrencies
WHERE total_supply IS NOT NULL
AND circulating_supply > 0.90 * total_supply;
""",

        3: """
SELECT
    name,
    symbol,
    current_price,
    ath
FROM cryptocurrencies
WHERE ath IS NOT NULL
AND current_price >= 0.90 * ath;
""",

        4: """
SELECT
    AVG(market_cap_rank) AS average_market_cap_rank
FROM cryptocurrencies
WHERE total_volume > 1000000000;
""",

        5: """
SELECT
    name,
    symbol,
    date
FROM cryptocurrencies
ORDER BY date DESC
LIMIT 1;
""",

        6: """
SELECT
    MAX(price_usd) AS highest_bitcoin_price
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND date >= CURDATE() - INTERVAL 365 DAY;
""",

        7: """
SELECT
    AVG(price_usd) AS average_ethereum_price
FROM crypto_prices
WHERE coin_id = 'ethereum'
AND date >= CURDATE() - INTERVAL 1 YEAR;
""",

        8: """
SELECT
    date,
    price_usd
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND date BETWEEN '2025-01-01' AND '2025-01-31'
ORDER BY date;
""",

        9: """
SELECT
    coin_id,
    AVG(price_usd) AS average_price
FROM crypto_prices
GROUP BY coin_id
ORDER BY average_price DESC
LIMIT 1;
""",

        10: """
SELECT
    MIN(price_usd) AS minimum_price,
    MAX(price_usd) AS maximum_price,
    AVG(price_usd) AS average_price
FROM crypto_prices
WHERE coin_id = 'bitcoin'
AND date BETWEEN '2025-01-01' AND '2025-12-31';
""",

        11: """
SELECT
    MAX(price_usd) AS highest_oil_price
FROM oil_prices
WHERE date >= CURDATE() - INTERVAL 5 YEAR;
""",

        12: """
SELECT
    YEAR(date) AS year,
    AVG(price_usd) AS average_oil_price
FROM oil_prices
GROUP BY YEAR(date)
ORDER BY year;
""",

        13: """
SELECT
    date,
    price_usd
FROM oil_prices
WHERE date BETWEEN '2020-03-01' AND '2020-04-30'
ORDER BY date;
""",

        14: """
SELECT
    MIN(price_usd) AS lowest_oil_price
FROM oil_prices
WHERE date >= CURDATE() - INTERVAL 10 YEAR;
""",

        15: """
SELECT
    YEAR(date) AS year,
    MAX(price_usd) - MIN(price_usd) AS volatility
FROM oil_prices
GROUP BY YEAR(date)
ORDER BY year;
""",

        16: """
SELECT *
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY date;
""",

        17: """
SELECT
    MAX(close) AS highest_nasdaq_closing_price
FROM stock_prices
WHERE ticker = '^IXIC';
""",

        18: """
SELECT
    date,
    high,
    low,
    high - low AS price_difference
FROM stock_prices
WHERE ticker = '^GSPC'
ORDER BY price_difference DESC
LIMIT 5;
""",

        19: """
SELECT
    ticker,
    YEAR(date) AS year,
    MONTH(date) AS month,
    AVG(close) AS average_closing_price
FROM stock_prices
GROUP BY
    ticker,
    YEAR(date),
    MONTH(date)
ORDER BY year, month;
""",

        20: """
SELECT
    AVG(volume) AS average_nsei_volume
FROM stock_prices
WHERE ticker = '^NSEI'
AND date BETWEEN '2024-01-01' AND '2024-12-31';
""",

        21: """
SELECT
    AVG(c.price_usd) AS bitcoin_average_price,
    AVG(o.price_usd) AS oil_average_price
FROM crypto_prices c
JOIN oil_prices o
    ON c.date = o.date
WHERE c.coin_id = 'bitcoin'
AND c.date BETWEEN '2025-01-01' AND '2025-12-31';
""",

        22: """
SELECT
    COUNT(*) AS matching_days,
    AVG(c.price_usd) AS average_bitcoin,
    AVG(s.close) AS average_sp500
FROM crypto_prices c
JOIN stock_prices s
    ON c.date = s.date
WHERE c.coin_id = 'bitcoin'
AND s.ticker = '^GSPC'
AND c.date BETWEEN '2025-01-01' AND '2025-12-31';
""",

        23: """
SELECT
    c.date,
    c.price_usd AS ethereum_price,
    s.close AS nasdaq_close
FROM crypto_prices c
JOIN stock_prices s
    ON c.date = s.date
WHERE c.coin_id = 'ethereum'
AND s.ticker = '^IXIC'
AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY c.date;
""",

        24: """
SELECT
    o.date,
    o.price_usd AS oil_price,
    c.price_usd AS bitcoin_price
FROM oil_prices o
JOIN crypto_prices c
    ON o.date = c.date
WHERE c.coin_id = 'bitcoin'
ORDER BY o.date;
""",

        26: """
SELECT
    s.date,
    s.close AS sp500_close,
    o.price_usd AS oil_price
FROM stock_prices s
JOIN oil_prices o
    ON s.date = o.date
WHERE s.ticker = '^GSPC'
ORDER BY s.date;
""",

        27: """
SELECT
    COUNT(*) AS matching_days,
    AVG(c.price_usd) AS average_bitcoin,
    AVG(o.price_usd) AS average_oil
FROM crypto_prices c
JOIN oil_prices o
    ON c.date = o.date
WHERE c.coin_id = 'bitcoin';
""",

        28: """
SELECT
    c.date,
    c.price_usd AS ethereum_price,
    s.close AS nasdaq_close
FROM crypto_prices c
JOIN stock_prices s
    ON c.date = s.date
WHERE c.coin_id = 'ethereum'
AND s.ticker = '^IXIC'
ORDER BY c.date;
""",

        30: """
SELECT
    c.date,
    c.price_usd AS bitcoin_price,
    o.price_usd AS oil_price,
    s.close AS sp500_close
FROM crypto_prices c
JOIN oil_prices o
    ON c.date = o.date
JOIN stock_prices s
    ON c.date = s.date
WHERE c.coin_id = 'bitcoin'
AND s.ticker = '^GSPC'
ORDER BY c.date;
"""
    }


   
    # RUN QUERY
    
    if st.button("▶ Run Query"):

        try:

           
            # Q25
           

            if query_number == 25:

                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id
                    FROM cryptocurrencies
                    ORDER BY market_cap_rank
                    LIMIT 3
                """)

                top3 = cursor.fetchall()

                cursor.close()

                ids = [x[0] for x in top3]

                placeholders = ",".join(
                    ["%s"] * len(ids)
                )

                sql = f"""
SELECT
    c.date,
    c.coin_id,
    c.price_usd AS crypto_price,
    s.close AS nifty_close
FROM crypto_prices c
JOIN stock_prices s
    ON c.date = s.date
WHERE s.ticker = '^NSEI'
AND c.coin_id IN ({placeholders})
AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY c.date, c.coin_id;
"""

                result_df = pd.read_sql(
                    sql,
                    conn,
                    params=ids
                )


        
            # Q29

            elif query_number == 29:

                cursor = conn.cursor()

                cursor.execute("""
                    SELECT id
                    FROM cryptocurrencies
                    ORDER BY market_cap_rank
                    LIMIT 3
                """)

                top3 = cursor.fetchall()

                cursor.close()

                ids = [x[0] for x in top3]

                placeholders = ",".join(
                    ["%s"] * len(ids)
                )

                sql = f"""
SELECT
    c.date,
    c.coin_id,
    c.price_usd AS crypto_price,
    s.ticker,
    s.close AS stock_close
FROM crypto_prices c
JOIN stock_prices s
    ON c.date = s.date
WHERE c.coin_id IN ({placeholders})
AND s.ticker IN ('^GSPC', '^IXIC', '^NSEI')
AND c.date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY c.date, c.coin_id, s.ticker;
"""

                result_df = pd.read_sql(
                    sql,
                    conn,
                    params=ids
                )

            # NORMAL QUERIES
            
            else:

                sql = queries[query_number]

                result_df = pd.read_sql(
                    sql,
                    conn
                )


            
            # SUCCESS
            
            st.success(
                "Query executed successfully"
            )

            # RESULT
            
            st.dataframe(
                result_df,
                use_container_width=True,
                hide_index=True
            )


            # INFO
            

            st.info(
                "💡 These queries are executed directly on the SQL database."
            )


        except Exception as e:

            st.error(
                f"❌ Query Error: {e}"
            )



# PAGE 3 - TOP 5 CRYPTO ANALYSIS

elif page == "🟠 Top 5 Crypto Analysis":

    st.markdown(
        '<div class="main-title">🪙 Top 5 Crypto Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Daily price analysis for top cryptocurrencies'
        '</div>',
        unsafe_allow_html=True
    )


    
    # GET TOP 5 CRYPTO
    
    top5_query = """
    SELECT
        id,
        name,
        symbol,
        market_cap_rank
    FROM cryptocurrencies
    WHERE market_cap_rank IS NOT NULL
    ORDER BY market_cap_rank
    LIMIT 5;
    """

    top5_df = pd.read_sql(
        top5_query,
        conn
    )


    if top5_df.empty:

        st.error("No cryptocurrency data found.")
        st.stop()


    
    # CRYPTO SELECTION
    
    crypto_ids = top5_df["id"].tolist()

    selected_crypto = st.selectbox(
        "Select a Cryptocurrency",
        crypto_ids
    )


    # DATE RANGE
    
    date_query = """
    SELECT
        MIN(date) AS min_date,
        MAX(date) AS max_date
    FROM crypto_prices
    WHERE coin_id = %s;
    """

    date_df = pd.read_sql(
        date_query,
        conn,
        params=(selected_crypto,)
    )


    min_date = pd.to_datetime(
        date_df["min_date"].iloc[0]
    ).date()

    max_date = pd.to_datetime(
        date_df["max_date"].iloc[0]
    ).date()


    # Reference-style defaults
    default_start = max(
        min_date,
        pd.Timestamp("2024-01-01").date()
    )

    default_end = max_date


    col1, col2 = st.columns(2)

    with col1:

        st.caption("Start Date")

        crypto_start = st.date_input(
            "Start Date",
            value=default_start,
            min_value=min_date,
            max_value=max_date,
            key="crypto_start",
            label_visibility="collapsed"
        )

    with col2:

        st.caption("End Date")

        crypto_end = st.date_input(
            "End Date",
            value=default_end,
            min_value=min_date,
            max_value=max_date,
            key="crypto_end",
            label_visibility="collapsed"
        )


    if crypto_start > crypto_end:

        st.error("Start Date must be before End Date.")
        st.stop()


    # -----------------------------------------------------
    # PRICE DATA
    # -----------------------------------------------------

    crypto_query = """
    SELECT
        date,
        price_usd
    FROM crypto_prices
    WHERE coin_id = %s
    AND date BETWEEN %s AND %s
    ORDER BY date;
    """

    crypto_df = pd.read_sql(
        crypto_query,
        conn,
        params=(
            selected_crypto,
            crypto_start,
            crypto_end
        )
    )

    # PRICE TREND
    
    st.subheader(
        f"📈 {selected_crypto.upper()} Price Trend"
    )


    if crypto_df.empty:

        st.warning(
            "No price data available for the selected dates."
        )

    else:

        crypto_df["date"] = pd.to_datetime(
            crypto_df["date"]
        )

        chart_df = crypto_df.set_index(
            "date"
        )

        st.line_chart(
            chart_df["price_usd"],
            use_container_width=True
        )


        # DAILY PRICE TABLE

        display_df = crypto_df.copy()

        display_df["date"] = display_df["date"].dt.strftime(
            "%Y-%m-%d"
        )

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )