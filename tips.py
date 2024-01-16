from datetime import datetime

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

import streamlit as st


def main():
    path = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
    tips = pd.read_csv(path)

    start_date = datetime(2023, 1, 1, 0, 0, 0)
    end_date = datetime(2023, 1, 31, 23, 59, 59)
    tips["time_order"] = generate_random_dates(start_date, end_date, tips.index.size)

    start, end = get_user_date(start_date, end_date)
    filtered_tips = filter_data(tips, start, end, "time_order")

    graphs = get_graph(filtered_tips)

    choise = st.sidebar.selectbox("Show graph", options=graphs.keys())

    st.write(
        f"""
        ## Total bill distribution from {start:%d/%m/%Y} to {end:%d/%m/%Y}
             """
    )

    st.write(
        f"""
             ## {choise}
             """
    )
    st.pyplot(graphs[choise])


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


def get_graph(data):
    total_bill = plt.figure()
    sns.histplot(data=data, x="total_bill", bins=range(0, 51, 2))

    tips_graph = plt.figure()
    sns.lineplot(data=data, x="time_order", y="tip").set(xlabel="Date", ylabel="Tip")
    tips_graph.tight_layout()
    tips_graph.autofmt_xdate(rotation=30)

    total_bill_vs_tips = plt.figure()
    sns.scatterplot(data=data, x="total_bill", y="tip", color="#A242DF").set(
        ylabel="Tip", xlabel="Total Bill"
    )

    total_bill_vs_tips_gender = plt.figure()
    sns.scatterplot(data=data, x="total_bill", y="tip", hue="sex").set(
        ylabel="Tip", xlabel="Total Bill"
    )

    tips_by_day, axes = plt.subplots(2, 1, figsize=(12, 6))
    sns.histplot(data=data[data["time"] == "Lunch"], x="tip", ax=axes[0]).set(
        title="Lunch"
    )
    sns.histplot(data=data[data["time"] == "Dinner"], x="tip", ax=axes[1]).set(
        title="Dinner"
    )
    tips_by_day.tight_layout()

    tips_vs_day_gender = plt.figure()
    sns.scatterplot(data=data, x="tip", y="day", hue="sex").set(
        ylabel="Day", xlabel="Tip"
    )

    bill_vs_day_and_time = plt.figure()
    sns.boxplot(data=data, x="day", y="total_bill", hue="time").set(
        ylabel="Total Bill", xlabel="Time"
    )

    graph_title = [
        "Total Bill",
        "Tips",
        "Total Bill vs. Tips",
        "Total Bill vs. Tips by Gender",
        "Tips vs. Day of the Week by Gender",
        "Total Bill by Day of the Week and Day Time",
        "Tips by Day Time",
    ]
    graph = [
        total_bill,
        tips_graph,
        total_bill_vs_tips,
        total_bill_vs_tips_gender,
        tips_vs_day_gender,
        bill_vs_day_and_time,
        tips_by_day,
    ]

    return dict(zip(graph_title, graph))


if __name__ == "__main__":
    main()
