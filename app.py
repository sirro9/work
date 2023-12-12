import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title='My Visualization Webpage')

st.title('Los Angeles Crime Data Visualization Analysis (2020-Present)')
st.markdown('---')
st.write("Los Angeles, located in the southwest of California, USA, is the second-largest city in the United States and the largest city in the western United States. It is often referred to as the 'City of Angels'. "
        "Los Angeles covers an area of about 1,215 square kilometers, with a city center located at 34°03′ north latitude and 118°15′ west longitude. The city has a population of over 4 million, making it a truly bustling metropolis.")
st.write("Although Los Angeles is a prosperous city known as the City of Angels, its annual crime rate remains high in the United States. "
         "With such a high number of crimes in Los Angeles, is there any way to reduce the crime rate? Let's explore together with this project!(✪ω✪)(ಥ_ಥ) ᕦ(･ㅂ･)ᕤ")
st.markdown('---')

tab1, tab2, tab3 = st.tabs(['Crime location distribution', 'Victim bias research', 'Summary and recommendations.'])



with st.sidebar:
    st.title('Welcome to my visualization webpage!')
    st.markdown('---')
    st.markdown('The volume of the Los Angeles crime dataset from 2020 until now was too large, with a total of over 830,000 records. '
                'Therefore, I processed the original dataset through data cleaning and sampling to obtain a dataset of 10,000 records for the visualization study. '
                'This webpage is mainly divided into three modules:\n- Visualizing the crime map of Los Angeles and the distribution of crime areas, '
                'exploring the high incidence areas of crime in Los Angeles.\n- Visualizing the age and gender distribution of victims, as well as the criminal modus operandi, '
                'can help explore whether there are certain reasons that make some people more vulnerable to crime.\n- Summary and recommendations.')


with tab1:
    st.write("First, the processed dataset can be directly plotted on a map as shown below. Click the 'Open map' button to view the crime map.")

    df = pd.read_csv('10000_data.csv')
    a = st.button('Open map')
    if a:
        st.map(df, size=10)
        st.write("By zooming in on the map, it can be seen that crime events in Los Angeles are mainly concentrated in the downtown area,"
                 " which means that being in the downtown area makes one more vulnerable to crime.")

    st.write("Next, we associate the victim age data to view the distribution of all crimes across the 21 administrative districts in Los Angeles. "
             "You can adjust the age range to view the number of crimes in different districts."
             "Select or remove different administrative districts for better comparison of the number of crime events.")

    df = pd.read_csv('10000_data.csv')

    crim = df['AREA NAME'].unique().tolist()
    age = df['Vict Age'].unique().tolist()

    age_selection = st.slider('Age:',
                              min_value=min(age),
                              max_value=max(age),
                              value=(min(age), max(age)))

    department_selection = st.multiselect('Management area:',
                                          crim,
                                          default=crim)

    # 根据选择过滤数据
    mask = (df['Vict Age'].between(*age_selection)) & (df['AREA NAME'].isin(department_selection))
    number_of_result = df[mask].shape[0]

    # 根据筛选条件, 得到有效数据
    st.markdown(f'*Effective data: {number_of_result}*')

    # 根据选择分组数据
    df_grouped = df[mask].groupby(by=['AREA NAME']).count()[['Vict Age']]
    df_grouped = df_grouped.rename(columns={'Vict Age': 'Amount'})
    df_grouped = df_grouped.reset_index()

    bar_chart = px.bar(df_grouped,
                       x='AREA NAME',
                       y='Amount',
                       text='Amount',
                       color_discrete_sequence=['#F63366'] * len(df_grouped),
                       template='plotly_white')
    st.plotly_chart(bar_chart)
    st.write("From the interactive bar chart above, it can be seen that people between the ages of 20 and 60, "
             "and those in the Central district, are more vulnerable to crime.")


