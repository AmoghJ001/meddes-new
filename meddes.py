
import tensorflow as tf
import keras 
import streamlit as st
from tensorflow.keras.models import load_model
import SessionState
import streamlit as st
import pandas as pd
import cv2
from PIL import Image, ImageOps
import numpy as np
import pandas as pd
import base64
meddes=Image.open('meddes.PNG')
st.set_page_config(page_title='MedDES', page_icon = meddes, initial_sidebar_state = 'auto')
st.sidebar.title('Navigation')
radio = st.sidebar.radio(label="", options=["About MedDES","Patient Biodata", "Malaria Test", "COVID-19 Test","Pneumonia Test", "Brain Tumour Test", "Patient Report"])

session_state = SessionState.get(name = "", gender = "", symptoms = "",age = 18,diability="",  mal="Not done",covid="Not done", pneu = "Not done", bt = "Not done")  # Pick some initial values.
cols = ["Patient Name", "Gender", "Age","Physical Disability", "Symptoms","Malaria Test", "COVID-19 Test","Pneumonia Test", "Brain Tumour Test"]
glist = ['Male', 'Female','Other']
dlist = ["No",'Yes']

if radio == "About MedDES":
    st.image(meddes, width=None)
    st.write("*Copyright:* :copyright: Amogh Manoj Joshi")
    st.title('MedDES: The Medical Diagnostic Expert System')
    st.write(
        'This is an AI driven Medical Diagnostic system which can assist the diagnostic process of a doctor.  \n '
        'Intended to be used in hospitals/medical labs as a diagnostic helper tool for medical healthcare staff  \n'
        'In urgent cases, when a medical expert is not available for diagnosis, MedDES can be of great help.  \n'
        'Though our diagnostic tests are highly accurate having trained on real data, the diagnostic predictions can go wrong in rare cases.  \n'
        'Hence, we recommend seeking an appointment with a medical expert for confirmation.')
    st.subheader('How It Works?')
    from PIL import Image
    image = Image.open('Systemfunc.png')
    st.image(image, caption='How MedDES works',width=None)
    st.subheader("*Patient Biodata*")
    st.write('The biodata of the concerned patient is uploaded in our system.  \n'
             'It is temporarily saved in our database and is later used while generating the patient report.')
    st.subheader("*Diagnostic Tests*")
    st.write('We currently have 4 diagnostic tests:  \n'
             '-Malaria Test  \n'
             '-COVID-19 Test  \n'
             '-Pneumonia Test  \n'
             '-Brain Tumour Test  \n'
             'Each test requires a particular biomedical image of the concerned body part for diagnosis eg. COVID-19 Test requires a CT scan of the chest.  \n'
             'The diagnostic result is immediately displayed once the required image is uploaded for diagnosis.  \n')
    st.subheader("*Generated Patient Report*")
    st.write('After taking all the tests required, the results of all the tests taken are updated in our system  \n'
             'Our system has an added feature of generating a detailed patient report.  \n'
             'The report contains the patient biodata and the results of the tests performed.  \n'
             'The detailed report can be downloaded as an excel file for hospital records.  \n')

elif radio == "Patient Biodata":
    st.title('Patient Biodata')
    st.write(
        'Please enter the biodata of the concerned patient')  # Asking for new profile data
    session_state.name = st.text_input("Enter the patient name: ", value=session_state.name)
    session_state.gender = st.selectbox("Select Gender:", glist)
    session_state.age = st.slider("What is your age?", 1, 100, value=session_state.age)
    session_state.disability = st.selectbox("Any physical disability:", dlist)
    session_state.symptoms = st.text_input("Any symptoms: ", value=session_state.symptoms)

