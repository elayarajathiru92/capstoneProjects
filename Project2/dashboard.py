import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from deffun import get_aTrans,get_aUser,get_mTrans,get_mUser,get_tTrans,get_tUser,format_cash,q1,q2,q3,q4,q5,q6,q7,q8,q9
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Phonepe Pulse",page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Phonepe Pulse")
st.markdown("""
            <style> 
            div[data-testid="block-container"] {padding: 1rem;}
            div[data-testid="stMetric"] {
                background-color: PaleTurquois;
                border: 1px solid rgba(28, 131, 225, 0.1);
                padding: 5% 5% 5% 10%;~
                border-radius: 5px;
                color: rgb(30, 103, 119);
                overflow-wrap: break-word;
            }

            /* breakline for metric text         */
            div[data-testid="stMetric"] > label[data-testid="stMetricLabel"] > div {
                overflow-wrap: break-word;
                white-space: break-spaces;
                color: red;
            }
            </style>
            """, unsafe_allow_html=True,)

df_a_TransList = get_aTrans()
df_a_UserList = get_aUser()
df_m_TransList = get_mTrans()
df_m_UserList = get_mUser()
df_t_TransList = get_tTrans()
df_t_UserList = get_tUser()

with st.sidebar:
    selected = option_menu("", ["Home","Report", 'Insight'], 
        icons=['house','database-fill-add','view-stacked'],menu_icon="cast",default_index=0)
    selectedstate= st.sidebar.multiselect("pick your state",df_a_TransList["State"].unique())
    selectedYear=st.multiselect("Select the year",df_a_TransList["Year"].unique())
    selectedQuater=st.multiselect("Select the year",df_a_TransList["Quater"].unique())

    if not selectedstate and not selectedYear and not selectedQuater:
        df_filter_atransList = df_a_TransList.copy()
        df_filter_auserList = df_a_UserList.copy()
        df_filter_mtransList = df_m_TransList.copy()
        df_filter_muserList = df_m_UserList.copy()
        df_filter_ttransList = df_t_TransList.copy()
        df_filter_tuserList = df_t_UserList.copy()
    elif not selectedstate and not selectedYear:
        df_filter_atransList = df_a_TransList[df_a_TransList["Quater"].isin(selectedQuater)]
        df_filter_auserList = df_a_UserList[df_a_UserList["Quater"].isin(selectedQuater)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Quater"].isin(selectedQuater)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Quater"].isin(selectedQuater)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Quater"].isin(selectedQuater)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Quater"].isin(selectedQuater)]
    elif not selectedstate and not selectedQuater:
        df_filter_atransList = df_a_TransList[df_a_TransList["Year"].isin(selectedYear)]
        df_filter_auserList = df_a_UserList[df_a_UserList["Year"].isin(selectedYear)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Year"].isin(selectedYear)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Year"].isin(selectedYear)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Year"].isin(selectedYear)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Year"].isin(selectedYear)]
    elif not selectedYear and not selectedQuater:
        df_filter_atransList = df_a_TransList[df_a_TransList["State"].isin(selectedstate)]
        df_filter_auserList = df_a_UserList[df_a_UserList["State"].isin(selectedstate)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["State"].isin(selectedstate)]
        df_filter_muserList = df_m_UserList[df_m_UserList["State"].isin(selectedstate)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["State"].isin(selectedstate)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["State"].isin(selectedstate)]
    elif not selectedstate:
        df_filter_atransList = df_a_TransList[(df_a_TransList["Year"].isin(selectedYear) & df_a_TransList["Quater"].isin(selectedQuater))]
        df_filter_auserList = df_a_UserList[df_a_UserList["Year"].isin(selectedYear) & df_a_UserList["Quater"].isin(selectedQuater)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Year"].isin(selectedYear) & df_m_TransList["Quater"].isin(selectedQuater)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Year"].isin(selectedYear) & df_m_UserList["Quater"].isin(selectedQuater)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Year"].isin(selectedYear) & df_t_TransList["Quater"].isin(selectedQuater)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Year"].isin(selectedYear) & df_t_UserList["Quater"].isin(selectedQuater)]
    elif not selectedYear:
        df_filter_atransList = df_a_TransList[(df_a_TransList["Quater"].isin(selectedQuater) & df_a_TransList["State"].isin(selectedstate))]
        df_filter_auserList = df_a_UserList[df_a_UserList["Quater"].isin(selectedQuater) & df_a_UserList["State"].isin(selectedstate)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Quater"].isin(selectedQuater) & df_m_TransList["State"].isin(selectedstate)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Quater"].isin(selectedQuater) & df_m_UserList["State"].isin(selectedstate)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Quater"].isin(selectedQuater) & df_t_TransList["State"].isin(selectedstate)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Quater"].isin(selectedQuater) & df_t_UserList["State"].isin(selectedstate)]
    elif not selectedQuater:
        df_filter_atransList = df_a_TransList[(df_a_TransList["Year"].isin(selectedYear) & df_a_TransList["State"].isin(selectedstate))]
        df_filter_auserList = df_a_UserList[df_a_UserList["Year"].isin(selectedYear) & df_a_UserList["State"].isin(selectedstate)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Year"].isin(selectedYear) & df_m_TransList["State"].isin(selectedstate)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Year"].isin(selectedYear) & df_m_UserList["State"].isin(selectedstate)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Year"].isin(selectedYear) & df_t_TransList["State"].isin(selectedstate)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Year"].isin(selectedYear) & df_t_UserList["State"].isin(selectedstate)]
    else:
        df_filter_atransList = df_a_TransList[(df_a_TransList["Year"].isin(selectedYear) & df_a_TransList["State"].isin(selectedstate) & df_a_TransList["Quater"].isin(selectedQuater))]
        df_filter_auserList = df_a_UserList[df_a_UserList["Year"].isin(selectedYear) & df_a_UserList["State"].isin(selectedstate) & df_a_UserList["Quater"].isin(selectedQuater)]
        df_filter_mtransList = df_m_TransList[df_m_TransList["Year"].isin(selectedYear) & df_m_TransList["State"].isin(selectedstate) & df_m_TransList["Quater"].isin(selectedQuater)]
        df_filter_muserList = df_m_UserList[df_m_UserList["Year"].isin(selectedYear) & df_m_UserList["State"].isin(selectedstate) & df_m_UserList["Quater"].isin(selectedQuater)]
        df_filter_ttransList = df_t_TransList[df_t_TransList["Year"].isin(selectedYear) & df_t_TransList["State"].isin(selectedstate) & df_t_TransList["Quater"].isin(selectedQuater)]
        df_filter_tuserList = df_t_UserList[df_t_UserList["Year"].isin(selectedYear) & df_t_UserList["State"].isin(selectedstate) & df_t_UserList["Quater"].isin(selectedQuater)]
        
