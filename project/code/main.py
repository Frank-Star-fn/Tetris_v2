import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import Canvas, Tk
import random
import webbrowser
import pyautogui
from PIL import Image, ImageTk
import pygame
import ctypes
import pickle
import os

import shapes
import explode_ani
import music
import datatype
import get_time

# 常量定义
C = datatype.C 
R = datatype.R

WIN_X = 750 # 
WIN_Y = 100
BG_COLOR = "lightblue"
BTN_COLOR = "#AADDFF"
STAGE_2_HP = 200 # 进入2阶段的血量
STAGE_3_HP = 100 # 进入3阶段的血量
STOP_KEY = 'x' # 暂停键
SKILL_KEY = 'z' # 技能键
cell_size = 35 #
Bottom_h = 12 # 
height = R * cell_size + Bottom_h # 
width = C * cell_size
level_score = [300, 600, 900, 1200, 1500, 2000] # 进入下一关所需的得分
level_fps = [0, 800, 750, 700, 680, 660, 640, 620] # 每关对应的fps
color_bottom = "#222222" # 黑色
color_bottom2 = "#CCCCAA" # 淡黄

# 全局对象定义
root,win,canvas,label = None,None,None,None
canvas_root,canvas_block = None,None
image_tk,image_tk2 = None,None
label_rule,label_store_2,label_store_note,store_window = None,None,None,None
# label_check = None

# 全局变量定义
# 每局都初始化的全局变量
vis,visold = [],[]
is_game_over,back_to_root = False,False # 

# 从第二局开始，不用初始化的全局变量
change_eng_input = False # 未切换英文输入法
# is_first_game = True
root_img_id = 0

# 加载图片
road = r"pic\boss_pic\boss_stage1.png"
road2 = r"pic\boss_pic\boss_stage2.png"
road3 = r"pic\boss_pic\boss_stage3.png"
road_die = r"pic\boss_pic\boss_die.png"

image = Image.open(road)
image2 = Image.open(road2)
image3 = Image.open(road3)
image_die = Image.open(road_die)
image_block = None

road4 = "pic\\block_pic\\" # 

def read_block_img(block_kind):
    global image_tk2, image_block_id, canvas_block

    road_block = road4 + block_kind + ".png"

    global image_block
    if block_kind=="":
        return
    
    image_block = Image.open(road_block)

    # 缩小图片
    new_width = 4 * cell_size
    new_height = 4 * cell_size
    resized_image = image_block.resize((new_width, new_height))
    image_tk2 = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象

    # 在指定位置绘制图片
    if image_block_id!=0:
        try:
            canvas_block.delete(image_block_id) # 清除之前的图片
        except:
            print("ERROR when delete old image")
    
    image_block_id = canvas_block.create_image(0,0, image=image_tk2,anchor='nw')


# 加入闯关机制
# 定义各种形状
SHAPES1 = shapes.SHAPES1
SHAPES2 = shapes.SHAPES2
SHAPES3 = shapes.SHAPES3
SHAPES4 = shapes.SHAPES4
SHAPES5 = shapes.SHAPES5
SHAPES6 = shapes.SHAPES6
SHAPES7 = shapes.SHAPES7
Rotate = shapes.Rotate
SHAPESCOLOR = shapes.SHAPESCOLOR

ARCH_ROAD = "./saves"

# 存档
def save_archive():
    dataout = datatype.DataOut() # 自定义数据类
    data = datatype.Data()
    global win_times, gold, init_revive_num, init_skill_points, highest_score, new_check_date
    global level_now, level_old, fps, oldfps, score, current_block, next_block_kind, revive_num
    global block_list, win, root, vis, visold, is_up_key_pressed
    global is_paused, skill_point, skill_using, fall_ci, boss_hp, boss_hp_old, image_id, image_block_id
    global left_turn, is_game_over, back_to_root
    
    dataout.win_times = win_times
    dataout.gold = gold
    dataout.init_revive_num = init_revive_num
    dataout.init_skill_points = init_skill_points
    dataout.highest_score = highest_score
    dataout.new_check_date = new_check_date

    data.level_now = level_now # 关卡数
    data.level_old = level_old
    data.fps = fps
    data.oldfps = oldfps
    data.score = score
    data.current_block = current_block
    data.next_block_kind = next_block_kind
    data.revive_num = revive_num
    data.block_list = block_list
    data.is_up_key_pressed = is_up_key_pressed
    data.is_paused = is_paused
    data.skill_point = skill_point
    data.skill_using = skill_using
    data.fall_ci = fall_ci
    data.boss_hp = boss_hp
    data.boss_hp_old = boss_hp_old
    data.image_id = image_id
    data.image_block_id = image_block_id
    data.left_turn = left_turn

    if not os.path.exists(ARCH_ROAD): # 路径不存在
        os.makedirs(ARCH_ROAD)
        #
        print("创建路径"+ARCH_ROAD) # 

    # 存档
    with open(ARCH_ROAD+"//save1", 'wb') as f:
        pickle.dump(data, f) 
    with open(ARCH_ROAD+"//saveout", 'wb') as f:
        pickle.dump(dataout, f) 


