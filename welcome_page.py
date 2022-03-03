from turtle import title
import streamlit as st
import streamlit_authenticator as stauth
import PIL
import random
import pandas as pd
from csv import writer
import csv
import math
from barcode import EAN13
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


disp_bal = 1

im1= PIL.Image.open("Robogyaan.png")
im2 = PIL.Image.open("vizworld.png")
im3 = PIL.Image.open("goat.png")

# st.set_page_config(page_title="Welcome Page", page_icon=" 🐐 ", layout="centered")

def clear_form():
    app()

def generate_unique_code():
    list2 = []
    with open('records.csv', 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        for row in csv_reader:
            try:
                list2.append(int(row[0]))
            except:
                continue
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(12):
            index = math.floor(random.random() * 10)
            random_str += str(digits[index])
        uniq_id = int(random_str)
        while True:
            if uniq_id in list2:
                random_str = ""
                for i in range(12):
                    index = math.floor(random.random() * 10)
                    random_str += str(digits[index])
                uniq_id = int(random_str)
            else:
                break
    return uniq_id


cattle_data = pd.read_csv(
    "records.csv"
)

def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection







def app():

    


    col1,col2,col3 = st.columns([3,6,3])

    with col1:
        st.write("")
    with col2:
        st.image(im1)
    with col3:
        st.write("")

    col1,col2,col3 = st.columns([0.5,6,0.5])
    with col1:
        st.write("")
    with col2:
        st.header("🐐 Cattle Management App")
    with col3:
        st.write("")

    st.write("")
    with st.expander("Add New Goat"):
        st.write("Fill & Submit the following form to Update the New Cattle Details")
        form = st.form(key="newgoat")
        with form:
            cols = st.columns((1, 1))
            farmer = cols[0].text_input("Report Farmer:")
            gender = cols[1].selectbox(
                "Gender:", ["Male", "Female"], index=1)
            cols = st.columns((1, 1))
            dob = cols[0].date_input("Date of Birth:")
            weight = cols[1].text_input("Weight (Kg)")
            cols = st.columns((1, 1))
            vaccination = cols[0].text_area("Vaccination Details:")
            diseases = cols[1].text_area("Disease Details:")
            cols = st.columns((1, 1))
            concieved = cols[0].text_area("Concieved Details:")
            delivery = cols[1].text_area("Delivery Details:")    
            cols = st.columns((1, 1))
            medication = cols[0].text_area("Medication Details:")
            remarks = cols[1].text_area("Additional Remarks:")  
            cols = st.columns((1, 1))
            dou = cols[0].date_input("Date of Updation:")
            cols = st.columns((1, 1))
            submitted = cols[0].form_submit_button(label="Submit")
            clearform = cols[1].form_submit_button(label="Clear Form")
        
        if submitted:    
            uid = generate_unique_code()
            List = [uid,farmer,gender,dob,weight,vaccination,diseases,concieved,delivery,medication,remarks,dou]
            with open('records.csv', 'a') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(List)
                f_object.close()
            st.balloons()
            st.success(f"Cattle Information Added Successfully")
            my_code = EAN13(str(uid))
            my_code.save("barcode")
            with open("barcode.svg", "rb") as file:
                btn = st.download_button(
                        label="Download Barcode",
                        data=file,
                        file_name=f"{uid}.svg",
                        mime="image/png"
                    )
        if clearform:
            clear_form()
        
    with st.expander("View All Existing Records"):
        st.write("Enrolled Cattle from the Records")
        selection = aggrid_interactive_table(df=cattle_data)
        if selection:
            st.write("You selected:")
            st.json(selection["selected_rows"])

    with st.expander("Get Individual Details"):
        st.write("""This Option Adds Goat Information to the Master sheet""")
        st.image("https://static.streamlit.io/examples/dice.jpg")

    
    return 'VARUN'

app()