from Connections import youtube
import streamlit as st
import re

def convert_duration(duration):
#    parsed_duration = re.search(f"PT(\d+H)?(\d+M)?(\d+S)", duration).groups()
#    duration_str = ""
#    for d in parsed_duration:
#        if d:
#            duration_str += f"{d[:-1]}:"
#    duration_str = duration_str.strip(":")
#    return duration_str
    regex = r'PT(\d+H)?(\d+M)?(\d+S)?'
    match = re.match(regex, duration)
    if not match:
        return '00:00:00'
    hours, minutes, seconds = match.groups()
    hours = int(hours[:-1]) if hours else 0
    minutes = int(minutes[:-1]) if minutes else 0
    seconds = int(seconds[:-1]) if seconds else 0
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return '{:02d}:{:02d}:{:02d}'.format(int(total_seconds / 3600), int((total_seconds % 3600) / 60), int(total_seconds % 60))

# Function to get channel details data
def get_channel_details(channel_id):
    try:
        ch_data = []
        try:
            response = youtube.channels().list(part = 'snippet,contentDetails,statistics',id= channel_id).execute()

            for i in range(len(response['items'])):
                data = dict(Channel_id = response['items'][i]['id'],
                            Channel_name = response['items'][i]['snippet']['title'],
                            Description = response['items'][i]['snippet']['description'],
                            Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                            Subscribers = int(response['items'][i]['statistics']['subscriberCount']),
                            Views = int(response['items'][i]['statistics']['viewCount']),
                            Total_videos = int(response['items'][i]['statistics']['videoCount']),
                            Country = response['items'][i]['snippet'].get('country')
                            )
                ch_data.append(data)
            
        except:
            pass

        return ch_data
    except Exception as e:
        st.exception(e)


# Function to get vedio id from channel
def get_channel_videoids(channel_id):
    try:
        video_ids = []
        playlist_id = (get_channel_details(channel_id))[0]['Playlist_id']
        next_page_token = None
        
        while True:
            try:
                res = youtube.playlistItems().list(playlistId=playlist_id, 
                                                part='snippet', 
                                                maxResults=50,
                                                pageToken=next_page_token).execute()
                
                for i in range(len(res['items'])):
                    video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token = res.get('nextPageToken')
                
                if next_page_token is None:
                    break
            except:
                pass

        return video_ids
    except Exception as e:
        st.exception(e)


# Function to get vedio details from Youtube API
def get_video_details(v_ids):
    try:
        videos = []
    
        for vid in v_ids:
            try:
                response = youtube.videos().list(part="snippet,contentDetails,statistics",id=vid).execute()
                for video in response['items']:
                    video_details = dict(Channel_name = video['snippet']['channelTitle'],
                                        Channel_id = video['snippet']['channelId'],
                                        Video_id = video['id'],
                                        Title = video['snippet']['title'],
                                        Tags = ','.join(video['snippet'].get('tags',["NA"])),
                                        Thumbnail = video['snippet']['thumbnails']['default']['url'],
                                        Description = video['snippet']['description'],
                                        Published_date = video['snippet']['publishedAt'],
                                        Duration = convert_duration(video['contentDetails']['duration']),
                                        Views = int(video['statistics']['viewCount']),
                                        Likes = int(video['statistics'].get('likeCount')),
                                        Dis_likes = int(video['statistics'].get('dislikeCount',0)),
                                        Comments = int(video['statistics'].get('commentCount','0')),
                                        Favorite_count = int(video['statistics']['favoriteCount']),
                                        Definition = video['contentDetails']['definition'],
                                        Caption_status = video['contentDetails']['caption']
                                    )
                    videos.append(video_details)
            except:
                pass

        return videos
    except Exception as e:
        st.exception(e)

# FUNCTION TO GET COMMENT DETAILS
def get_comments_details(v_id):
    try:
        comment_data = []
        try:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=v_id).execute()
            
            for cmt in response['items']:
                data = dict(Comment_id = cmt['id'],
                            Video_id = cmt['snippet']['videoId'],
                            Comment_text = cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_author = cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_posted_date = cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                            Like_count = int(cmt['snippet']['topLevelComment']['snippet']['likeCount']),
                            Reply_count = int(cmt['snippet']['totalReplyCount'])
                            )
                comment_data.append(data)
        except:
            pass

        return comment_data
    except Exception as e:
        st.exception(e)
# Function to insert all the record into one dict
def InsertMongoDBData(chn_id):
    ch_details = get_channel_details(chn_id)
    v_ids = get_channel_videoids(chn_id)
    vid_details = get_video_details(v_ids)

    def comments():
        com_d = []
        for i in v_ids:
            com_d+= get_comments_details(i)
        return com_d
    comm_details = comments()

    channels={
        "_id":chn_id,
        "channel_detail":ch_details,
        "vedio_detail":vid_details,
        "comment_detail":comm_details
    }
    return channels