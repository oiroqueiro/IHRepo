def filter_videos(_filtertext):
    """Function to filter the videos in Django
    
    Keyword arguments:
    _filtertext: Text to filter
    Return: id List
    """
    #Connect to mysql
    import mysql.connector

    connection = mysql.connector.connect(user='****', #your user
                            password='*****', #your_password
                            host='*****') #your host

    id_list = []
    if connection.is_connected():
        cursor = connection.cursor()

        query = """SELECT distinct id 
                    FROM ironrep.video_texts 
                    WHERE video_text like concat('%',%s,'%') 
                    ORDER BY id"""
        val = [str(_filtertext)]

        cursor.execute(query, val)

        query_table = cursor.fetchall()
        if (len(query_table)>0):  
            for q in query_table:
                id_list.append(q[0])

    else:
        print("No connection to database.")    
    
    return id_list
    
def video_player(_videoid, _langid, _position = 0):
    """Function to launch the video with subtitles
    
    Keyword arguments:
    _conn: connection object
    _videoid: the id of the video
    _langid: the id of the language to use for the subtitles
    _position: time in seconds to start the video
    Return: None
    """

    import os
    from pathlib import Path
    #Connect to mysql
    import mysql.connector
    #Pandas
    import pandas as pd

    connection = mysql.connector.connect(user='root',
                            password='p1ssw4rd',
                            host='localhost')
    if connection.is_connected():
        cursor = connection.cursor() 
        query = """SELECT video_player, temp_directory
                            FROM ironrep.configuration 
                            LIMIT 1;"""

        cursor.execute(query)
        conf_table = cursor.fetchall()
        conf_df = pd.DataFrame(conf_table)
        conf_df.columns = [i[0] for i in cursor.description]

        query = """SELECT subtitles
                        FROM ironrep.subtitles
                    WHERE videoid = %s
                        AND languageid = %s"""
        val = [int(_videoid), _langid]
        cursor.execute(query, val)   
        print(cursor.statement) 
        subt_table = cursor.fetchall()
        if (len(subt_table)>0):
            subt_df = pd.DataFrame(subt_table)
            subt_df.columns = [i[0] for i in cursor.description]
            
            #os.remove(Path(list(conf_df['temp_directory'])[0]+"/play_subtitle.srt"))
            with open(Path(list(conf_df['temp_directory'])[0]+"/play_subtitle.srt"), "w+") as f:
                f.write(list(subt_df['subtitles'])[0])
            
            query = """SELECT video_path
                        FROM ironrep.videos
                        WHERE id = %s"""
            val = [int(_videoid)]
            cursor.execute(query, val)
            video_table = cursor.fetchall()
            video_df = pd.DataFrame(video_table)
            video_df.columns = [i[0] for i in cursor.description]            
            os.system(list(conf_df['video_player'])[0].replace('{videoparam}',list(video_df['video_path'])[0]).replace('{subtitleparam}',list(conf_df['temp_directory'])[0]+"/play_subtitle.srt").replace('{positionparam}',str(_position)))
        else:
            print(f'No subtitles found in language {_langid}')

def search_pos_video(_subitles,_text):
    """Function to locate the positions of the subtitles
       where the text to search is located.
       This function will use to find text inside a video

    Keyword arguments:
    _subtitles: the subtitles of the video
    _text: text to find
    Return: a list of tuples with the positition (seconds) and the time
    """
    import re

    #print(_subitles)
    #print(_text)

    pos_find = [re.findall('(\d{2}:\d{2}:\d{2},\d{3})',_subitles[:i.start()])[-2].split(':') for i in re.finditer(_text.lower(), _subitles.lower())]
    positions_final = [(int(pos[0])*3600+int(pos[1])*60+int(float(pos[2].replace(',','.'))),':'.join(pos)) for pos in pos_find]
    return positions_final
