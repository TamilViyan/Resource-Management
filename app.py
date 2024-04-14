import os
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit as st
from streamlit_option_menu import option_menu
import requests
import json


path_dir ='C:/Users/Aarav/OneDrive/Desktop/DataSets/'
df=pd.DataFrame()

for files in os.listdir(path_dir):
    DataFrame = pd.read_csv('C:/Users/Aarav/OneDrive/Desktop/DataSets/' + files, encoding='ISO-8859-1')
    df = pd.concat([df, DataFrame])

#Renaming the column names
df.rename(columns = {'State Code':'State_Code'}, inplace = True)
df.rename(columns = {'District Code':'District_Code'}, inplace = True)
df.rename(columns = {'Main Workers - Total -  Persons':'Main_Workers_Total_Persons'}, inplace = True)
df.rename(columns = {'Main Workers - Total - Males':'Main_Workers_Total_Males'}, inplace = True)
df.rename(columns = {'Main Workers - Total - Females':'Main_Workers_Total_Females'}, inplace = True)
df.rename(columns = {'Main Workers - Rural -  Persons':'Main_Workers_Rural_Persons'}, inplace = True)
df.rename(columns = {'Main Workers - Rural - Males':'Main_Workers_Rural_Males'}, inplace = True)
df.rename(columns = {'Main Workers - Rural - Females':'Main_Workers_Rural_Females'}, inplace = True)
df.rename(columns = {'Main Workers - Urban -  Persons':'Main_Workers_Urban_Persons'}, inplace = True)
df.rename(columns = {'Main Workers - Urban - Males':'Main_Workers_Urban_Males'}, inplace = True)
df.rename(columns = {'Main Workers - Urban - Females':'Main_Workers_Urban_Females'}, inplace = True)
df.rename(columns = {'Marginal Workers - Total -  Persons':'Marginal_Workers_Total_Persons'}, inplace = True)
df.rename(columns = {'Marginal Workers - Total - Males':'Marginal_Workers_Total_Males'}, inplace = True)
df.rename(columns = {'Marginal Workers - Total - Females':'Marginal_Workers_Total_Females'}, inplace = True)
df.rename(columns = {'Marginal Workers - Rural -  Persons':'Marginal_Workers_Rural_Persons'}, inplace = True)
df.rename(columns = {'Marginal Workers - Rural - Males':'Marginal_Workers_Rural_Males'}, inplace = True)
df.rename(columns = {'Marginal Workers - Rural - Females':'Marginal_Workers_Rural_Females'}, inplace = True)
df.rename(columns = {'Marginal Workers - Urban -  Persons':'Marginal_Workers_Urban_Persons'}, inplace = True)
df.rename(columns = {'Marginal Workers - Urban - Males':'Marginal_Workers_Urban_Males'}, inplace = True)
df.rename(columns = {'Marginal Workers - Urban - Females':'Marginal_Workers_Urban_Females'}, inplace = True)
df.rename(columns={'India/States':'States'},inplace = True)
df.rename(columns = {'NIC Name':'NICName'}, inplace = True)

#EDA
#creating new feature
df["state_head"]=df.States.str.split("-")
df["state_dump"]=df.States.str.split("-")
df["state_names"]=df.state_dump.apply(lambda x:x[1])

df.state_head=df.state_dump.apply(lambda x:x[0])
df.drop(columns=['state_dump', 'States'], inplace=True)

def eda():
    # Check for leading/trailing whitespaces
    df['state_names'].str.strip()
    df['state_names'] = df['state_names'].str.title()
    df['state_names'] = df['state_names'].replace('Nct Of Delhi', 'Delhi')

    df_sts = df[df['state_head'] == 'STATE ']
    return df_sts
        
def state():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])
    states_name.sort()
    return data1



