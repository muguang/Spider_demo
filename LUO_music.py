#coding:utf-8

__auther  = "JH"


import requests
from bs4 import BeautifulSoup
import time
import re
import os


LUO_url = "http://www.luoo.net/music/{}"
music_url = "http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio{}/{}.mp3"
#  http://luoo-mp3.kssws.ks-cdn.com/low/luoo/radio805/01.mp3

def get_song_list(volumn):
    r = requests.get(LUO_url.format(volumn))
    bs = BeautifulSoup(r.content, 'lxml')
    songs = bs.find_all('div', 'player-wrapper')
    music_info = []
    cover_dic = {}
    for song in songs:
        # print(song)
        info = []
        name = song.find('p', 'name').getText()
        artist = song.find('p', 'artist').getText()
        album = song.find('p', 'album').getText()
        cover_url = song.find('img')['src']
        info.append(name)
        info.append(artist)
        info.append(album)
        # print(name, artist, album)
        music_info.append(info)
        cover_dic[album[7:]] = cover_url
    print("Debug: ", music_info)
    return music_info, cover_dic

def download_cover(cover_dic):

    for album_name, cover_url in cover_dic.items():
        suffix = re.findall('.+cover(.+)\?.+', cover_url)
        cover_name = str(album_name)+suffix[0]
        # print(cover_name)

        with open(cover_name, "wb") as f:
            time.sleep(0.1)
            f.write(requests.get(cover_url).content)
#

def download_music(music_name):
    len_l = len(music_name)

    for i in range(1, len_l+1):
        track = "%02d" % i
        music_url_temp = music_url.format(number, track)
        # print(music_url_temp)
        # print(music_name[i-1], music_url_temp)
        music = music_name[i-1]+".mp3"
        with open(music, "wb") as f:
            print("downing: ", music)
            f.write(requests.get(music_url_temp).content)
            time.sleep(0.1)


def init(number):


    #  create the cataloge if not exist
    #  if the cataloge have the content or is just a empty folder

    path = os.getcwd()
    path_name = path+"/"+str(number)
    # print(path_name)
    # print(type(path_name))

    if not os.path.exists(path_name):
        os.mkdir(path_name)
    file_size = os.path.getsize(path_name)

    # print(file_size)
    # print(type(file_size))

    if file_size > 100:
        print("这期歌应该已经下载过了..")
        exit()

    os.chdir(path_name)
    # print(os.getcwd())

    music_list, coverdict = get_song_list(number)

    print(music_list, coverdict)

    music_name = []
    for music in music_list:
        music_name.append(music[0])
    download_music(music_name)

    download_cover(cover_dic=coverdict)

if __name__ == '__main__':

    number = input("下载哪一期音乐 >")
    init(number)