with tab2:
    st.write("First, remove all abnormal age data from the dataset and keep only the valid ages. "
             "Then, combine the crime time of the crime events and plot a bar-scatter plot as shown below:")
    st.write("From the figure below, it is evident that the main distribution of victim ages falls between 20 and 65 years old. However,"
             " this is just an estimated range after visualization. "
             "Placing the mouse cursor over the image allows you to view specific data for points of interest.")


    df = pd.read_csv('10000_data.csv')
    fig = px.scatter(df, x="Vict Age", y="TIME OCC", marginal_y="rug", marginal_x="histogram")
    st.plotly_chart(fig)

    st.write("After obtaining an approximate age distribution, we can examine the main distribution of different crime events. "
             "Here, I will use a pie chart to visualize the percentage of each crime event.")
    st.write("You can click on the pie chart to view specific values, "
             "or click on the labels on the right side with your mouse to remove the current event percentage.")
    pie_chart = px.pie(df,
                       title='Crime Event Percentage Chart',
                       values='Crm Cd',
                       names='Crm Cd Desc')
    st.plotly_chart(pie_chart)
    st.write("By observing the pie chart, it can be seen that the crime event 'BURGLARY FROM VEHICLE' has a higher occurrence frequency."
             "Next, let's combine the crime events with the age of the victims for further observation as follows:")

    crim = df['Crm Cd Desc'].unique().tolist()
    age = df['Vict Age'].unique().tolist()

    age_selection = st.slider('年龄1:',
                              min_value=min(age),
                              max_value=max(age),
                              value=(min(age), max(age)))

    department_selection = st.multiselect('部门:',
                                          crim,
                                          default=crim)

    # 根据选择过滤数据
    mask = (df['Vict Age'].between(*age_selection)) & (df['Crm Cd Desc'].isin(department_selection))
    number_of_result = df[mask].shape[0]

    # 根据筛选条件, 得到有效数据
    st.markdown(f'*Effective data: {number_of_result}*')

    # 根据选择分组数据
    df_grouped = df[mask].groupby(by=['Crm Cd Desc']).count()[['Vict Age']]
    df_grouped = df_grouped.rename(columns={'Vict Age': 'Amount'})
    df_grouped = df_grouped.reset_index()

    bar_chart = px.bar(df_grouped,
                       x='Crm Cd Desc',
                       y='Amount',
                       text='Amount',
                       color_discrete_sequence=['#F63366'] * len(df_grouped),
                       template='plotly_white')
    st.plotly_chart(bar_chart)

    st.write("To better visualize the distribution of victim ages, let's plot a clear line graph as follows:")

    # 根据选择分组数据
    df_grouped = df[mask].groupby(by=['Vict Age']).count()[['Crm Cd Desc']]
    df_grouped = df_grouped.rename(columns={'Crm Cd Desc': 'Amount'})
    df_grouped = df_grouped.reset_index()


    aa = px.line(df_grouped, x="Vict Age", y="Amount")
    st.plotly_chart(aa)
    st.markdown(f'*Effective data: {number_of_result}*')
    st.write("Combining the above observations, the main distribution of victim ages can be expanded to range between 15 and 70. "
             "This indicates that individuals with a certain level of financial capability are more susceptible to crime.")

    st.write("Finally, to demonstrate the correlation between crime time and crime methods, "
             "the following dynamic bar chart is created to observe the daily crime situation.")
    fig1 = px.bar(df,
                  y="Crm Cd Desc",
                  x="Vict Age",
                  animation_frame="DATE OCC",
                  orientation='h',
                  range_x=[0, df['Vict Age'].max()],
                  color="Crm Cd Desc")
    # improve aesthetics
    fig1.update_layout(width=1000,
                       height=800,
                       xaxis_showgrid=False,
                       yaxis_showgrid=False,
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       title_text='Crime Incident Trend Chart',
                       showlegend=False)
    fig1.update_xaxes(title_text='Age')
    fig1.update_yaxes(title_text='')

    st.plotly_chart(fig1)


with tab3:
    st.write("Based on the visual analysis of the crime data presented earlier, "
             "we can conclude that the age distribution of the victims in these crime events is primarily between 15 and 70. "
             "This may be due to the fact that individuals within this age range are more likely to have financial capability. "
             "Additionally, there is a high percentage of property damage incidents, "
             "indicating that many people may be experiencing heightened levels of restlessness in their lives, "
             "which can contribute to criminal activities.")
    df = pd.read_csv('10000_data.csv')
    st.dataframe(df[mask], width=1000)
    st.write("The above is a data table displaying the specific data used for this data visualization. "
             "The characteristics of this dataset include undergoing data cleaning and random sampling, "
             "where invalid latitude and longitude values, as well as incorrect ages (age <= 0), have been removed. As a result, "
             "the dataset has been significantly reduced in size compared to the original data, leading to improved visualization efficiency.")
    st.write("Based on data analysis, this project identifies two main reasons for the persistently high crime rate: "
             "1. Significant wealth disparity in the Los Angeles area. "
             "2. Possible leniency in the education system for youth in Los Angeles. "
             "3. High demand and insufficient supply of job opportunities in the city of Los Angeles.")
    st.write("Therefore, we can suggest to the government to strengthen social and economic development, "
             "increase job opportunities, enhance moral education for youth, and promote crime prevention knowledge. "
             "These measures can help reduce the crime rate to a certain extent.")