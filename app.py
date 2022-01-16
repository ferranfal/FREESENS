import pandas as pd
import streamlit as st
import plotly.express as px
import xlrd


st.set_page_config(page_title='FREESENS', 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="expanded" )

# df = open('/home/ferran/GIT_HUB/FREESENS/humedad_no_sort.xls')
# df.name[-3:]


def main():  
       
   # titulo de la app
    st.title('FREESENS')
    st.header('FREE SOIL SENSOR VIWER')
    
    
    # Subir los datos en csv
    datafile = st.file_uploader('select csv or xls') 
        
    if datafile is not None:
        st.sidebar.markdown('### Introduce all data for visualization')
        st.sidebar.markdown("---")  
        
        if datafile.name[-3:] == 'csv':            
            sel_csv = st.sidebar.radio(
             "Select separator of your csv",
             (',', ';'))
            if sel_csv == ',':
                df = pd.read_csv(datafile, delimiter = ',')
            else:
                df = pd.read_csv(datafile, delimiter = ';')
                
                       
        elif datafile.name[-3:] == 'xls':
            df = pd.read_excel(datafile)
        else:
            st.warning('Input data should be .csv or .xls')
            
        #df = pd.read_csv(datafile, delimiter = ';')
        #df = pd.read_excel(datafile)
        #st.dataframe(df)
        columnas = df.columns
        col_sel = st.sidebar.selectbox('Date', columnas)
        
        columnas2 = columnas.drop([col_sel])
        col_sel2 = st.sidebar.multiselect('Sensors', columnas, default = columnas2.to_list())
        st.sidebar.markdown("""---""")
        st.sidebar.markdown('### Introduce data for mean analisys')
        st.sidebar.markdown("""---""")
       
        fig = px.line(
          df,
          x = col_sel,
          y = col_sel2,
          width=1200, 
          height=500, 
          template="simple_white"
          )
        
        fig.update_traces(line=dict(width=1))
        
        fig.update_layout({
            'plot_bgcolor': '#FFFFFF'
            ''
            })
     
        st.plotly_chart(fig)
        

        # PARA EL GRAFICO DE MEDIAS
        col_sel = st.sidebar.selectbox('Date for mean value', columnas)
        
        columnas2 = columnas.drop([col_sel])
        col_sel2 = st.sidebar.multiselect('Sensors for mean value', columnas)
        
        df_mean = pd.DataFrame(df[col_sel2].mean(axis=1))
        df_date = pd.DataFrame(df[col_sel])
        
        df_mean_final = pd.concat([df_date, df_mean], axis = 1)
        
        cc = st.sidebar.number_input('Field capacity')
        ur = st.sidebar.number_input('Irrigation point')
        
        
        fig2 = px.line(
          df_mean_final,
          x = df_mean_final.columns[0],
          y = df_mean_final.columns[1],
          width=1200, height=500, 
          template="simple_white"
          )
        fig2.update_traces(line=dict(width=1))
        
        fig2.add_hrect(
            y0=ur, y1=cc,
            fillcolor="green", opacity=0.1,
            layer="below", line_width=0,
            )
        
        fig2.add_hrect(
            y0=0, y1=ur,
            fillcolor="red", opacity=0.1,
            layer="below", line_width=0,
            )
        
        fig2.add_hrect(
            y0=cc, y1=100,
            fillcolor="blue", opacity=0.1,
            layer="below", line_width=0,
            )
        
        
        fig2.update_layout({
            'plot_bgcolor': '#FFFFFF'
            })
        
        st.plotly_chart(fig2)
        

    pass

if __name__ =='__main__':
    main()


