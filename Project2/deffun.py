import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepe"
)
my_sql_cursor = mydb.cursor(buffered=True)

def replace_state_name(datas):
    datas['State']=datas['State'].str.replace('-',' ')
    datas['State']=datas['State'].str.title()
    datas['State'].replace("Andaman & Nicobar Islands", "Andaman & Nicobar",inplace = True)
    datas['State'].replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu",inplace = True)
    return datas

def get_aTrans():
    sql_query = f"""select State,Year,Quater,Trans_type,sum(Trans_count),sum(Trans_amount) from Aggregated_trans group by State,Year,Quater,Trans_type"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','Trans_type','count','Amount']) 
    df = replace_state_name(df)
    return df

def get_aUser():
    sql_query = f"""select State,Year,Quater,brand,count from Aggregated_user group by State,Year,Quater"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','Brand','count']) 
    df = replace_state_name(df)
    return df

def get_mTrans():
    sql_query = f"""select State,Year,Quater,District_name,Trans_count,Trans_amount from map_trans group by State,Year,Quater,District_name"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','District','Count','Amount']) 
    df = replace_state_name(df)
    return df

def get_mUser():
    sql_query = f"""select State,Year,Quater,District,registeredUsers,appOpens from map_user group by State,Year,Quater,District"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','District','Reg user','App Opens']) 
    df = replace_state_name(df)
    return df

def get_tTrans():
    sql_query = f"""select State,Year,Quater,District,count,amount from top_trans group by State,Year,Quater,District"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','District','Count','Amount']) 
    df = replace_state_name(df)
    return df

def get_tUser():
    sql_query = f"""select State,Year,Quater,District,reg_users from top_user group by State,Year,Quater,District"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Year','Quater','District','Reg user']) 
    df = replace_state_name(df)
    return df

def q1():#Top 10 Transaction in Overall India
    sql_query = f"""select State,sum(Trans_count) from Aggregated_trans group by State"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Count'])
    df = replace_state_name(df)
    df.sort_values("Count",ascending=False,inplace=True)
    return df.head(10)
def q2():#Top 5 Brand and thier count
    sql_query = f"""select distinct(brand),sum(count) as totalCount from aggregated_user group by brand ORDER by totalCount DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Brand','Count'])
    return df.head(5)
def q3():#Top 10 District Transaction in overall India
    sql_query = f"""SELECT distinct(district_name), SUM(Trans_amount) as TransAmount from map_trans GROUP by District_name"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['District','Amount'])
    df.sort_values("Amount",ascending=False,inplace=True)
    return df.head(10)
def q4():#Top 3 District Transaction on each state
    sql_query = f"""SELECT distinct(district_name),state, SUM(Trans_amount) as TransAmount,RANK() OVER (PARTITION BY state ORDER BY TransAmount) as Rank from map_trans GROUP by state,District_name ORDER BY state,Rank DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['District','State','Amount','Rank']) 
    df = replace_state_name(df)
    return df[df["Rank"] <= 3]
def q5():#Top 10 Registered Users in overall India
    sql_query = f"""SELECT distinct(District), SUM(registeredUsers) as regUser from map_user GROUP by District"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['District','Count']) 
    #df = replace_state_name(df)
    return df
def q6():#Top 3 Pincode Transaction on each state
    sql_query = f"""SELECT distinct(District),state, SUM(amount) as TransAmount ,RANK() OVER (PARTITION BY state ORDER BY TransAmount) as Rank from top_trans GROUP by state,District ORDER BY state,Rank DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['District','State','Amount','Rank']) 
    df = replace_state_name(df)
    return df[df["Rank"] <= 3]
def q7():#Top 10 Registered Users by pincode and their count
    sql_query = f"""select distinct(District),State,sum(reg_users) as totalCount from top_user group by State,District ORDER by State"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['District','State','Count']) 
    df = replace_state_name(df)
    return df.head(10)
def q8():#which quater return highest transaction on each state
    sql_query = f"""select DISTINCT(Quater),State,year,SUM(Trans_amount) as TransAmount from aggregated_trans group by State,Year,Quater"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Quater','State','year','Amount']) 
    df = replace_state_name(df)
    return df
def q9():#Total Transaction group by Transaction Types and their respective state
    sql_query = f"""select State,Trans_type,SUM(Trans_amount) as TransAmount from aggregated_trans group by State,Trans_type"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['State','Type','Amount']) 
    df = replace_state_name(df)
    return df

def format_cash(amount):
    def truncate_float(number, places):
        return '{:,.2f}'.format(int(number * (10 ** places)) / 10 ** places)
    if amount < 1e3:
        return amount

    if 1e3 <= amount < 1e5:
        return str(truncate_float((amount / 1e5) * 100, 2)) + " K"

    if 1e5 <= amount < 1e7:
        return str(truncate_float((amount / 1e7) * 100, 2)) + " L"

    if amount > 1e7:
        return str(truncate_float(amount / 1e7, 2)) + " Cr"