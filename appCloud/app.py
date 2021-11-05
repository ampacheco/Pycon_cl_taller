import streamlit as st
import pandas as pd

st.title('AppMap')
st.markdown('This is a simple app to help you visualize your app\'s data.')
st.markdown('**Note:** This app is still in development. Please report any bugs or suggestions to [@napoles3D](https://twitter.com/napoles3D)')

filepath = 'https://raw.githubusercontent.com/napoles-uach/Pycon_cl_taller/main/meteorite-landings.csv'

@st.cache
def read_csv(file_path):
    df = pd.read_csv(file_path)
    return df

df = read_csv(filepath)

st.button('test')

df=df[(df['mass']>0 )] #evitar algunos valores incompletos
df=df[abs(df['lat'])>0]  #evitar algunos valores incompletos

year_min=int(df['year'].min()) #identificamos el valor mínimo
year_max=int(df['year'].max()) #identificamos el valor máximo
cols=list(df.columns) # lista con nombres de columnas en el csv


# separamos en columnas
col1,col2,col3 = st.columns([5,1,5])

with col1.expander('widgets'):
    year_range = st.slider('year range',year_min,year_max,[1800,1900],step=10)
    vals=st.multiselect('',cols)

df1=df[(df['year']>=year_range[0] ) & (df['year']<=year_range[1] )]
df2=df1[vals]

with col1.expander('data'):
    st.dataframe(df2)

if ("lat" in vals) and ("lon" in vals):
    col3.map(df2)

check=col1.checkbox('Save File')
if check:
    df2.to_csv('data.csv')
    name=col1.text_input('*.csv file name:')
    #check if name is not empty
    if name:
        with open('data.csv') as f:
            col1.download_button('Download Data',f,file_name=name)
