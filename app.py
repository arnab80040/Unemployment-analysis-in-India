import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

df = pd.read_csv("Unemployment in India file.csv")
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df_urbanisation = df.drop_duplicates(subset=["Region", "Area"], keep="last")

df_urbanisation = df.drop_duplicates(subset=["Region", "Area"], keep="last")
df_urban = df[df["Area"] == "Urban"]
df_rural = df[df["Area"] == "Rural"]

df_high_u = df[df[" Date"] == '30-06-2020'].sort_values("Unemployment rate", ascending=False).head(5)
df_high_u["Region and Area"] = df_high_u["Region"] + "(" + df_high_u["Area"] + ")"
df_low_u = df[df[" Date"] == '30-06-2020'].sort_values("Unemployment rate", ascending=True).head(5)
df_low_u["Region and Area"] = df_low_u["Region"] + "(" + df_low_u["Area"] + ")"

df["Region and Area"] = df["Region"] + "(" + df["Area"] + ")"
df_high_e = df[df[" Date"] == '30-06-2020'].sort_values("Employed", ascending=False).head(5)
df_low_e = df[df[" Date"] == '30-06-2020'].sort_values("Employed").head(5)

df_low_l = df[df[" Date"] == '30-06-2020'].sort_values("Labour Participation Rate (%)").head(5)
df_high_l = df[df[" Date"] == '30-06-2020'].sort_values("Labour Participation Rate (%)", ascending=False).head(5)

regions = df["Region"].unique()
area = df["Area"].unique()
dates = df[" Date"].unique()

st.sidebar.title("Unemployment analysis in India")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overall analysis', 'Region and Area based comparison', 'Unemployment rate change over time')
)

data_area_wise = [["Urban", np.mean(df_urban["Unemployment rate"])], ["Rural", np.mean(df_rural["Unemployment rate"])]]
area_wise_df = pd.DataFrame(data_area_wise, columns=["Area", "Unemployment rate"])


def get_unemp_rate(region, area, date):
    return float(df[(df["Area"] == area) & (df["Region"] == region) & (df[" Date"] == date)]["Unemployment rate"])


def get_employed(region, area, date):
    return float(df[(df["Area"] == area) & (df["Region"] == region) & (df[" Date"] == date)]["Employed"])


def get_labour_part_rate(region, area, date):
    return float(df[(df["Area"] == area) & (df["Region"] == region) & (df[" Date"] == date)]["Labour Participation Rate (%)"])

if user_menu == 'Overall analysis':
    st.markdown("<h1 style='text-align: center; color: grey;'>Average unemployment rate</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.header(str(round(np.mean(df["Unemployment rate"]), 2)) +"%")

    with col3:
        st.write(' ')

    st.title("\n\n\n\n\n")

    st.title("Areas in India based on urbanisation")
    fig4 = px.pie(df_urbanisation, names=df_urbanisation["Area"].unique(), values=[df_urbanisation["Area"].value_counts()[0], df_urbanisation["Area"].value_counts()[1]])
    st.plotly_chart(fig4)


    st.title("Area wise average unemployment rate in India from 31-05-2019 to 30-06-2020")
    fig1 = px.bar(area_wise_df, y = "Area", x = area_wise_df["Unemployment rate"], orientation="h")
    st.plotly_chart(fig1)

    st.title("Regions along with areas with highest unemployment rate")
    fig2 = px.bar(df_high_u, x = "Region and Area", y = "Unemployment rate")
    st.plotly_chart(fig2)

    st.title("Regions along with areas with lowest unemployment rate")
    fig3 = px.bar(df_low_u, x = "Region and Area", y = "Unemployment rate")
    st.plotly_chart(fig3)

    st.title("Highest employed per region and area as on 30-06-2020")
    fig5 = px.bar(df_high_e, x = "Region and Area", y = "Employed")
    st.plotly_chart(fig5)

    st.title("Lowest employed per region and area as on 30-06-2020")
    fig6 = px.bar(df_low_e, x="Region and Area", y="Employed")
    st.plotly_chart(fig6)

    st.title("Highest Labour participation rate per region and area as on 30-06-2020")
    fig7 = px.bar(df_high_l, x="Region and Area", y="Labour Participation Rate (%)")
    st.plotly_chart(fig7)

    st.title("Lowest Labour participation rate per region and area as on 30-06-2020")
    fig7 = px.bar(df_low_l, x="Region and Area", y="Labour Participation Rate (%)")
    st.plotly_chart(fig7)

    st.title("Peak unemployment rate along with region, area and date")
    st.table(df[df["Unemployment rate"] == np.max(df["Unemployment rate"])][["Region and Area", " Date", "Unemployment rate"]])

    st.title("Trough unemployment rate along with region, area and date")
    st.table(df[df["Unemployment rate"] == np.min(df["Unemployment rate"])][["Region and Area", " Date", "Unemployment rate"]])

elif user_menu == "Unemployment rate change over time":
    selected_region = st.sidebar.selectbox("Select region", regions)

    selected_area = st.sidebar.selectbox("Select area", area)

    try:
        def get_dates_for_graph(region, dev_status):
            return df[(df["Region"] == region) & (df["Area"] == dev_status)][" Date"]
        def get_unemp_rate_for_graph(region, dev_status):
            return df[(df["Region"] == region) & (df["Area"] == dev_status)]["Unemployment rate"]
        fig8 = px.line(df, y = get_unemp_rate_for_graph(selected_region, selected_area), x = get_dates_for_graph(selected_region, selected_area), labels={"x":"Date of record", "y":"Unemployment rate(%)"})
        st.plotly_chart(fig8)
    except ValueError:
        st.write("No records found for the given input")

elif user_menu == "Region and Area based comparison":
    selected_region1 = st.sidebar.selectbox("Select region 1", regions)
    selected_area1 = st.sidebar.selectbox("Select area 1", area)
    selected_region2 = st.sidebar.selectbox("Select region 2", regions)
    selected_area2 = st.sidebar.selectbox("Select area 2", area)
    selected_date = st.sidebar.selectbox("Select date of record", dates)
    try:
        categories = ["Unemployment rate(%)", "Employed*100000", "Labour participation rate(%)"]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[get_unemp_rate(selected_region1, selected_area1, selected_date), get_employed(selected_region1, selected_area1, selected_date)/100000, get_labour_part_rate(selected_region1, selected_area1, selected_date)],
            theta=categories,
            fill='toself',
            name = str(selected_region1) +"(" +str(selected_area1) + ")"
        ))
        fig.add_trace(go.Scatterpolar(
            r=[get_unemp_rate(selected_region2, selected_area2, selected_date), get_employed(selected_region2, selected_area2, selected_date)/100000, get_labour_part_rate(selected_region2, selected_area2, selected_date)],
            theta=categories,
            fill='toself',
            name=str(selected_region2) + "(" + str(selected_area2) + ")"
        ))
        st.plotly_chart(fig)
    except:
        st.write("Some records not available for given input")