def STC_wrks_ttl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    
    state_group = state.groupby("State_Code")[["Main_Workers_Total_Persons","Main_Workers_Rural_Persons","Main_Workers_Urban_Persons",
                                              "Marginal_Workers_Total_Persons","Marginal_Workers_Rural_Persons","Marginal_Workers_Urban_Persons"]].sum()
    state_group.reset_index(inplace = True)
    
    fig_bar = px.bar(state_group, x='State_Code', y=['Main_Workers_Total_Persons', 'Marginal_Workers_Total_Persons'], 
                     title='Main and Marginal Workers by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar)
    state_group

def STC_wrks_rrl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group = state.groupby("State_Code")[["Main_Workers_Total_Persons","Main_Workers_Rural_Persons","Main_Workers_Urban_Persons",
                                              "Marginal_Workers_Total_Persons","Marginal_Workers_Rural_Persons","Marginal_Workers_Urban_Persons"]].sum()
    state_group.reset_index(inplace = True)
    
    fig_bar1 = px.bar(state_group, x='State_Code', y=['Main_Workers_Rural_Persons', 'Marginal_Workers_Rural_Persons'], 
                    title='Main and Marginal Rural Workers by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar1)
    state_group

def STC_wrks_urb(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group = state.groupby("State_Code")[["Main_Workers_Total_Persons","Main_Workers_Rural_Persons","Main_Workers_Urban_Persons",
                                             "Marginal_Workers_Total_Persons","Marginal_Workers_Rural_Persons","Marginal_Workers_Urban_Persons"]].sum()
    state_group.reset_index(inplace = True)
    
    fig_bar2 = px.bar(state_group, x='State_Code', y=['Main_Workers_Urban_Persons', 'Marginal_Workers_Urban_Persons'], 
                     title='Main and Marginal Urban Workers by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar2)
    state_group   

def STC_male_ttl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_male = state.groupby("State_Code")[["Main_Workers_Total_Males","Main_Workers_Rural_Males","Main_Workers_Urban_Males",
                                              "Marginal_Workers_Total_Males","Marginal_Workers_Rural_Males","Marginal_Workers_Urban_Males"]].sum()
    state_group_male.reset_index(inplace = True)
    
    fig_bar3 = px.bar(state_group_male, x='State_Code', y=['Main_Workers_Total_Males', 'Marginal_Workers_Total_Males'], 
                     title='Main and Marginal Workers total Males by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar3)
    state_group_male

def STC_male_rrl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_male = state.groupby("State_Code")[["Main_Workers_Total_Males","Main_Workers_Rural_Males","Main_Workers_Urban_Males",
                                              "Marginal_Workers_Total_Males","Marginal_Workers_Rural_Males","Marginal_Workers_Urban_Males"]].sum()
    state_group_male.reset_index(inplace = True)
    
    fig_bar4 = px.bar(state_group_male, x='State_Code', y=['Main_Workers_Rural_Males', 'Marginal_Workers_Rural_Males'], 
                     title='Main and Marginal Workers Rural Males by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar4)
    state_group_male

def STC_male_urb(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_male = state.groupby("State_Code")[["Main_Workers_Total_Males","Main_Workers_Rural_Males","Main_Workers_Urban_Males",
                                              "Marginal_Workers_Total_Males","Marginal_Workers_Rural_Males","Marginal_Workers_Urban_Males"]].sum()
    state_group_male.reset_index(inplace = True)
    
    fig_bar5 = px.bar(state_group_male, x='State_Code', y=['Main_Workers_Urban_Males', 'Marginal_Workers_Urban_Males'], 
                     title='Main and Marginal Workers Urban Males by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar5)
    state_group_male

def STC_female_ttl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_female = state.groupby("State_Code")[["Main_Workers_Total_Females","Main_Workers_Rural_Females","Main_Workers_Urban_Females",
                                              "Marginal_Workers_Total_Females","Marginal_Workers_Rural_Females","Marginal_Workers_Urban_Females"]].sum()
    state_group_female.reset_index(inplace = True)
    
    fig_bar6 = px.bar(state_group_female, x='State_Code', y=['Main_Workers_Total_Females', 'Marginal_Workers_Total_Females'], 
                     title='Main and Marginal Workers Total Females by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar6)
    state_group_female

def STC_female_rrl(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_female = state.groupby("State_Code")[["Main_Workers_Total_Females","Main_Workers_Rural_Females","Main_Workers_Urban_Females",
                                              "Marginal_Workers_Total_Females","Marginal_Workers_Rural_Females","Marginal_Workers_Urban_Females"]].sum()
    state_group_female.reset_index(inplace = True)
    
    fig_bar7 = px.bar(state_group_female, x='State_Code', y=['Main_Workers_Rural_Females', 'Marginal_Workers_Rural_Females'], 
                     title='Main and Marginal Workers Rural Females by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar7)
    state_group_female

def STC_female_urb(code):
    state = df[df["State_Code"] == code]
    state.reset_index(drop = True,inplace = True)
    state_group_female = state.groupby("State_Code")[["Main_Workers_Total_Females","Main_Workers_Rural_Females","Main_Workers_Urban_Females",
                                              "Marginal_Workers_Total_Females","Marginal_Workers_Rural_Females","Marginal_Workers_Urban_Females"]].sum()
    state_group_female.reset_index(inplace = True)
    
    fig_bar8 = px.bar(state_group_female, x='State_Code', y=['Main_Workers_Urban_Females', 'Marginal_Workers_Urban_Females'], 
                     title='Main and Marginal Workers Urban Females by State with Color', height=600, width=600)
    st.plotly_chart(fig_bar8)
    state_group_female

#streamlit part
st.set_page_config(layout="wide")
st.title(":blue[RESOURCE MANAGEMENT]")

with st.sidebar:
    select = option_menu("Main Menu",["Home","Geo-Visualization","Data Analysis"])

if select == "Home":
    st.write("Resource Management")
elif select == "Data Analysis":
    tab1,tab2,tab3 = st.tabs(["Total","Male","Female"])
    
    with tab1:
        method = st.radio("Select the method",["Total Workers", "Rural Workers", "Urban Workers"])
        if method == "Total Workers":

            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox')
                total_wrk = STC_wrks_ttl(code)
       
        elif method == "Rural Workers":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox')
                rural_wrk = STC_wrks_rrl(code)
        elif method == "Urban Workers":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox')
                urban_wrk = STC_wrks_urb(code)
    with tab2:
        method1 = st.radio("Select the method",["Total Male", "Rural Male", "Urban Male"])
        if method1 == "Total Male":
            
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'))
                total_male = STC_male_ttl(code)
        elif method1 == "Rural Male":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'))
                rural_male = STC_male_rrl(code)
        elif method1 == "Urban Male":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'))
                urban_male = STC_male_urb(code)

    with tab3:
        method2 = st.radio("Select the method",["Total Female", "Rural Female", "Urban Female"])
        if method2 == "Total Female":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox1')
                total_female = STC_female_ttl(code)
        elif method2 == "Rural Female":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox1')
                rural_female = STC_female_rrl(code)
        
        elif method2 == "Urban Female":
            col1,col2 = st.columns(2)
            with col1:
                code = st.selectbox('Select the State Code',
                            ('`07', '`16', '`20', '`24', '`27', '`29', '`30', '`32', '`33',
                            '`34', '`02', '`05', '`09', '`10', '`11', '`13', '`18', '`21',
                            '`08', '`12', '`14', '`15', '`19'),key='state_code_selectbox1')
                urban_female = STC_female_urb(code)

elif select == "Geo-Visualization":
    tab1,tab2,tab3 = st.tabs(["Total","Male","Female"])
    with tab1:
        col1,col2 = st.columns(2)
        with col1:
            #statewise main workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Total_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Total_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Total_Persons"].min(), df_sl_group["Main_Workers_Total_Persons"].max()),
                                        hover_name="state_names", title="Main Workers Count by State", fitbounds = "locations",height=500, width=500)
            fig_state.update_geos(visible = False)
            st.plotly_chart(fig_state)
        
        with col2:
            #statewise marginal workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Marginal_Workers_Total_Persons","Marginal_Workers_Total_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state1 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Total_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Total_Persons"].min(), df_sl_group["Marginal_Workers_Total_Persons"].max()),
                                        hover_name="state_names", title="Marginal Workers Count by State", fitbounds = "locations",
                                        height=500, width=500)
            fig_state1.update_geos(visible = False)
            st.plotly_chart(fig_state1)

        col1,col2 = st.columns(2)
        with col1:
            #statewise main rural workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Rural_Persons"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state2 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Rural_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Rural_Persons"].min(), df_sl_group["Main_Workers_Rural_Persons"].max()),
                                        hover_name="state_names", title="Main Rural Workers Count by State", fitbounds = "locations",height=500, width=500)
            fig_state2.update_geos(visible = False)
            st.plotly_chart(fig_state2)
        
        with col2:
            #statewise marginal rural workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Marginal_Workers_Total_Persons","Marginal_Workers_Rural_Persons"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state3 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Rural_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Rural_Persons"].min(), df_sl_group["Marginal_Workers_Rural_Persons"].max()),
                                        hover_name="state_names", title="Marginal Rural Workers Count by State", fitbounds = "locations",
                                        height=500, width=500)
            fig_state3.update_geos(visible = False)
            st.plotly_chart(fig_state3)

        col1,col2 = st.columns(2)
        with col1:
            #statewise main urban workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Urban_Persons"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state4 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Urban_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Urban_Persons"].min(), df_sl_group["Main_Workers_Urban_Persons"].max()),
                                        hover_name="state_names", title="Main Urban Workers Count by State", fitbounds = "locations",height=500, width=500)
            fig_state4.update_geos(visible = False)
            st.plotly_chart(fig_state4)
        
        with col2:
            #statewise marginal urban workers total persons
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Marginal_Workers_Total_Persons","Marginal_Workers_Urban_Persons"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state5 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Urban_Persons", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Urban_Persons"].min(), df_sl_group["Marginal_Workers_Urban_Persons"].max()),
                                        hover_name="state_names", title="Marginal Urban Workers Count by State", fitbounds = "locations",
                                        height=500, width=500)
            fig_state5.update_geos(visible = False)
            st.plotly_chart(fig_state5)

    with tab2:
        col1,col2 = st.columns(2)
        with col1:
            #statewise main workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Total_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state6 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Total_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Total_Males"].min(), df_sl_group["Main_Workers_Total_Males"].max()),
                                        hover_name="state_names", title="Main Worker Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state6.update_geos(visible = False)
            st.plotly_chart(fig_state6)

        with col2:
            #statewise marginal workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Total_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state7 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Total_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Total_Males"].min(), df_sl_group["Marginal_Workers_Total_Males"].max()),
                                        hover_name="state_names", title="Marginal Worker Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state7.update_geos(visible = False)
            st.plotly_chart(fig_state7)

        col1,col2 = st.columns(2)
        with col1:
            #statewise main rural workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Rural_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state8 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Rural_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Rural_Males"].min(), df_sl_group["Main_Workers_Rural_Males"].max()),
                                        hover_name="state_names", title="Main Worker Rural Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state8.update_geos(visible = False)
            st.plotly_chart(fig_state8)

        with col2:
            #statewise marginal rural workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Rural_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state9 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Rural_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Rural_Males"].min(), df_sl_group["Marginal_Workers_Rural_Males"].max()),
                                        hover_name="state_names", title="Marginal Worker Rural Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state7.update_geos(visible = False)
            st.plotly_chart(fig_state9)

        col1,col2 = st.columns(2)
        with col1:
            #statewise main urban workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Urban_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state10 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Urban_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Urban_Males"].min(), df_sl_group["Main_Workers_Urban_Males"].max()),
                                        hover_name="state_names", title="Main Worker Urban Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state10.update_geos(visible = False)
            st.plotly_chart(fig_state10)

        with col2:
            #statewise marginal urban workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Urban_Males"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state11 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Urban_Males", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Urban_Males"].min(), df_sl_group["Marginal_Workers_Urban_Males"].max()),
                                        hover_name="state_names", title="Marginal Worker Urban Males Count by State", fitbounds = "locations",height=500, width=500)
            fig_state11.update_geos(visible = False)
            st.plotly_chart(fig_state11)

    with tab3:
        col1,col2 = st.columns(2)
        with col1:
            #statewise main workers total females
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Total_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state12 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Total_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Total_Females"].min(), df_sl_group["Main_Workers_Total_Females"].max()),
                                        hover_name="state_names", title="Main Worker Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state12.update_geos(visible = False)
            st.plotly_chart(fig_state12)

        with col2:
            #statewise marginal workers total females
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Total_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state13 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Total_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Total_Females"].min(), df_sl_group["Marginal_Workers_Total_Females"].max()),
                                        hover_name="state_names", title="Marginal Worker Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state13.update_geos(visible = False)
            st.plotly_chart(fig_state13)

        col1,col2 = st.columns(2)
        with col1:
            #statewise main rural workers total females
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Rural_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state14 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Rural_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Rural_Females"].min(), df_sl_group["Main_Workers_Rural_Females"].max()),
                                        hover_name="state_names", title="Main Worker Rural Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state14.update_geos(visible = False)
            st.plotly_chart(fig_state14)

        with col2:
            #statewise marginal rural workers total females
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Rural_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state15 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Rural_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Rural_Females"].min(), df_sl_group["Marginal_Workers_Rural_Females"].max()),
                                        hover_name="state_names", title="Marginal Worker Rural Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state15.update_geos(visible = False)
            st.plotly_chart(fig_state15)
        
        col1,col2 = st.columns(2)
        with col1:
            #statewise main urban workers total females
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Main_Workers_Urban_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state16 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Main_Workers_Urban_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Main_Workers_Urban_Females"].min(), df_sl_group["Main_Workers_Urban_Females"].max()),
                                        hover_name="state_names", title="Main Worker Urban Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state16.update_geos(visible = False)
            st.plotly_chart(fig_state16)

        with col2:
            #statewise marginal urban workers total males
            df_states = eda()  
            df_sl_group = df_states.groupby("state_names")[["Main_Workers_Total_Persons","Marginal_Workers_Urban_Females"]].sum()
            df_sl_group.reset_index(inplace = True)
            df_sl_group['state_names'] = df_sl_group['state_names'].str.strip()
            
            data = state()
            fig_state17 = px.choropleth(df_sl_group, geojson=data, locations="state_names", featureidkey="properties.ST_NM",
                                        color="Marginal_Workers_Urban_Females", color_continuous_scale="Rainbow",
                                        range_color=(df_sl_group["Marginal_Workers_Urban_Females"].min(), df_sl_group["Marginal_Workers_Urban_Females"].max()),
                                        hover_name="state_names", title="Marginal Worker Urban Females Count by State", fitbounds = "locations",height=500, width=500)
            fig_state17.update_geos(visible = False)
            st.plotly_chart(fig_state17)


