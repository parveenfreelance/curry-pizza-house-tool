import streamlit as st
from google.cloud import bigquery
from datetime import date, datetime

st.set_page_config(page_title="Store Tool")

client = bigquery.Client()
TABLE_ID = "repors-dashboards.dashboard_new.store_prices"

st.title("Internal Store Entry")

store = st.text_input("Store")
location = st.text_input("Location")
price = st.number_input("Price", min_value=0.0)
order_date = st.date_input("Date", value=date.today())

if st.button("Submit"):
    if not store or not location:
        st.error("Store and Location required")
    else:
        rows = [{
            "store": store,
            "location": location,
            "price": price,
            "order_date": order_date.isoformat(),
            "created_at": datetime.utcnow().isoformat()
        }]
        errors = client.insert_rows_json(TABLE_ID, rows)
        if errors:
            st.error(errors)
        else:
            st.success("Saved successfully ✅")
