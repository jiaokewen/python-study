from bs4 import BeautifulSoup as bs
import requests as request
import time
import json
import pymysql
import os

def save_img(imgurl,nikename):
    filename = path+nikename+'.jpg'
    r = request.get(imgurl)
    with open(filename, 'wb') as f:
        f.write(r.content)
    return filename

def insert_sql(args):
    sql = "INSERT INTO music_comment(comment_id,nick_name,user_id, \
           liked,content,liked_count,avatar_url) \
           VALUES (%(commentId)s, %(nickname)s, %(userId)s, %(liked)s, %(content)s, %(likedCount)s, %(avatarUrl)s)"
    try:
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交到数据库执行
        db.commit()
    except pymysql.Error as e:
        # 发生错误时回滚
        print(e)
        db.rollback()

def prase_item (item):
    commentId = item.get('commentId')
    nickname = item.get('user').get('nickname')
    userId = item.get('user').get('userId')
    liked = 0 if item.get('liked') else 1
    content = item.get('content')
    likedCount = item.get('likedCount')
    avatarUrl = save_img(item.get('user').get('avatarUrl'),nickname)
    args = {'commentId':commentId,'nickname':nickname,'userId':userId,'liked':liked,'content':content,
            'likedCount':likedCount,'avatarUrl':avatarUrl}
    insert_sql(args)

if __name__ == '__main__':
    api = 'http://music.163.com/api/v1/resource/comments/R_SO_4_441491828?limit=20&offset=%s'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5603.400 QQBrowser/10.1.1775.400'}
    path = 'C:/Users/jkw/Desktop/云音乐头像/'

    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "root", "python")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    i = 0
    while i < 312480:
        try:
            print('正在爬取第%s页评论' % (i / 20 + 1))
            resp = request.get(api % i, headers=headers)
            if resp.status_code == 200:
                resp_json = json.loads(resp.text)
                hotComments = resp_json.get('hotComments')
                comments = resp_json.get('comments')
                if hotComments != None:
                    for item in hotComments:
                        prase_item(item)
                for item in comments:
                    prase_item(item)
            resp.close()
            i = i + 20
        except Exception as e:
            print(e)
    db.close()
