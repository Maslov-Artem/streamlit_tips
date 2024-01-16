from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px

import streamlit as st


def main():
    path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    tips = pd.read_csv(path)

    start_date = datetime(2023, 1, 1, 0, 0, 0)
    end_date = datetime(2023, 1, 31, 23, 59, 59)
    tips["time_order"] = generate_random_dates(start_date, end_date, tips.index.size)

    start, end = get_user_date(start_date, end_date)
    filtered_tips = filter_data(tips, start, end, "time_order")

    graphs = [
        "Total Bill",
        "Tips",
        "Total Bill vs. Tips",
        "Total Bill vs. Tips by Gender",
        "Tips vs. Day of the Week by Gender",
        "Total Bill by Day of the Week and Day Time",
        "Tips by Day Time",
    ]

    st.write(
        f"""
        ## Total bill distribution from {start:%d/%m/%Y} to {end:%d/%m/%Y}
             """
    )

    choice = st.sidebar.selectbox("Show graph", graphs)

    st.write(
        f"""
             ## {choice}
             """
    )
    display_graph(filtered_tips, choice)


def generate_random_dates(start_date, end_date, k):
    date_range = (end_date - start_date).total_seconds()
    random_seconds = np.random.randint(date_range, size=k)
    random_dates = pd.to_datetime(start_date) + pd.to_timedelta(
        random_seconds, unit="sec"
    )
    return random_dates


def get_user_date(start_date, end_date):
    start = st.sidebar.slider("start date", start_date, end_date, value=start_date)
    if start == end_date:
        st.sidebar.write("Move start date to the earlier date to choose range")
        end = start
    else:
        end = st.sidebar.slider("end date", start, end_date, value=end_date)
    return start, end


def filter_data(data, start_date, end_date, column_name):
    return data[(data[column_name] >= start_date) & (data[column_name] <= end_date)]


def display_graph(data, choice):
    if choice == "Total Bill":
        fig = px.histogram(
            data_frame=data,
            x="total_bill",
            nbins=20,
            barmode="overlay",
            labels={"total_bill": "Total Bill"},
        )
        fig.update_layout(yaxis_title="Count")
        fig.update_traces(marker_line_width=1, marker_line_color="black")
        st.plotly_chart(fig)

    elif choice == "Tips":
        st.line_chart(data=data, x="time_order", y="tip")

    elif choice == "Total Bill vs. Tips":
        st.scatter_chart(data=data, x="total_bill", y="tip")

    elif choice == "Total Bill vs. Tips by Gender":
        fig = px.scatter(data_frame=data, x="total_bill", y="tip", color="sex")
        st.plotly_chart(fig)

    elif choice == "Tips vs. Day of the Week by Gender":
        fig = px.histogram(
            data_frame=data[data["time"] == "Lunch"],
            x="tip",
            nbins=7,
            labels={"tip": "Tip"},
            title="Lunch",
        )
        fig.update_traces(marker_line_width=1, marker_line_color="black")
        fig.update_layout(yaxis_title="Count")
        st.plotly_chart(fig)
        fig = px.histogram(
            data_frame=data[data["time"] == "Dinner"],
            labels={"tip": "Tip"},
            x="tip",
            nbins=7,
            title="Dinner",
        )
        fig.update_layout(yaxis_title="Count")
        fig.update_traces(marker_line_width=1, marker_line_color="black")
        st.plotly_chart(fig)

    elif choice == "Total Bill by Day of the Week and Day Time":
        fig = px.scatter(data_frame=data, x="tip", y="day", color="sex")
        st.plotly_chart(fig)

    elif choice == "Tips by Day Time":
        fig = px.box(data_frame=data, x="day", y="total_bill", color="time")
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