if selected == "Home":
    st.write("Home")
if selected == "Report":
    metric1,metric2,metric3 = st.columns(3,gap='large')
    with metric1:
        st.metric(label="Total Transaction", value=format_cash(df_filter_atransList['Amount'].sum()),help=f"""Total State Transaction Amount: {format_cash(df_filter_atransList['Amount'].sum())}""")
    with metric2:
        st.metric(label="Total Transaction", value=format_cash(df_filter_atransList['Amount'].sum()),help=f"""Total District Transaction Amount: {format_cash(df_filter_atransList['Amount'].sum())}""")
    with metric3:
        st.metric(label="Total brand", value=format_cash(df_filter_atransList['Amount'].sum()),help=f"""Total Brand & the count: {format_cash(df_filter_atransList['Amount'].sum())}""")

    tab1,tab2=st.tabs(["DataFrame","Charts"])
    with tab1:
        st.dataframe(df_filter_atransList)
        st.dataframe(df_filter_auserList)
        st.dataframe(df_filter_mtransList)
        st.dataframe(df_filter_ttransList)
    with tab2:
        #fig1 = px.bar(df_filter_atransList,x="State", y =df_filter_atransList["Quater"], title = 'State Quater wise',text_auto=True)
        fig=px.bar(df_filter_atransList,x="State",y="count",color="Trans_type",text_auto=True,width=1200,height=600)
        st.plotly_chart(fig)
        fig1=px.sunburst(df_filter_atransList, path=['State','Year', 'Quater'], values='count')
        st.plotly_chart(fig1)
        fig2 = px.choropleth(
        df_filter_atransList,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='count',
        color_continuous_scale='Reds'
        )
        fig2.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig2)


if selected == "Insight":
    questions=[
        "Top 10 Transaction in Overall India",
        "Top 5 Brand and thier count",
        "Top 10 District Transaction in overall India",
        "Top 3 District Transaction on each state?",
        "Top 10 Registered Users in overall India?",
        "Top 3 Pincode Transaction on each state?",
        "Top 10 Registered Users by pincode and their count?",
        "which quater return highest transaction on each state",
        "Total Transaction group by Transaction Types and their respective state"
    ]
    selected_Ques = st.selectbox('**Select Any Question', options = questions, index=None,placeholder="Select Question...")

    if selected_Ques == "Top 10 Transaction in Overall India":
        df=q1()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.bar(df, x='State', y='Count')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 5 Brand and thier count":
        df=q2()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.pie(df, values='Count', names='Brand')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 10 District Transaction in overall India":
        df=q3()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.bar(df, x='District', y='Amount')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 3 District Transaction on each state?":
        df=q4()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            #fig = px.treemap(df, path=[px.Constant('India'), 'State', 'District'], values=['Amount','State'],color='District')
            fig = px.bar(df, x='District', y='Amount')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 10 Registered Users in overall India?":
        df=q5()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.bar(df, x='District', y='Count')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 3 Pincode Transaction on each state?":
        df=q6()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.bar(df, x='District', y='Amount')
            st.plotly_chart(fig)
    elif selected_Ques == "Top 10 Registered Users by pincode and their count?":
        df=q7()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.bar(df, x='District', y='Count')
            st.plotly_chart(fig)
    elif selected_Ques == "which quater return highest transaction on each state":
        df=q8()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            #fig = px.treemap(df, path=[px.Constant('India'), 'State', 'year'], values='Amount',color='Quater', hover_data=['iso_alpha'])
            #st.plotly_chart(fig)
            st.dataframe(df,hide_index=True)
    elif selected_Ques == "Total Transaction group by Transaction Types and their respective state":
        df=q9()
        col1,col2=st.columns([1.3,3])
        with col1:
            st.dataframe(df,hide_index=True)
        with col2:
            fig = px.sunburst(df, path=['State', 'Type'], values='Amount',color='Type')
            st.plotly_chart(fig)
