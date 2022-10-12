from turtle import title
import streamlit as st
from transformers.pipelines import pipeline
import pandas as pd
from io import StringIO 
import boto3
import random
import plotly.express as px

st.set_page_config(page_title="Telescope", page_icon="🔭",  menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': None
     })

# Inject CSS with Markdown
hide_table_row_index = """
        <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            footer, header {display:none !important}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)

st.header("Add Data For Analysis")
uploaded_txts = st.file_uploader(label="Drop Medical Summaries", type=['txt'], accept_multiple_files=True)

@st.cache(allow_output_mutation=True)
def load_nlp_QA():
    model_name = "deepset/roberta-base-squad2"
    return pipeline('question-answering', model=model_name, tokenizer=model_name)

query = ""

if len(uploaded_txts)>0:

    for txt in uploaded_txts:
        string = StringIO(txt.getvalue().decode("utf-8")).read()
        # call backend for qa
        if string != "":
            nlp = load_nlp_QA()
            QA_input = {
                'question': 'What will the people need to do or get in the future?',
                'context': string
            }
            res = nlp(QA_input)
            certainty = res['score']
            answer = res['answer']
            query += answer+"\n"

    structure ={} # datastructue for counting
    df = pd.DataFrame(columns=['Procedure Name','Count', 'Cost'])
    # call backend for AWS NER
    client = boto3.client(service_name='comprehendmedical', region_name='us-east-2')
    result = client.detect_entities(Text=query)
    entities = result['Entities']
    # count instances of procedures
    for entity in entities:
        if entity["Category"] == "TEST_TREATMENT_PROCEDURE":
            try:
                structure[entity["Text"].capitalize()] += 1
            except:
                structure[entity["Text"].capitalize()] = 1

    # count total costs and add data to df
    total_cost = 0
    for key,value in structure.items():
        cost = random.randint(200, 1000)
        df.loc[len(df.index)] = [key, value, cost] 
        total_cost += value*cost

    st.header("Predicted Future Procedures")
    
    # datafram visualization
    st.table(df)

    # key metric visualization
    total_count = df['Count'].sum()
    col1, col2,col3 = st.columns(3)
    col1.metric(label="Total Count of Procedures", value=total_count)
    col2.metric(label="Total Expected Cost", value="${:.0f}".format(total_cost))
    col3.metric(label="Average Cost Per Person", value="${:.0f}".format(total_cost/len(uploaded_txts)))
    
    st.header("Visualizations")
    
    # histogram
    fig = px.histogram(df,x="Cost",y="Count", nbins=15, title="Histogram of Future Procedure Costs")
    fig.update_layout(xaxis_title="Cost", yaxis_title="Count")
    st.plotly_chart(fig)

    # pie chart
    fig = px.pie(df, values='Count', names='Procedure Name', title='Pie Chart of Future Procedures')
    st.plotly_chart(fig, use_container_width=True)