# 读档
def load_archive(is_out = False):
    if is_out: # 读取局外存档
        global win_times, gold, init_revive_num, init_skill_points, highest_score, new_check_date
        saveout_road = ARCH_ROAD+"//saveout"
        if os.path.exists(saveout_road): # 文件存在
            try:
                with open(ARCH_ROAD+"//saveout", 'rb') as f:
                    dataout = pickle.load(f)
                    win_times = dataout.win_times
                    gold = dataout.gold
                    init_revive_num = dataout.init_revive_num
                    init_skill_points = dataout.init_skill_points
                    highest_score = dataout.highest_score
                    new_check_date = dataout.new_check_date

            except:
                print("读取局外存档失败")
                win_times = 0
                gold = 0
        # else:
            # print("未找到局外存档") #

    else: # 读取局内存档
        save1road = ARCH_ROAD+"//save1"
        if os.path.exists(save1road): # 文件存在
            try:
                with open(save1road, 'rb') as f:
                    data = pickle.load(f)
                    global level_now, level_old, fps, oldfps, score, current_block, next_block_kind, revive_num
                    global block_list, win, root, vis, visold, is_up_key_pressed
                    global is_paused, skill_point, skill_using, fall_ci, boss_hp, boss_hp_old, image_id, image_block_id
                    global left_turn, is_game_over, back_to_root

                    level_now = data.level_now # 关卡数
                    level_old = data.level_old
                    fps = data.fps
                    oldfps = data.oldfps
                    score = data.score
                    current_block = data.current_block
                    next_block_kind = data.next_block_kind
                    revive_num = data.revive_num
                    block_list = data.block_list
                    is_up_key_pressed = data.is_up_key_pressed
                    is_paused = data.is_paused
                    skill_point = data.skill_point
                    skill_using = data.skill_using
                    fall_ci = data.fall_ci
                    boss_hp = data.boss_hp
                    boss_hp_old = data.boss_hp_old
                    image_id = data.image_id
                    image_block_id = data.image_block_id
                    left_turn = data.left_turn
            except:
                print("读取局内存档失败")
        # else:
        #     print("未找到局内存档") #

# 新游戏，初始化局内存档
def init_archive():
    save1road = ARCH_ROAD+"//save1"
    if os.path.exists(save1road): # 文件存在
        with open(save1road, 'wb') as f:
            data = datatype.Data()
            pickle.dump(data, f) 


def draw_cell_by_cr(c, r, color="#CCCCCC", tag_kind=""):
    #
    # print("draw_cell_by_cr")
    # print("c,r =", c,r)
    # print("color =", color)
    # print("tag_kind =", tag_kind)

    """
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :return:
    """
    if c<0 or c>=C or r<0 or r>=R:
        print("ERROR, 越界")
        print("c,r =", c,r)
        return
    
    global canvas
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = x0 + cell_size
    y1 = y0 + cell_size
    if tag_kind == "falling":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color,outline="white", width=2, tag=tag_kind)
    elif tag_kind == "row":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2, tag="row-%s" % r)
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2) # 背景方块


# 画一块
def draw_bottom_block(x, visx):
    global canvas
    y0 = height - Bottom_h
    y1 = height
    canvas.delete("b%s" % x) # 删除原有的指示条，避免变卡
    if visx==0:
        canvas.create_rectangle(x*cell_size, y0, (x+1)*cell_size, y1, fill=color_bottom, outline="white", width=2, tag="b%s" % x)
    else:
        canvas.create_rectangle(x*cell_size, y0, (x+1)*cell_size, y1, fill=color_bottom2, outline="white", width=2, tag="b%s" % x)


# 画一整行
def draw_bottom(draw_all = False):
    if draw_all:
        for i in range(0,C):
            visold[i]=vis[i]
            draw_bottom_block(i, vis[i])
    else:
        for i in range(0,C):
            if vis[i]!=visold[i]: # 有变化
                visold[i]=vis[i]
                draw_bottom_block(i, vis[i])


# 绘制面板, 只有在第一次绘制时才绘制背景色方块
def draw_board(isFirst=False):
    #
    # print("draw_board")
    # print("isFirst =", isFirst)

    # 删掉原来所有的行
    for ri in range(R):
        canvas.delete("row-%s" % ri)

    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type=='Boss': 
                continue # Boss方块不用绘制

            if isFirst: # 第一次绘制,绘制背景
                draw_cell_by_cr(ci, ri)
            if cell_type: # 绘制上方的方块
                #
                # print("draw_board -> draw_cell_by_cr")
                # print("block_list[ri] =", block_list[ri]) # 
                draw_cell_by_cr(ci, ri, SHAPESCOLOR[cell_type], tag_kind="row") # 

    if isFirst:
        global current_block
        if current_block: # 不为空
            draw_block_move(current_block, [0,0]) # 

    draw_bottom(draw_all = isFirst) # 第一次画全部


