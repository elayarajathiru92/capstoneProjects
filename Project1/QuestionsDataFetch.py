import pandas as pd
from Connections import my_sql_cursor

questions={
        1:"What are the names of all the videos and their corresponding channels?",
        2:"Which channels have the most number of videos, and how many videos do they have?",
        3:"What are the top 10 most viewed videos and their respective channels?",
        4:"How many comments were made on each video, and what are their corresponding video names?",
        5:"Which videos have the highest number of likes, and what are their corresponding channel names?",
        6:"What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
        7:"What is the total number of views for each channel, and what are their corresponding channel names?",
        8:"What are the names of all the channels that have published videos in the year 2022?",
        9:"What is the average duration of all videos in each channel, and what are their corresponding channel names?",
        10:"Which videos have the highest number of comments, and what are their corresponding channel names?"
    }

def q1(): # what are the names of all the videos and their corresponding channels?
    sql_query = f"""select Title,Channel_name from vedios"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Vedio Name', 'Channel Name'])# Fetch the result into a Pandas DataFrame
    return df

def q2(): # Which channels have the most number of videos, and how many videos do they have?,
    sql_query=f"""SELECT Channel_name, Total_videos FROM channels ORDER BY Total_videos DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['channel Name','vedio count'])# Fetch the result into a Pandas DataFrame
    return df

def q3(): # What are the top 10 most viewed videos and their respective channels
    sql_query=f"""SELECT Channel_name,Title,Views FROM vedios ORDER BY Views DESC LIMIT 10"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['channel Name','vedio','Total views'])# Fetch the result into a Pandas DataFrame
    return df

def q4():# How many comments were made on each video, and what are their corresponding video names
    sql_query=f"""SELECT Title,Comments FROM vedios"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['vedio','Total Comment'])# Fetch the result into a Pandas DataFrame
    return df

def q5():#Which videos have the highest number of likes, and what are their corresponding channel names
    sql_query=f"""SELECT Channel_name,Title,Likes FROM vedios ORDER BY Likes DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['channel Name','vedio','Total Like Count'])# Fetch the result into a Pandas DataFrame
    return df

def q6():#What is the total number of likes and dislikes for each video, and what are their corresponding video names
    sql_query=f"""SELECT Title,Likes,Dis_likes FROM vedios ORDER BY Likes DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['vedio','Total Likes','Total DisLike'])# Fetch the result into a Pandas DataFrame
    return df

def q7():#What is the total number of views for each channel, and what are their corresponding channel names
    sql_query=f"""SELECT Channel_name,Views FROM channels"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Channel Name','Total Views'])# Fetch the result into a Pandas DataFrame
    return df

def q8():# What are the names of all the channels that have published videos in the year 2022
    sql_query=f"""SELECT DISTINCT(Channel_name) FROM vedios WHERE YEAR(Published_date) = 2022"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Channel Name'])# Fetch the result into a Pandas DataFrame
    return df

def q9():# What is the average duration of all videos in each channel, and what are their corresponding channel names
    sql_query=f"""SELECT Channel_name,AVG(Duration) AS duration FROM vedios GROUP by Channel_name ORDER BY duration DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Channel Name','Duration'])# Fetch the result into a Pandas DataFrame
    return df

def q10():# Which videos have the highest number of comments, and what are their corresponding channel names
    sql_query=f"""SELECT Channel_name,Title,Comments FROM vedios ORDER BY Comments DESC"""
    my_sql_cursor.execute(sql_query)
    result = my_sql_cursor.fetchall()
    df = pd.DataFrame(result, columns=['Channel Name','Vedio Name','Comment Count'])# Fetch the result into a Pandas DataFrame
    return df
