import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_season_data(day_df):
  season_count_data =  day_df.groupby(by="season").agg({"cnt": ["sum"]})
  return season_count_data

def count_by_weekday_data(day_df):
    weekday_data_count = day_df.groupby(by="weekday").agg({"cnt": ["sum"]})
    return weekday_data_count

def total_workday_data(day_df):
   workday_data =  day_df.groupby(by="workday").agg({
      "cnt": "sum"
    })
   workday_data = workday_data.reset_index()
   workday_data.rename(columns={
        "cnt": "workday_sum"
    }, inplace=True)
   return workday_data

def total_holiday_data(day_df):
   holiday_data =  day_df.groupby(by="holiday").agg({
      "cnt": "sum"
    })
   holiday_data = holiday_data.reset_index()
   holiday_data.rename(columns={
        "cnt": "holiday_sum"
    }, inplace=True)
   return holiday_data

def average_order_by_season (day_df):
    avg_order_items_data = day_df.groupby("season").cnt.mean().reset_index()
    return avg_order_items_data

def average_order_by_weekday (day_df):
    avg_order_items_data = day_df.groupby("weekday").cnt.mean().reset_index()
    return avg_order_items_data

def average_order_by_workday (day_df):
    avg_order_items_data = day_df.groupby("workday").cnt.mean().reset_index()
    return avg_order_items_data

def average_order_by_holiday (day_df):
    avg_order_items_data = day_df.groupby("holiday").cnt.mean().reset_index()
    return avg_order_items_data

day_df = pd.read_csv("./dashboard/day_cleaned.csv")
hour_df = pd.read_csv("./dashboard/hour_cleaned.csv")

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = day_df['cnt'].sum()
    st.metric("Total orders", value=total_orders)

with col2:
    avg_orders = day_df['cnt'].mean()
    st.metric("Average orders", value=avg_orders)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    day_df["date"],
    day_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Best Performing Season")

fig, ax = plt.subplots(figsize=(16, 8))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

seasons_data = day_df.groupby('season')['cnt'].sum()
sns.barplot(x=seasons_data.index, y=seasons_data.values, palette=colors, ax=ax)
ax.set_ylabel(None)
ax.set_xlabel("Season", fontsize=30)
ax.set_title("Best Performing Season", loc="center", fontsize=50)
ax.set_xticks(range(len(seasons_data.index)))
ax.set_xticklabels(seasons_data.index, rotation=45)
ax.tick_params(axis='y', labelsize=35)
ax.tick_params(axis='x', labelsize=30)
st.pyplot(fig)

st.subheader("Customer Demographics")
fig, ax = plt.subplots(figsize=(20, 10))

day_df['weekday'] = day_df['weekday'].replace({0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'})

sns.barplot(
    y="cnt", 
    x="weekday",
    data=day_df.sort_values(by="cnt", ascending=False),
    palette=["#FF69B4", "#33CC33", "#6666CC", "#CC6633", "#33CCCC", "#FF9900", "#66CCCC"],
    ax=ax
)
ax.set_title("Number of Customer by Weekday", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35, rotation=45)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

st.subheader("Proportion of Customer by Workday")

fig, ax = plt.subplots(1, 2, figsize=(15, 6)) 

labels = ['Holiday', 'Working Day']  
day_df['workday'] = day_df['workday'].replace({0: 'Holiday', 1: 'Working Day'}) 
colors = ['#FF5733', '#00BFFF']

sns.barplot(x='workday', y='cnt', data=day_df, hue='workday', palette=colors, legend=False, ax=ax[0])
ax[0].set_title('Average Bike Shares on Holidays vs. Working Days') 
ax[0].set_xlabel('Day Type')
ax[0].set_ylabel('Average Shares') 

data = day_df['workday'].value_counts() 
colors = ['#00BFFF', '#FF5733']

ax[1].pie(data, labels=data.index, autopct='%1.1f%%', colors=colors, startangle=90)
ax[1].set_title('Percentage of Bike Shares on Holidays vs. Working Days') 

plt.tight_layout()
st.pyplot(fig) 

min_date_days = pd.to_datetime(day_df["date"].min()).date()
max_date_days = pd.to_datetime(day_df["date"].max()).date()

with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Bike_Share_Toronto_logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

    day_df = day_df[(day_df["date"] >= str(start_date)) & 
                    (day_df["date"] <= str(end_date))]

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3"]

st.caption("Copyright by Hisyam Fadhilah Bahar (2024)")