def draw_cells(c, r, cell_list, color="#CCCCCC"):
    #
    # print("draw_cells")
    # print("c,r =", c,r)
    # print("cell_list =", cell_list)
    # print("color =", color)

    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param r: 该形状设定的原点所在的行
    :param c: 该形状设定的原点所在的列
    :param cell_list: 该形状各个方格相对自身所处位置
    :param color: 该形状颜色
    :return:
    """
    global canvas, vis
    vis = [0 for i in range(C)] # 初始化vis
    for cell in cell_list:
        cell_c, cell_r = cell

        ci = cell_c + c
        ri = cell_r + r
        # 判断该位置方格在画板内部(画板外部的方格不再绘制)
        # if 0 <= c < C and 0 <= r < R: # 
        if 0 <= ci < C and 0 <= ri < R: # 
            draw_cell_by_cr(ci, ri, color, tag_kind="falling")
            vis[ci]=1 # 更新vis
    
    
def draw_block_move(block, direction=[0, 0]):
    """
    绘制向指定方向移动后的俄罗斯方块
    :param canvas: 画板
    :param block: 俄罗斯方块对象
    :param direction: 俄罗斯方块移动方向
    :return:
    """
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    global canvas
    try:
        canvas.delete("falling") # 移动前，清除原有位置绘制的俄罗斯方块
    except:
        print("ERROR, canvas is not exist") #
        return 

    dc, dr = direction
    new_c, new_r = c+dc, r+dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(new_c, new_r, cell_list, SHAPESCOLOR[shape_type])
    
    draw_bottom() # 更新底部指示条(左右移动,以及第一次往下移动时,都需要更新)


def draw_vertical_line(ci): # 绘制竖线
    color = SHAPESCOLOR['Boom'] # 

    if ci==0:
        for i in range(0,R):
            if block_list[i][ci]!='Boss':
                draw_cell_by_cr(ci,i,color) # 变红
    elif ci<C:
        for i in range(0,R):
            if block_list[i][ci]!='Boss':
                draw_cell_by_cr(ci,i,color) # 变红
            if block_list[i][ci-1]!='Boss':
                draw_cell_by_cr(ci-1,i) # 变灰
    else: # ci==C
        for i in range(0,R):
            if block_list[i][ci-1]!='Boss':
                draw_cell_by_cr(ci-1,i) # 变灰


def draw_black():
    global canvas
    canvas.create_rectangle(0, 0, width, height, fill="#000000") # 


def generate_new_block():
    shapes = [None, SHAPES1, SHAPES2, SHAPES3, SHAPES4, SHAPES5, SHAPES6, SHAPES7]
    shape_now = SHAPES1

    global level_now, next_block_kind, boss_hp, left_turn, canvas
    try:
        shape_now = shapes[level_now]
    except:
        print("ERROR level") # 

    # 生成新的方块
    if next_block_kind!="": # 不是第一次，已知下一个方块的类别
        kind = next_block_kind
    else: # 第一次生成
        kind = random.choice(list(shape_now.keys()))

    # 随机生成下一个方块的类别
    next_block_kind = random.choice(list(shape_now.keys()))
        
    draw_label() # 更新标签

    if kind == "Skill": # 技能
        global skill_using
        skill_using = True # 正在释放技能
        kind = next_block_kind # 

    # 对应横纵坐标，以左上角为原点，水平向右为x轴正方向，
    # 竖直向下为y轴正方向，x对应横坐标，y对应纵坐标
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': shape_now[kind], # 方块列表
        'cr': cr # 中心点的行列
    }

    if level_now==7 and boss_hp<=STAGE_3_HP: # 在boss第三阶段
        left_turn -= 1 # 剩余回合数-1
        draw_label() # 更新标签

        if left_turn<=0:
            # 游戏结束
            global is_game_over
            is_game_over = True
    
    return new_block
    

def check_move(block, direction=[0, 0]):
    #
    # print("check_move")
    # print("block =", block)
    # print("direction =", direction)

    """
        判断俄罗斯方块是否可以朝制定方向移动
        :param block: 俄罗斯方块对象
        :param direction: 俄罗斯方块移动方向
        :return: boolean 是否可以朝制定方向移动
    """
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]
        # 判断该位置是否超出左右边界，以及下边界
        # 一般不判断上边界，因为俄罗斯方块生成的时候，可能有一部分在上边界之上还没有出来
        if c < 0 or c >= C or r >= R:
            return False

        # 必须要判断r不小于0才行，否则数组越界
        if r >= 0 and block_list[r][c]:
            return False

    return True


def check_row_complete(row):
    for cell in row:
        if cell=='':
            return False

    return True


def draw_label(paused = False, lack_skill = False):
    global score, level_now, revive_num, next_block_kind, skill_point, boss_hp, is_paused, left_turn

    read_block_img(next_block_kind) # 
    
    text = "得分{:<4}   \n关卡{}     \n复活次数{}".format(score, level_now, revive_num)
    # {:<4}左对齐

    if lack_skill: # 在没有技能点时，尝试使用技能
        text = text + "\n技能点不足" # 把 技能点数0 改成 技能点不足, 这样在打boss的时候不容易多字
    else:
        text = text + "\n技能点数{}".format(skill_point)
    
    if level_now == 7: # boss关
        text = text + "\nBoss血量{}".format(boss_hp)        
        if boss_hp <= STAGE_3_HP: # boss的最终阶段
            text = text + "\n剩余{}回合".format(left_turn) 
        else:
            text = text + "\n" # 
    else:
        text = text + "\n\n" # 

    if paused or is_paused: # 正在暂停
        text = text + "\n暂停中，\n按"+ STOP_KEY +"继续"
    else:
        text = text + "\n\n"
    
    label.config(text=text) # 


def show_boss():
    global canvas, image, cell_size, image_tk, boss_hp # 调用全局变量

    for i in range(R-3,R-5,-1):
        for j in range(4, 10):
            block_list[i][j] = 'Boss'
    for i in range(R-1,R-3,-1):
        for j in range(3, 11):
            block_list[i][j] = 'Boss'

    # 缩小图片
    new_width = 8 * cell_size
    new_height = 4 * cell_size

    if boss_hp > STAGE_2_HP: # stage 1
        resized_image = image.resize((new_width, new_height))
    elif boss_hp > STAGE_3_HP: # stage 2
        resized_image = image2.resize((new_width, new_height))
    else: # boss_hp<=STAGE_3_HP, stage 3
        resized_image = image3.resize((new_width, new_height))

    image_tk = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象

    # 位置
    x = 3 * cell_size
    y = (R-4) * cell_size + 5 # 
    # 在指定位置绘制图片
    global image_id
    if image_id!=0:
        try:
            canvas.delete(image_id) # 清除之前的图片
        except:
            print("ERROR when delete old image")
    image_id = canvas.create_image(x,y, image=image_tk,anchor='nw')


def check_level(): # 更新当前所在的关卡
    global score, fps, level_now, level_old
    len1=len(level_score)
    for i in range(len1-1,-1,-1): # 
        if score>=level_score[i]:
            level_now = i+2
            fps = level_fps[level_now]
            break

    if level_now>level_old: # 涨关了
        level_old = level_now
        if level_now%3==0: # 到达3的倍数关
            global skill_point
            skill_point += 1 # 多一个技能点
        if level_now==7: # 到达boss关
            show_boss() # 


# 更新得分
def update_score(cnt):
    global score
    score += cnt # 得分增加
    check_level()
    draw_board() # 重新绘制
    draw_label()

def boom_clear(block):
    global boss_hp
    c,r = block['cr']
    cnt=0
    for i in range(-1,2):
        for j in range(-1,2):
            dc=c+i
            dr=r+j
            if dr<0 or dr>=R: # R=行数
                continue 
            if dc<0 or dc>=C: # C=列数
                continue 
            
            if(block_list[dr][dc]!=''): # 
                if  block_list[dr][dc]=='Boss': # 击中boss方块
                    boss_hp -= 1 # 造成伤害
                else:
                    block_list[dr][dc]='' # 消除
                cnt+=1
    
    update_score(cnt)


def addBoom_clear(block):
    global boss_hp
    c,r = block['cr']
    cnt=0
    for i in range(-1,2):
        for j in range(0,R):
            dc=c+i
            if dc<0 or dc>=C: # C=列数
                continue 
            if(block_list[j][dc]!=''): # 
                if  block_list[j][dc]=='Boss': # 击中boss方块
                    boss_hp -= 1 # 造成伤害
                else:
                    block_list[j][dc]='' # 消除
                cnt+=1

    for i in range(-1,2):
        for j in range(0,C):
            dr=r+i
            if dr<0 or dr>=R: # R=行数
                continue 
            if(block_list[dr][j]!=''): # 
                if  block_list[dr][j]=='Boss': # 击中boss方块
                    boss_hp -= 1 # 造成伤害(特性：卡在角落时，可以对角落的boss方块造成两次伤害)
                else:
                    block_list[dr][j]='' # 消除
                cnt+=1

    update_score(cnt)


def check_and_clear():
    global score, boss_hp

    has_complete_row = False
    # 连续消除得分更高
    score1=10 # 可以增加的分
    for ri in range(0,len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0: # 不在最顶上
                for j in range(0, C):
                    if block_list[ri][j]=='Boss': # boss方块
                        boss_hp -= 1 # boss扣血
                    else: # 普通方块
                        for cur_ri in range(ri, 0, -1):
                            block_list[cur_ri][j]=block_list[cur_ri-1][j] # 上面的掉下来
                        block_list[0][j]=''
            else: # ri==0,最顶上
                block_list[ri] = ['' for j in range(C)]

            score += score1 # 得分增加
            score1 += 10 # 连续消除得分：10,20,30,40,...
            # 消除1行：10分, 消除2行：30分, 
            # 消除3行：60分, 消除4行：100分, 以此类推

    if has_complete_row:
        check_level() # 更新当前关卡
        draw_board() # 重新绘制
        draw_label()


def save_block_to_list(block):
    canvas.delete("falling") # 清除原有的打上了 falling 标签的方块

    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr
        # block_list 在对应位置记下其类型(用于在清除时更新画板)

        if r>=0 and r<R and c>=0 and c<=C: # 判断，避免数组越界
            block_list[r][c] = shape_type #
            draw_cell_by_cr(c, r, SHAPESCOLOR[shape_type], tag_kind="row")
        
        # else: # 部分方块超出了画面上限
            # print("WARNING, 部分方块超出了画面上限") # 
            
def horizontal_move_block(event):
    """
    左右水平移动俄罗斯方块
    """
    if is_paused or is_game_over: # 暂停中
        return
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(current_block, direction)


def rotate_block(event): # 旋转
    if is_paused or is_game_over: # 暂停中
        return
    
    global current_block, is_up_key_pressed
    if current_block is None:
        return
    if Rotate[current_block['kind']]==False: # 旋转后形状一样的方块，禁用旋转
        return
    if is_up_key_pressed: # 正在长按上键
        return
        
    is_up_key_pressed = True # 记录按下

    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, -cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        'kind': current_block['kind'],  # 对应俄罗斯方块的类型
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):
        cc, cr= current_block['cr']
        draw_cells(cc, cr, current_block['cell_list'])
        draw_cells(cc, cr, rotate_list,SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate
        draw_bottom() # 更新底部


def on_up_key_release(event):
    global is_up_key_pressed
    is_up_key_pressed = False # 记录放开上键

def land(event): # 下落
    if is_paused or is_game_over: # 暂停中或者游戏已经结束
        return

    global current_block, block_list
    if current_block is None:
        return
    
    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = R
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if r>=0 and block_list[r][c]:
            return
        h = 0
        for ri in range(r+1, R):
            if block_list[ri][c]:
                break
            else:
                h += 1
        if h < min_height:
            min_height = h

    down = [0, min_height]

    if min_height>=1: # 下落距离大于等于1格时才响应(0格不响应)
        block_now = current_block # 获取当前block
        if check_move(block_now, down):
            draw_block_move(block_now, down)


def revive(): # 复活
    R2 = R//2
    for i in range(0, R2):
        block_list[i] = ['' for j in range(0, C)]

    global revive_num
    revive_num-=1
    draw_board() # 重新绘制
    draw_label()
    if level_now==7: # 正在boss关
        show_boss() # 重新绘制boss，避免显示bug


def show_boss_die():
    global image_tk, image_id
    # 缩小图片
    new_width = 8 * cell_size
    new_height = 4 * cell_size
    resized_image = image_die.resize((new_width, new_height))
    
    image_tk = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象
    # 位置
    x = 3 * cell_size
    y = (R-4) * cell_size + 5 # 
    if image_id!=0:
        canvas.delete(image_id) # 清除之前的图片
    image_id = canvas.create_image(x,y, image=image_tk,anchor='nw') # 绘制图片


def change_boss_stage(stage_id): # 
    global image_tk, image_id
    # 缩小图片
    new_width = 8 * cell_size
    new_height = 4 * cell_size
    
    resized_image = None
    if stage_id == 2:
        resized_image = image2.resize((new_width, new_height))
    elif stage_id == 3:
        resized_image = image3.resize((new_width, new_height))
    else:
        print("ERROR stage_id, stage_id =", stage_id) # 

    image_tk = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象
    # 位置
    x = 3 * cell_size
    y = (R-4) * cell_size + 5 # 

    if image_id!=0:
        canvas.delete(image_id) # 清除之前的图片

    image_id = canvas.create_image(x,y, image=image_tk,anchor='nw') # 绘制图片


def check_boss_hp():
    global boss_hp, boss_hp_old
    if boss_hp<=0: # 击败boss
        show_boss_die() # 
        draw_label()
        return True # 击败boss, 返回True
    
    elif boss_hp<=STAGE_3_HP: # 在3阶段
        if boss_hp_old>STAGE_3_HP: # 刚刚进入
            boss_hp_old = boss_hp
            change_boss_stage(3) # 

    elif boss_hp<=STAGE_2_HP: # 在2阶段
        if boss_hp_old>STAGE_2_HP: # 刚刚进入
            boss_hp_old = boss_hp
            change_boss_stage(2) # 

    return False # 未击败boss

def game_over(win = False):
    global gold, score
    win_gold = score//10 # 每获得10分，+1金币
    
    if win: # 胜利
        # (获胜后，可以播放获胜动画，并且延迟弹出胜利窗口)
        score += 500 # 击败boss额外+500分数
        win_gold += 50 # 游戏获胜额外+50金币
        draw_label() # 更新label
        messagebox.showinfo("游戏胜利！", "最终得分%s分，获得%d个金币" % (score,win_gold))
        global win_times
        win_times += 1 # 通关次数+1
    else: # 失败
        messagebox.showinfo("游戏结束！", "最终得分%s分，获得%d个金币" % (score,win_gold))

    gold += win_gold # 获得金币
    global highest_score
    highest_score = max(highest_score, score) # 更新最高分

    init_archive() # 初始化局内存档
    init_value() # 初始化局内变量值
    save_archive() # 保存存档
    init()

def game_loop():
    global change_eng_input
    if change_eng_input==False:
        change_eng_input = True # 已切换英文
        switch_input()

    if back_to_root: # 返回主界面
        save_archive() # 存档
        init()
        return

    if music.music_on:
        for event in pygame.event.get(): # 处理事件队列
            if event.type == pygame.USEREVENT:
                music.play_next()

    global skill_using, fall_ci, fps, oldfps, canvas, vis, visold, boss_hp, win

    if skill_using: # 正在使用技能
        if fall_ci<=C: # 
            draw_vertical_line(fall_ci) # 
            fall_ci += 1
            win.after(fps, game_loop) # 
            return
        else: # 技能释放结束
            fps = oldfps
            skill_using = False # 标记技能释放结束

            canvas.destroy() # 删除原有canvas
            canvas = create_canvas() # 新建canvas

            draw_board(True) # 绘制
            check_level() # 更新关卡
            if level_now==7: # 正在boss关
                show_boss()
                boss_hp -= 12 # 造成12点伤害 
                if check_boss_hp(): # 如果击败boss
                    game_over(True) # 获胜
                    return # 退出

            vis = [0 for i in range(C)]
            visold = [1 for i in range(C)]
            draw_bottom() # 更新底部指示条
    
    if is_paused or is_game_over: # 暂停中
        win.after(fps, game_loop) # 
        return  
    
    try:
        win.update()
    except:
        print("ERROR when win.update()")

    global current_block
    if current_block is None: # 之前的block落地了
        new_block = generate_new_block() # 生成新的bolck
        
        if skill_using: # 正在使用技能
            # 清屏(除了boss)
            global block_list
            for i in range(0, R):
                for j in range(0,C):
                    if block_list[i][j]!='Boss':
                        block_list[i][j]=''

            # 播放动画
            oldfps = fps
            fps = 100 # 加速
            fall_ci = 0
            draw_vertical_line(fall_ci) # 绘制竖线
            fall_ci += 1
            win.after(fps, game_loop)
            return

        # 新生成的俄罗斯方块需要先在生成位置绘制出来
        draw_block_move(new_block)
        draw_bottom() # 更新底部指示条

        current_block = new_block

        if is_game_over: # 回合数到了，爆炸
            draw_black() # 变黑
            explode_ani.boss_explode_animation(canvas,width//2,height//2) # 播放爆炸动画
            win.after(explode_ani.Duration_Time, game_over) # 游戏结束
            return

        if not check_move(current_block, [0, 0]):
            global revive_num
            if revive_num<=0:
                game_over() # 游戏结束
                return
            else: # revive_num>=1
                revive() # 复活,清掉上半屏幕
                # current_block = None # 

    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(current_block, [0, 1])
        else:
            # 无法移动，记入 block_list 中
            save_block_to_list(current_block)
             
            if current_block['kind'] == "Boom": # 炸弹
                boom_clear(current_block)
            elif current_block['kind'] == "AddBoom": # 加号炸弹
                addBoom_clear(current_block)

            current_block = None
            check_and_clear()
            if check_boss_hp():
                game_over(True) # 获胜
                return
                
    win.after(fps, game_loop)

def switch_input(): # 切换输入法
    ctypes.windll.user32.LoadKeyboardLayoutW("00000409", 1)  # 英文（美国）输入法的键盘布局代码为 "00000409"

def switch_input_back(): # 切换回来
    pyautogui.keyDown('shift')
    pyautogui.press('alt')
    pyautogui.keyUp('shift')


def closing_root():
    root.quit()  # 退出事件循环
    root.destroy()  # 关闭窗口
    if change_eng_input:
        switch_input_back()

def closing_win():  
    save_archive() # 存档
    win.quit()  # 退出事件循环
    win.destroy()  # 关闭窗口
    root.quit()  # 退出事件循环
    root.destroy()  # 关闭窗口
    if change_eng_input:
        switch_input_back()



def pause():
    global is_paused
    is_paused = not is_paused # 更新暂停状态
    draw_label(is_paused) # 更新标题
        

def use_skill(): 
    global next_block_kind
    global skill_point

    if next_block_kind!="Skill": # 下一个不是用技能
        skill_point -= 1 # 消耗技能点
        next_block_kind = "Skill" # 下一个改为使用技能
        draw_label()


def print_lack_skill(): # 技能点不足
    draw_label(lack_skill=True)


def skill(): # 放技能
    global skill_point
    if skill_point>=1: # 技能点足够
        use_skill()
    else:
        print_lack_skill()
        

def press_key(event):
    if event.char.lower() == STOP_KEY:
        pause()
    else:
        global is_paused
        if (is_paused == False) and (is_game_over == False): # 不在暂停状态
            if event.char.lower() == SKILL_KEY:
                skill()

def space_key_pressed(event): # 按下
    global fps
    fps = 100 # 加速

def space_key_released(event): # 抬起
    global fps, level_fps, level_now
    fps = level_fps[level_now]


def create_canvas(): 
    canvas = tk.Canvas(win, width=width, height=height) 

    canvas.pack()
    draw_label() # 更新label，标题中展示分数和关卡
    canvas.focus_set() # 聚焦到canvas画板对象上
    canvas.bind("<KeyPress-Left>", horizontal_move_block)
    canvas.bind("<KeyPress-Right>", horizontal_move_block)
    canvas.bind("<KeyPress-Up>", rotate_block)
    canvas.bind("<KeyRelease-Up>", on_up_key_release) # 
    canvas.bind("<KeyPress-Down>", land)
    canvas.bind("<KeyPress>", press_key) # 
    canvas.bind("<KeyPress-space>", space_key_pressed)
    canvas.bind("<KeyRelease-space>", space_key_released)
    return canvas

def back_root():
    confirm = messagebox.askyesno("确认", "确认返回主界面吗？")
    if confirm:
        global back_to_root
        back_to_root = True # 下一次game_loop时，返回主界面


def create_win(new_game = False): # 
    if new_game==False: # 不是新游戏
        load_archive() # 读取局内变量

    else: # 是新游戏
        load_archive(is_out=True) # 读取局外变量
        init_archive() # 初始化局内存档
        load_archive() # 读取局内变量
        init_value() # 初始化值

    global win 
    if win: # 已有窗口
        try:
            win.quit() #
        except:
            print("ERROR when win.quit()")

    win = tk.Toplevel(root) # 游戏界面

    win.geometry(f"{width+200}x{height+10}") # 设置大小
    win.configure(bg=BG_COLOR) # 

    x = WIN_X
    y = WIN_Y
    win.geometry(f'+{x}+{y}') # 设置窗口位置

    win.title("俄罗斯方块闯关版")
    win.protocol("WM_DELETE_WINDOW", closing_win) # 

    win_frame = tk.Frame(win, bg=BG_COLOR) # 创建一个框架

    global canvas_block
    canvas_block = tk.Canvas(win_frame, width=4*cell_size , height=4*cell_size) 
    canvas_block.pack(side="top", pady=20) # 

    global label, canvas
    
    label = Label(win_frame, text="", bg=BG_COLOR, justify="left", anchor="w") # 
    label_font = font.Font(size=15) # 
    label.configure(font=label_font)
    label.pack()

    # 创建一个播放音乐的按钮
    play_button2 = tk.Button(win_frame, text="音乐", font=('黑体', 15), width=8, height=1, bg=BTN_COLOR, command=music.play_random_music)
    play_button2.pack(pady=5)

    # 返回按钮
    back_button =  tk.Button(win_frame, text="返回", font=('黑体', 15), width=8, height=1, bg=BTN_COLOR, command=back_root)
    back_button.pack(pady=5)

    # 将框架放置在界面上
    win_frame.pack(side="right", padx=(0,15)) # 

    canvas = create_canvas() # 新建canvas

    draw_board(True) # 第一次绘制
    check_level() # 更新关卡

    win.update()
    win.after(fps, game_loop) # 在fps 毫秒后调用 game_loop方法
    
    return win


def main(new_game = False):
    if new_game:
        result = messagebox.askokcancel("确认", "开始新游戏会覆盖现有存档，你确定要继续吗？") # 提示
        if result == False: # 取消 
            return

    global win, level_now
    win = create_win(new_game) # 创建游戏界面
    if level_now==7: # 到达boss关
        show_boss() 
    root.withdraw() # 隐藏开始界面
    test_use() # 测试用
    win.mainloop() # 


def open_link():
    webbrowser.open('https://github.com/Frank-Star-fn/Tetris_v2')

def draw_root_image():
    global image_tk, canvas_root
    # 缩小图片
    new_width = 8 * cell_size
    new_height = 4 * cell_size
    resized_image = image.resize((new_width, new_height))
    image_tk = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象
    # 位置
    x = 3 * cell_size
    y = 10 # 
    global root_img_id
    if root_img_id:
        canvas_root.delete(root_img_id) # 清除之前的图片

    root_img_id = canvas_root.create_image(x, y, image=image_tk, anchor='nw') # 重新绘制图像


def update_label_rule():
    text_rule = ('\n游戏规则：填满一行即消除，堆满方块则失败。\n\n' + 
                 '操作：左右键移动，上键旋转，\n空格键加速下落，下键直接落地，\n' + 
                 STOP_KEY+'键暂停，'+SKILL_KEY+'键释放技能。\n')
    load_archive(is_out=True)
    global win_times, gold
    text_rule += "\n通关次数{} 最高分{} 金币{}".format(win_times, highest_score, gold) 
    global label_rule
    label_rule.config(text=text_rule)

def get_price():
    global init_revive_num
    revive_price = 20
    if init_revive_num>=1:
        revive_price = 400 # 涨价到500
    skill_price = 150
    return revive_price,skill_price

def update_label_store_2():
    global label_store_2, gold, init_revive_num
    text_gold = "您的金币{}\n初始复活次数{} 初始技能点数{}".format(gold,init_revive_num,init_skill_points)

    revive_price,skill_price = get_price()
    text_gold += "\n复活次数价格{} 技能点数价格{}".format(revive_price,skill_price)
    label_store_2.config(text=text_gold)

def update_store_note(str=""):
    global label_store_note
    label_store_note.config(text=str)

def buy(item):
    global gold, init_revive_num, init_skill_points

    revive_price,skill_price = get_price()

    if item == "revive":
        if init_revive_num<2:
            if gold>=revive_price:
                gold-=revive_price
                init_revive_num+=1
                save_archive() # 存档
                update_label_store_2()
                update_label_rule()
                update_store_note("购买成功！")
            else:
                update_store_note("金币不足") # 显示在label里面

        else:
            update_store_note("初始复活次数达到上限") # 显示在label里面

    elif item == "skill":
        if init_skill_points<1:
            if gold>=skill_price:
                gold-=skill_price
                init_skill_points+=1
                save_archive() # 存档
                update_label_store_2()
                update_label_rule()
                update_store_note("购买成功！")
            else:
                update_store_note("金币不足")
        else:
            update_store_note("初始技能点数达到上限") # 显示在label里面
    

def closing_shop():
    global store_window
    store_window.destroy()  # 关闭窗口
    store_window = None

def open_shop(main_window):
    global store_window
    if store_window!=None: # 已有窗口
        return
    
    store_window = tk.Toplevel(main_window, bg=BG_COLOR)
    store_window.protocol("WM_DELETE_WINDOW", closing_shop) # 
    store_window.title("商店")
    store_window.geometry("650x300")
    
    # 在子页面中添加其他部件
    label = tk.Label(store_window, font=('黑体', 25), text=" 欢迎来到商店！", bg=BG_COLOR)
    label.pack()

    global label_store_2
    label_store_2 = tk.Label(store_window, font=('黑体', 20), text="", bg=BG_COLOR)
    update_label_store_2()
    label_store_2.pack()

    global label_store_note
    label_store_note = tk.Label(store_window, font=('黑体', 20), text="", bg=BG_COLOR)
    label_store_note.pack()

    store_frame = tk.Frame(store_window, bg=BG_COLOR) # 创建一个框架
    button = tk.Button(store_frame, text="购买初始复活次数", font=('黑体', 20), bg=BTN_COLOR, command=lambda: buy("revive")) # 创建按钮
    button.pack(side=tk.LEFT,padx=4) #
    button = tk.Button(store_frame, text="购买初始技能点数", font=('黑体', 20), bg=BTN_COLOR, command=lambda: buy("skill")) # 创建按钮
    button.pack(side=tk.RIGHT,padx=4) #
    store_frame.pack(pady=10)


def is_same_day(date1, date2):
    return date1.year == date2.year and date1.month == date2.month and date1.day == date2.day

def check_in(): # 每日签到
    global new_check_date, gold
    try:
        ntp_time = get_time.get_now_time() # 通过 NTP 获取时间
    except:
        messagebox.showinfo("签到失败", "签到失败，请重试")
        return
    
    if new_check_date!=None:
        if is_same_day(ntp_time, new_check_date): # 同一天
            messagebox.showinfo("签到失败", "签到失败，今天签到过了")
            return
            
    gold += 10 
    new_check_date = ntp_time
    save_archive() # 存档
    update_label_rule()
    messagebox.showinfo("签到成功", "签到成功，获得10金币！")


def create_root():
    global root 
    root = tk.Tk()
    root.title("俄罗斯方块闯关版")
    root.protocol("WM_DELETE_WINDOW", closing_root)
    root.configure(bg=BG_COLOR) # 

    screen_height = root.winfo_screenheight() # 获取屏幕的高度

    # 设置界面大小
    global width
    root_width = width
    root_height = screen_height//2 + 80 # 
    root.geometry(f"{root_width}x{root_height}")

    x = WIN_X
    y = WIN_Y+50
    root.geometry(f'+{x}+{y}') # 设置窗口位置

    global label_rule
    label_rule = tk.Label(root, text="", font=('黑体', 13), bg=BG_COLOR)
    update_label_rule()
    label_rule.pack(side=tk.TOP, pady=0) # 

    # 计算按钮的位置
    button_width = 150
    button_height = 80
    button_x = (root_width // 2) - (button_width // 2) 
    button_y = (root_height // 2) - (button_height // 2)  # 

    button = tk.Button(root, text="继续游戏", font=('黑体', 20), bg=BTN_COLOR, command=main) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
    button.pack(side=tk.TOP, pady=8) #

    btn_width_2 = 13
    btn_height_2 = 1

    button = tk.Button(root, text="新游戏", width=btn_width_2, height=btn_height_2, font=('黑体', 10), bg=BTN_COLOR, command=lambda: main(True)) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
    button.pack(side=tk.TOP, pady=8) #

    # 创建一个播放音乐的按钮
    play_button = tk.Button(root, text="播放/停止音乐", width=btn_width_2, height=btn_height_2, font=('黑体', 10), bg=BTN_COLOR, command=music.play_random_music)
    play_button.pack(side=tk.TOP, pady=8)

    button = tk.Button(root, text="商店", width=btn_width_2, height=btn_height_2, font=('黑体', 10), bg=BTN_COLOR, command=lambda: open_shop(root)) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
    button.pack(side=tk.TOP, pady=8) #

    global new_check_date
    button = tk.Button(root, text="每日签到", width=btn_width_2, height=btn_height_2, font=('黑体', 10), 
                       bg=BTN_COLOR, command=check_in) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
    button.pack(side=tk.TOP, pady=8) #

    label_web = tk.Label(root, text='项目链接', font=('黑体', 10), fg='blue', cursor='hand2', bg=BG_COLOR)
    label_web.pack(side='bottom', anchor='s') # 放在底部
    label_web.bind('<Button-1>', lambda e: open_link())

    global canvas_root
    canvas_root = Canvas(root, width=500, height=550, highlightthickness=0, bg=BG_COLOR)
    canvas_root.pack()

    # draw root image
    draw_root_image()

    return root 

def init_value(): # 初始化局内变量
    global init_revive_num, init_skill_points
    global level_now, level_old, fps, oldfps, score, current_block, next_block_kind, revive_num
    global block_list, vis, visold, is_up_key_pressed
    global is_paused, skill_point, skill_using, fall_ci, boss_hp, boss_hp_old, image_id, image_block_id
    global left_turn, is_game_over, back_to_root

    revive_num = init_revive_num # 复活次数
    skill_point = init_skill_points # 技能点数

    vis = [0 for i in range(C)]
    visold = [1 for i in range(C)]
    is_game_over = False
    back_to_root = False

    level_now = 1 # 关卡数
    level_old = 1
    fps = 800 # 刷新页面的毫秒间隔
    oldfps = 800
    score = 0 # 得分
    current_block = None
    next_block_kind = ""
    block_list = []
    for i in range(R):
        i_row = ['' for j in range(C)]
        block_list.append(i_row)
    is_up_key_pressed = False
    is_paused = False
    skill_using = False
    fall_ci = 0
    boss_hp = 300
    boss_hp_old = boss_hp
    image_id = 0
    image_block_id = 0
    left_turn = 30

def init(first = False): # 初始化
    if first: # 第一次初始化，声明局外变量
        global win_times, gold, init_revive_num, init_skill_points, highest_score, new_check_date
        win_times,gold,init_revive_num,init_skill_points,highest_score = 0,0,0,0,0 # 初始化
        new_check_date = None
        load_archive(is_out=True) # 读取局外变量 

    init_value() # 初始化局内变量值

    global root, win 
    if first: # 第一次初始化
        root = create_root() # 主循环
        root.mainloop() # 启动主循环

    else: # 不是第一次初始化
        try:
            win.quit()  # 退出事件循环
            win.destroy()  # 关闭窗口
        except:
            print("Error in operating interface") 
        
        root.deiconify() # 显示
        update_label_rule() # 更新label_rule
        draw_root_image() # 绘制root的背景图


def test_use(): # 测试用, 直接改数据
    global gold, score, revive_num, skill_point, boss_hp, left_turn, fps, SHAPES1
    # gold = 600 # 改金币数量
    # score = 2000 # 改初始score 
    # revive_num = 0 # 999 # 改复活次数
    # skill_point = 3 # 改初始技能点
    # boss_hp = 1 # 改boss血量
    # left_turn = 2 # 改剩余回合数
    # fps = 100 # 改下落速度
    # SHAPES1 = { # 改方块类型
    #     "I1p6": [(0,3),(0,2),(0,1),(0,0),(0,-1),(0,-2)], # 1*6
    # }


if __name__ == "__main__":
    init(True) # 初始化
    