elif radio == "Malaria Test":
    model = load_model('/app/malmodelnew.hdf5')
    st.write("""
                 # Malaria Diagnostic Test
                 """
             )
    st.write(
        "Malaria is a life-threatening disease. It's typically transmitted through the bite of an infected Anopheles mosquito. "
        "Infected mosquitoes carry the Plasmodium parasite. When this mosquito bites you, the parasite is released into your bloodstream.  \n"
        "Examining microscopic blood cells has proven to be an effective diagnostic test for early diagnosis of Malaria  \n"
        "*SYMPTOMS:*  \n"
        "-Chills, fever and sweating usually occurring a few weeks after being bitten.  \n"
        "-Some other symptoms include fast heart rate, headache, diarrhoea, nausea or vomiting   \n"
        "*source:* [who.int](https://www.who.int/news-room/fact-sheets/detail/malaria)")
    st.subheader("Please upload a Microscopic Blood Smear Image of the patient!")
    file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        size = (64, 64)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resize = (cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)) / 255.
        img_reshape = img_resize[np.newaxis, ...]
        prediction = model.predict(img_reshape)
        classes = np.argmax(prediction, axis=1)
        if classes == 0:
            st.subheader('Diagnostic Result:')
            st.write("The following patient is an Uninfected case")
            session_state.mal = "Normal"
        else:
            st.subheader('Diagnostic Result:')
            st.write("The following patient is an Infected case. We suggest an appointment with a Medical Expert for confirmation. ")
            #st.text("Diagnostic probability:" + prob)
            session_state.mal = "Malaria Infected"
elif radio == "COVID-19 Test":
    model = load_model('/app/covidmodel.hdf5')
    st.write("""
                 # COVID-19 Diagnostic Test
                 """
             )
    st.write(
        "Sars-Cov2 also known as Coronavirus disease (COVID-19) is an infectious disease caused by a newly discovered coronavirus. Most people who fall sick with COVID-19 will experience mild to moderate symptoms and recover without special treatment.  \n"
        "Several researches have shown that Chest Computer Tomography (CT) scans manifest clear radiological findings of COVID-19. Hence, examining chest CT scans is an effective diagnostic test for COVID-19  \n"
        "*MOST COMMON SYMPTOMS:*  \n"
        "-fever  \n"
        "-dry cough  \n"
        "-tiredness  \n"
        "*LESS COMMON SYMPTOMS:*  \n"
        "-aches and pains  \n"
        "-sore throat  \n"
        "-diarrhoea  \n"
        "-conjunctivitis  \n"
        "-headache  \n"
        "-loss of taste or smell  \n"
        "-a rash on skin, or discolouration of fingers or toes  \n"
        "*source:* [who.int](https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19#:~:text=symptoms)")
    st.subheader("Please upload an Axial Chest CT Scan  of the patient!")
    file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resize = (cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)) / 255.
        img_reshape = img_resize[np.newaxis, ...]
        prediction = model.predict(img_reshape)
        classes = np.argmax(prediction, axis=1)
        if classes == 0:
            st.subheader('Diagnostic Result:')
            st.write("The following patient is Covid Negative i.e Normal case")
            session_state.covid = "COVID Negative"
        else:
            st.subheader('Diagnostic Result:')
            st.write("The following patient has been infected with COVID-19. We suggest an appointment with a Medical Expert for confirmation.")
            #st.text("Diagnostic probability:" + prob)
            session_state.covid = "COVID Positive"
elif radio == "Pneumonia Test":
    model = load_model('/app/pneumodel.hdf5')
    st.write("""
                 # Pneumonia Diagnostic Test
                 """
             )
    st.write(
        "Infection that inflames air sacs in one or both lungs, which may fill with fluid. With pneumonia, the air sacs may fill with fluid or pus.  \n"
        "The infection can be life-threatening to anyone, but particularly to infants, children and people over 65.  \n"
        "Examining Chest X-Ray scans is a popular and efficient way of diagnosing Pneumonia.  \n"
        "*SYMPTOMS:*  \n"
        "-Symptoms include a cough with phlegm or pus, fever, chills and difficulty breathing.  \n"
        "-Some other symptoms include dehydration, fatigue, fast breathing, shallow breathing.  \n"
        "*source:* [healthline](https://www.healthline.com/health/pneumonia#is-it-contagious?)")
    st.subheader("Please upload the Chest X-Ray of the patient!")
    file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resize = (cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)) / 255.
        img_reshape = img_resize[np.newaxis, ...]
        prediction = model.predict(img_reshape)
        classes = np.argmax(prediction, axis=1)
        if classes == 0:
            st.subheader('Diagnostic Result:')
            st.write("The following patient is a Normal case")
            session_state.pneu = "Normal"
        else:
            st.subheader('Diagnostic Result:')
            st.write("The following patient has been infected with Pneumonia. We suggest an appointment with a Medical Expert for confirmation.")
            #st.text("Diagnostic probability:" + prob)
            session_state.pneu = "Pneumonia"

