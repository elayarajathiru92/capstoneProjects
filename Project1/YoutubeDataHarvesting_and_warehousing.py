from Connections import sql_connection,mongo_db,youtube,collections,my_sql_cursor
from YoutubeDataFetch import InsertMongoDBData
import streamlit as st
from streamlit_option_menu import option_menu
from QuestionsDataFetch import questions,sql_q1,sql_q2,sql_q3,sql_q4,sql_q5,sql_q6,sql_q7,sql_q8,sql_q9,sql_q10
import pandas as pd

#creating sidebar menus
with st.sidebar:
    selected = option_menu("Main Menu",["Home","Extract & Transform","View"],
                           icons=['house','database-fill-add','view-stacked'],menu_icon="cast",default_index=0)

#Function to get existing channels from mongoDB
def channel_names():
    x=collections.find()
    chn_name={}
    for i in x:
        chn_name[i["channel_detail"][0]["Channel_name"]]=i["channel_detail"][0]["Channel_id"]
    return chn_name

# Home page data
if selected == "Home":
    st.write("## :blue[Project Title] : YouTube Data Harvesting and Warehousing using MySQL, MongoDB and Streamlit")
    st.write("## :blue[Technology used] : Python,MongoDB, Youtube Data API, MySQL, Streamlit")
    st.write("## :blue[Domain] : Social Media")
    st.write("## :blue[Overview] : Retrieving the Youtube channels data from the Google API, storing it in a MongoDB as data lake, migrating and transforming data into a SQL database,then querying the data and displaying it in the Streamlit app.")
    
# Extrace & Transform page data
if selected == "Extract & Transform":
    tab1, tab2 = st.tabs(["Extract", "Transform"])
    with tab1:
        st.write("Enter the Youtube Channel id :")
        channel_ids = st.text_input("Hint : If providing more than one channels with ',' then provide next channel id.").split(',')
        existsChannels=channel_names()
        for chn_id in channel_ids:
            if st.button("Upload to MongoDB"):
                with st.spinner('Please Wait for it...'):
                    if len(existsChannels)>= 0 and (chn_id in existsChannels.values()) == False:
                        chn=InsertMongoDBData(chn_id)
                        collections.insert_one(chn)
                        st.success("Upload to MogoDB successful !!")
                    else:
                        st.warning("Already Data updated to MongoDB for this Channel : " + chn_id)


    with tab2:
        st.write("Select a channel to begin Transformation to SQL")
        existsChannels=channel_names()
        if len(existsChannels)>0:
            selected_channel = st.selectbox('',options = list(existsChannels.keys()))
            selected_channelId = existsChannels[selected_channel]
        else:
            selected_channel = st.selectbox('',options = "", index=None,placeholder="Select channel...")
            selected_channelId = 0
        Migrate = st.button('**Migrate to MySQL**')

        try:
            my_sql_cursor.execute("SELECT Channel_id FROM channels")
            myresult = my_sql_cursor.fetchall()
        except:
            myresult=[]

        mysql_channelIds=[]
        for i in myresult:
            mysql_channelIds.append(i[0])
        my_sql_cursor.close()

        
        if Migrate:
            with st.spinner('Please Wait for it...'):
                if len(mysql_channelIds)>=0 and (selected_channelId not in mysql_channelIds):
                    # Retrieve the document with the specified name
                    result = collections.find_one({"_id": selected_channelId})
                    # Data Conversion
                    # channel details conversion
                    channel_df = pd.DataFrame.from_dict(result["channel_detail"][0], orient='index').T
                    channel_df.to_sql(con=sql_connection,name='channels', if_exists='append',index=False)

                    # vedio details conversion
                    vedios_df = pd.DataFrame(result["vedio_detail"])
                    vedios_df.to_sql(con=sql_connection,name='vedios', if_exists='append',index=False)

                    # comment details conversion
                    Comments_df = pd.DataFrame(result["comment_detail"])
                    Comments_df.to_sql(con=sql_connection,name='comments', if_exists='append',index=False)

                    st.success("Transfered to MySQL successful !!")
                else:
                    st.warning(f"Already for this channel - {selected_channel} - data is transfered to MySQL")
                
    
# View page data
if selected == "View":
    st.write("## :orange[Select any question to get Insights]")
    selected_Ques = st.selectbox('**Select Any Question', options = list(questions.values()), key='question_names')
    for key, val in questions.items():
        if val == selected_Ques:
            selected_QuesId=key
    
    if selected_QuesId == 1:
        st.dataframe(sql_q1(),hide_index=True)
    elif selected_QuesId == 2:
        st.dataframe(sql_q2(),hide_index=True)
    elif selected_QuesId == 3:
        st.dataframe(sql_q3(),hide_index=True)
    elif selected_QuesId == 4:
        st.dataframe(sql_q4(),hide_index=True)
    elif selected_QuesId == 5:
        st.dataframe(sql_q5(),hide_index=True)
    elif selected_QuesId == 6:
        st.dataframe(sql_q6(),hide_index=True)
    elif selected_QuesId == 7:
        st.dataframe(sql_q7(),hide_index=True)
    elif selected_QuesId == 8:
        st.dataframe(sql_q8(),hide_index=True)
    elif selected_QuesId == 9:
        st.dataframe(sql_q9(),hide_index=True)
    elif selected_QuesId == 10:
        st.dataframe(sql_q10(),hide_index=True)
