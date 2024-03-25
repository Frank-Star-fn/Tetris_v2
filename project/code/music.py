import tkinter as tk
import pygame
import random


Volume = 0.6 # 0.1 # bgm音量大小
music_on = True


def play_random_music():
    global music_on
    if music_on:
        music_on = False
        pygame.mixer.music.stop() # 停止音乐
    else:
        music_on = True
        play_next()


def play_next():
    global music_on
    if music_on: # 打开了音乐
        if not pygame.mixer.music.get_busy(): # 当前没有播放歌曲
            random_song = random.choice(music_list)  # 随机选择下一首音乐
            pygame.mixer.music.load(random_song)
            pygame.mixer.music.play()


pygame.init()

music_list = [
    r"music\music1.MP3",
    r"music\music2.MP3",
    r"music\music3.MP3",
    r"music\music4.MP3",
    r"music\music5kids.MP3",
    r"music\music6.MP3",
    r"music\music7.MP3",
    r"music\music8.MP3",
]

random_song1 = random.choice(music_list)  # 随机选择下一首音乐
pygame.mixer.music.load(random_song1) # 加载第一首歌曲
pygame.mixer.music.set_volume(Volume)  # 设置音量大小
pygame.mixer.music.play()

pygame.time.set_timer(pygame.USEREVENT, 2000)  # 每2秒触发一个自定义事件
