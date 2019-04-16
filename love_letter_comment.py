from bs4 import BeautifulSoup as bs
import requests as request
import time
import pymysql
import os

#电影情书评论

pymysql.install_as_MySQLdb()
url = "https://movie.douban.com/subject/1292220/comments?start=%s&limit=20&sort=new_score&status=P"
path = 'C:/Users/jkw/Desktop/豆瓣头像/'

heards = {
    'Cookie': 'll="118282"; bid=LovkMVFZHRc; __yadk_uid=B5lgo43L9OOoYJmbESAgn6wyxeaxYi9H; _vwo_uuid_v2=D4825E1ECC679BB8ED28E1C80223D4C23|321f6b0b47c2dfd0f88d5f7f83687660; douban-fav-remind=1; push_noty_num=0; push_doumail_num=0; __utmz=30149280.1554790751.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.12801; __utmz=223695111.1554790765.3.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/search; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1554797526%2C%22https%3A%2F%2Fwww.douban.com%2Fsearch%3Fsource%3Dsuggest%26q%3D%25E6%2583%2585%25E4%25B9%25A6%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.74472172.1554779479.1554790751.1554797526.3; __utmc=30149280; __utma=223695111.246802348.1554779479.1554790765.1554797526.4; __utmb=223695111.0.10.1554797526; __utmc=223695111; ap_v=0,6.0; __utmb=30149280.1.10.1554797526; ct=y; _pk_id.100001.4cf6=97f546da65c72141.1554779478.4.1554802448.1554790770.; dbcl2="128017193:GGIAMSKd3Mo"',
    'User-Agen':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5603.400 QQBrowser/10.1.1775.400'
}

# 打开数据库连接
db = pymysql.connect("localhost","root","root","python" )
# 使用cursor()方法获取操作游标
cursor = db.cursor()

def save_img(imgurl):
    filename = path+os.path.basename(imgurl)
    r = request.get(imgurl)
    with open(filename, 'wb') as f:
        f.write(r.content)

def insert_sql(args):
    sql = "INSERT INTO movie_comment(movie_name,user_name,comment_info, \
           rating,votes,head_path) \
           VALUES (%(movieName)s, %(userName)s, %(commentInfo)s, %(rating)s, %(votes)s, %(headPath)s)"
    try:
        # 执行sql语句
        cursor.execute(sql,args)
        # 提交到数据库执行
        db.commit()
    except pymysql.Error as e:
        # 发生错误时回滚
        print(e)
        db.rollback()

rating_dict = {'力荐':'5','推荐':'4','还行':'3','较差':'2','很差':'1','无评分':'0'}
i=500
while i < 6004:
    soup = bs(request.get(url%i,headers=heards).text)
    for item in soup.find_all('div', class_='comment-item'):
        avatar = item.find('div', class_='avatar')
        if avatar is None:
            imgurl = ''
        else:
            imgurl = avatar.img['src']
        # save_img(imgurl)
        comment = item.find('div', class_='comment')
        if comment.find('span', class_='votes') is None:
            votes = 0
        else:
            votes = comment.find('span', class_='votes').text
        if comment.find('span', class_='comment-time') is None:
            comment_time = ''
        else:
            comment_time = comment.find('span', class_='comment-time')['title']
        if comment.find('span', class_='comment-info').a is None:
            username = ''
        else:
            username = comment.find('span', class_='comment-info').a.text
        if comment.find('span', class_='rating') is None:
            rating = '无评分'
        else:
            rating = comment.find('span', class_='rating')['title']
        if comment.find('span', class_='short') is None:
            short = ''
        else:
            short = comment.find('span', class_='short').text
        args = {'movieName': '情书', 'userName': username, 'commentInfo': short, 'rating': int(rating_dict.get(rating)),
                'votes': int(votes), 'headPath': imgurl}
        insert_sql(args)
    print('第%s页评论爬取完毕'%(i/20+1))
    time.sleep(3)
    i=i+20
db.close()