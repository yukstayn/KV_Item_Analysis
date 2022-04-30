
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time



st.title('KV - Item Analyzer')

upload_file = st.file_uploader( label = 'Choose an Excel File', type = 'xlsx')

with st.spinner('rendering...'):
    time.sleep(4)

if upload_file is not None:

	df = pd.DataFrame(pd.read_excel(upload_file)).astype(int)
	df.index = df.index + 1
	st.write(df)

	st.subheader('Delete Unwanted Columns and Rows')

	
	col_a, col_b = st.columns(2)

	with col_a:
		col_delete = st.multiselect('Choose Columns to Delete', options = df.columns)
		df.drop( col_delete, axis='columns', inplace=True)
		

	with col_b:
		row_delete = st.multiselect('Choose Rows to Delete', options = df.index)
		df.drop(row_delete, axis=0, inplace=True)

	st.write(df)


	st.subheader('Discrimination and Difficulty Index')

	slider = st.slider('Choose the number of Upper and Lower Group', min_value = df.index.min(), max_value = df.index.max())

	st.success(f'The Upper Group and Lower Group is {slider}')
	col_c, col_d = st.columns(2)

	with col_c:
		st.markdown('#### Upper Group')
		upper = df.head(slider)
		st.write(upper)
	with col_d:
		st.markdown('#### Lower Group')
		lower = df.tail(slider)
		st.write(lower)

	

	UG = upper.sum(axis=0)
	LG = lower.sum(axis=0)


	diff_index = (UG + LG)/(2*slider) 
	disc_index = (UG - LG)/(2*slider) 

	new_df = pd.concat([diff_index, disc_index], axis=1).T
	new_df.set_index([pd.Index(['Difficulty Index', 'Discrimination Index'])],inplace=True)

	st.markdown('### Analysis & Visualization')
	st.write(new_df)

	fig = go.Figure(data=[
	    go.Bar(name='Difficulty Index', x=new_df.columns, y=diff_index),
	    go.Bar(name='Discrimination Index', x=new_df.columns, y=disc_index)
	])
	
	fig.update_layout(barmode='group')
	fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right",x=1))
	fig.update_xaxes(tickangle=-45,tickmode = 'array', tickvals = new_df.columns)

	st.plotly_chart(fig, sharing="streamlit")

 
	








