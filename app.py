import streamlit as st
from google.cloud import bigquery
from datetime import date, datetime

# Page config
st.set_page_config(page_title="CurryPizzaHouse Tool")

# BigQuery client
client = bigquery.Client()
TABLE_ID = "repors-dashboards.dashboard_new.store_prices"

# Title
st.title("CurryPizzaHouse - Manual Store/Price Entry")

# Store dropdown values
STORE_LIST = [
    "Lathrop",
    "Clark County #3 (Clark County, NV)",
    "Ashburn",
    "Celina",
    "Summerlin",
    "Walnut Creek",
    "Bombay",
    "Fremont",
    "Redwood City",
    "Union Ave",
    "Roseville",
    "Dublin",
    "San Ramon",
    "Palo Alto",
    "Warm Springs",
    "Cupertino",
    "Milpitas",
    "Cedar Park",
    "Evergreen",
    "Natomas",
    "Manteca",
    "Frisco",
    "Berkeley",
    "Folsom",
    "Sunnyvale",
    "Lake Forest",
    "San Jose (Capitol Ave)",
    "Las Vegas",
    "Kent",
    "Cypress",
    "Hillsboro",
    "Pleasanton",
    "South San Francisco",
    "Tustin",
    "Foster City",
    "Little Elm",
    "Elk Grove",
    "San Mateo",
    "Plano",
    "Katy",
    "Bee Cave",
    "Portland",
    "Alpharetta",
    "Dover",
    "Fishers",
    "Mira Mesa",
    "Irving",
    "Round Rock",
    "Hayward",
    "Mountain House"
]

# Platform list
PLATFORM_LIST = [
    "Toast",
    "DoorDash",
    "OLO",
    "UberEats",
    "GrubHub",
    "EzCaters",
    "SnackPass",
    "Forkable",
    "Chowmill",
    "Waiters",
    "Foodja"
]
# Inputs
store = st.selectbox("Store Name", STORE_LIST)
platform = st.selectbox("Platform Name", PLATFORM_LIST)
price = st.number_input("Price", min_value=1, step=1)

start_date = st.date_input("Start Date", value=date.today())
end_date = st.date_input("End Date", value=date.today())

# Submit button
if st.button("Submit"):

    # Basic validations
    if not platform.strip():
        st.error("Platform name is required")
    elif end_date < start_date:
        st.error("End date cannot be earlier than start date")
    else:
        # Check for existing entry
        check_query = """
        SELECT COUNT(*) AS record_count
        FROM `repors-dashboards.dashboard_new.store_prices`
        WHERE store = @store
          AND location = @location
          AND start_date = @start_date
          AND end_date = @end_date
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("store", "STRING", store),
                bigquery.ScalarQueryParameter("location", "STRING", platform),
                bigquery.ScalarQueryParameter("start_date", "DATE", start_date),
                bigquery.ScalarQueryParameter("end_date", "DATE", end_date),
            ]
        )

        result = client.query(check_query, job_config=job_config).result()
        exists = next(result).record_count > 0

        if exists:
            st.warning("⚠️ Entry already exists for this Store, Platform, and Date range")
        else:
            # Insert row (DATE-only for start_date and end_date)
            rows = [{
                "store": store,
                "location": platform,
                "price": price,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "created_at": datetime.utcnow().isoformat()
            }]

            errors = client.insert_rows_json(TABLE_ID, rows)

            if errors:
                st.error(errors)
            else:
                st.success("Saved successfully ✅")