elif radio == "Brain Tumour Test":
    model = load_model('/app/btmodel90.hdf5')
    st.write("""
                 # Brain Tumour Diagnostic Test
                 """
             )
    st.write(
        "A cancerous or non-cancerous mass or growth of abnormal cells in the brain. Tumours can start in the brain, or cancer elsewhere in the body can spread to the brain.  \n"
        "Brain MRI scans manifest clear sightings of tumours and hence are effective in diagnosing and locating the tumours.  \n"
        "*SYMPTOMS:*  \n"
        "-Symptoms include new or increasingly strong headaches, blurred vision, loss of balance, confusion and seizures.  \n"
        "-In some cases, there may be no symptoms.  \n"
        "*source:* [healthline](https://www.healthline.com/health/brain-tumor#symptoms)")
    st.subheader("Please upload a Brain MRI of the patient!")
    file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    if file is None:
        st.text("Please upload an image file")
    else:
        image = Image.open(file)
        st.image(image, use_column_width=True)
        size = (64, 64)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image = np.asarray(image)
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img_resize = (cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)) / 255.
        img_reshape = img_resize[np.newaxis, ...]
        prediction = model.predict(img_reshape)
        classes = np.argmax(prediction, axis=1)
        if classes == 0:
            st.subheader('Diagnostic Result:')
            st.write("The following patient is a Normal case")
            session_state.bt = "Normal"
        else:
            st.subheader('Diagnostic Result:')
            st.write("The following patient has been diagnosed with Brain Tumour. We suggest an appointment with a Medical Expert for confirmation.")
            #st.text("Diagnostic probability:" + prob)
            session_state.bt = "Tumour diagnosed"
elif radio == "Patient Report":
    import streamlit as st
    import base64


    def download_link(object_to_download, download_filename, download_link_text):
        """
        Generates a link to download the given object_to_download.

        object_to_download (str, pd.DataFrame):  The object to be downloaded.
        download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
        download_link_text (str): Text to display for download link.

        Examples:
        download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
        download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

        """
        if isinstance(object_to_download, pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)

        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
        link = f'<a href="data:file/csv;base64,{b64}" download="{download_filename}.csv">Download csv file</a>'
        return link

    if session_state.symptoms == "":
        data = [[session_state.name, session_state.gender, session_state.age,session_state.disability, "None", session_state.mal,session_state.covid, session_state.pneu, session_state.bt]]
        new_profile = pd.DataFrame(columns=cols, data=data)
        st.subheader('Patient Report')
        st.table(new_profile)
        if st.button('Download Patient Report'):
            tmp_download_link = download_link(new_profile, session_state.name, 'Click here to download the report!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)

    else:
        data = [[session_state.name, session_state.gender, session_state.age, session_state.disability, session_state.symptoms, session_state.mal, session_state.covid,session_state.pneu, session_state.bt]]
        new_profile = pd.DataFrame(columns=cols, data=data)
        st.subheader('Patient Report')
        st.table(new_profile)
        if st.button('Download Patient Report'):
            tmp_download_link = download_link(new_profile, session_state.name, 'Click here to download the report!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)


    if st.button("Clear Patient Biodata"):
        session_state.name = ""
        session_state.gender = 'Male'
        session_state.disability = 'No'
        session_state.age = 18
        session_state.symptoms =""
        session_state.mal = "Not done"
        session_state.covid = "Not done"
        session_state.pneu = "Not done"
        session_state.bt = "Not done"
        st.write("Biodata cleared from system! Go to biodata page for entering new data")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

#selection = st.sidebar.radio("Go to", list(PAGES.keys()))
#page = PAGES[selection]
#if page == "Malaria":
#    mal = page.app()
#elif page == "Home":
#    name, age, gender = page.app()
#else:
#    page.app()
