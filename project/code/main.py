import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import random
import webbrowser
import pyautogui
import time
from PIL import Image, ImageTk
from tkinter import Canvas, Tk
import pygame

import shapes
import explode_ani
import music

# 常量定义
BG_COLOR = "lightblue"
BTN_COLOR = "#AADDFF"

STAGE_2_HP = 200 # 进入2阶段的血量
STAGE_3_HP = 100 # 进入3阶段的血量

STOP_KEY = 'x' # 暂停键
SKILL_KEY = 'z' # 技能键

cell_size = 35 #
C = 14 # 12
R = 22 # 20
Bottom_h = 12 # 
height = R * cell_size + Bottom_h # 
width = C * cell_size
level_score = [300, 600, 900, 1200, 1500, 2000] # 进入下一关所需的得分
level_fps = [0, 800, 750, 700, 680, 660, 640, 620] # 每关对应的fps
color_bottom = "#222222" # 黑色
color_bottom2 = "#CCCCAA" # 淡黄
Window_X = 900
Window_Y = 100

# 全局对象定义
root,win,canvas,label = None,None,None,None
canvas_root = None
image_tk = None # 全局变量，避免被回收
# play_button2 = None # 全局变量,控制音乐

# 全局变量定义
# 每局都初始化的全局变量
level_now = 1 # 关卡数
level_old = 1
score = 0 # 得分
fps = 800 # 刷新页面的毫秒间隔
oldfps = 800
revive_num = 1 # 复活次数
current_block = None
next_block_kind = ""
block_list = []
vis = []
visold = []
is_up_key_pressed = False
is_paused = False
skill_point = 1 # 技能点
skill_using = False
fall_ci = 0
boss_hp = 300
boss_hp_old = boss_hp
image_id = 0
left_turn = 30 # 剩余回合数
is_game_over = False

# 从第二局开始，不用初始化的全局变量
change_eng_input = False # 未切换英文输入法



# 加载图片
road = r"boss_pic\boss_stage1.png"
road2 = r"boss_pic\boss_stage2.png"
road3 = r"boss_pic\boss_stage3.png"
road_die = r"boss_pic\boss_die.png"

image = Image.open(road)
image2 = Image.open(road2)
image3 = Image.open(road3)
image_die = Image.open(road_die)



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

def draw_cell_by_cr(c, r, color="#CCCCCC", tag_kind=""):
    # return #
    """
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :return:
    """
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
def draw_bottom():
    for i in range(0,C):
        if vis[i]!=visold[i]: # 有变化
            visold[i]=vis[i]
            draw_bottom_block(i, vis[i])


# 绘制面板, 只有在第一次绘制时才绘制背景色方块
def draw_board(isFirst=False):
    # 删掉原来所有的行
    for ri in range(R):
        canvas.delete("row-%s" % ri)

    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type=='Boss': 
                continue # Boss方块不用绘制
            if cell_type:
                draw_cell_by_cr(ci, ri, SHAPESCOLOR[cell_type], tag_kind="row")
            elif isFirst:
                draw_cell_by_cr(ci, ri)
    
    draw_bottom()


def draw_cells(c, r, cell_list, color="#CCCCCC"):
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
        if 0 <= c < C and 0 <= r < R:
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
    # 移动前，清除原有位置绘制的俄罗斯方块
    try:
        canvas.delete("falling") #
    except:
        print("ERROR, canvas is not exist") #
        return 

    dc, dr = direction
    new_c, new_r = c+dc, r+dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(new_c, new_r, cell_list, SHAPESCOLOR[shape_type])
    
    if dc!=0: # 左右移动
        draw_bottom() # 更新底部指示条


def draw_vertical_line(ci): # 
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
    text = "得分{:<4}   关卡{}     下一个{:<7}\n复活次数{}".format(score, level_now, next_block_kind, revive_num)
    # {:<4}左对齐

    if lack_skill: # 在没有技能点时，尝试使用技能
        text = text + "  技能点不足" # 把 技能点数0 改成 技能点不足, 这样在打boss的时候不容易多字
    else:
        text = text + "  技能点数{}".format(skill_point)
    
    if level_now == 7: # boss关
        text = text + "  Boss血量{}".format(boss_hp)        
        if boss_hp <= STAGE_3_HP: # boss的最终阶段
            text = text + "\n剩余回合数{} ".format(left_turn) 
        else:
            text = text + "\n" # 
    else:
        text = text + "\n" # 

    if paused or is_paused: # 正在暂停
        text = text + "暂停中，按"+ STOP_KEY +"继续"
    
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
    #
    # print("check_level")

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
    # check_boss_hp()


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
    # check_boss_hp()


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
        # check_boss_hp() # 



def save_block_to_list(block):
    # 清除原有的打上了 falling 标签的方块
    canvas.delete("falling")

    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr
        # block_list 在对应位置记下其类型(用于在清除时更新画板)
        block_list[r][c] = shape_type
        draw_cell_by_cr(c, r, SHAPESCOLOR[shape_type], tag_kind="row")

    #
    # print("block_list :", block_list) # 


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
        #
        draw_bottom() # 更新底部

def on_up_key_release(event):
    global is_up_key_pressed
    is_up_key_pressed = False # 记录放开上键

def land(event):
    if is_paused or is_game_over: # 暂停中
        return

    global current_block
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
    if check_move(current_block, down):
        draw_block_move(current_block, down)


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
    # print("change_boss_stage, stage_id =", stage_id) # 

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
    if win: # 胜利
        # (获胜后，可以播放获胜动画，并且延迟弹出胜利窗口)
        messagebox.showinfo("游戏胜利！", "最终得分：%s分" % score)
    else: # 失败
        messagebox.showinfo("游戏结束！", "最终得分：%s分" % score)
    init()


def game_loop():
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
    if current_block is None:
        new_block = generate_new_block()
        
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
            draw_vertical_line(fall_ci) # 
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
                revive() # 复活
                
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

def switch_input(): # 模拟按下Shift键+Alt键来切换输入法
    pyautogui.keyDown('shift')
    pyautogui.press('alt')
    pyautogui.keyUp('shift')

def closing_root():
    root.quit()  # 退出事件循环
    root.destroy()  # 关闭窗口
    if change_eng_input:
        switch_input()

def closing_win():
    win.quit()  # 退出事件循环
    win.destroy()  # 关闭窗口
    if change_eng_input:
        switch_input()

def pause():
    global is_paused
    is_paused = not is_paused # 更新暂停状态
    draw_label(is_paused) # 更新标题
        

def use_skill(): # 
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


def create_canvas(): # 
    canvas = tk.Canvas(win, width=width, height=height) # 

    canvas.pack()
    draw_label() # 更新label，标题中展示分数和关卡
    canvas.focus_set() # 聚焦到canvas画板对象上
    canvas.bind("<KeyPress-Left>", horizontal_move_block)
    canvas.bind("<KeyPress-Right>", horizontal_move_block)
    canvas.bind("<KeyPress-Up>", rotate_block)
    canvas.bind("<KeyRelease-Up>", on_up_key_release) # 
    canvas.bind("<KeyPress-Down>", land)
    canvas.bind("<KeyPress>", press_key) # 

    return canvas


def create_win(): # 
    global win #
    if win: # 已有窗口
        try:
            win.quit() #
        except:
            print("ERROR when win.quit()")

    win = tk.Tk() # 游戏界面
    win.geometry(f"{width+100}x{height+90}") # 设置大小
    win.configure(bg=BG_COLOR) # 

    # 创建一个框架
    win_frame = tk.Frame(win, bg=BG_COLOR)



    # win = Toplevel(root) # 
    win.focus_set() # 设置焦点

    x = Window_X
    y = Window_Y
    win.geometry(f'+{x}+{y}') # 设置窗口位置

    win.title("俄罗斯方块")
    win.protocol("WM_DELETE_WINDOW", closing_win) # 

    global label, canvas
    
    label = Label(win_frame, text="", bg=BG_COLOR, justify="left", anchor="w") # 

    label_font = font.Font(size=15) # 
    label.configure(font=label_font)
    # label.pack(side='top', anchor='w') # 上面，向左对齐
    label.pack(side="left")

    # 创建一个播放音乐的按钮
    play_button2 = tk.Button(win_frame, text="播放\n音乐", bg=BTN_COLOR, command=music.play_random_music)
    # play_button2.pack(side=tk.RIGHT, padx=(0, 18)) # 设置右侧间隔

    # play_button2.pack(anchor="ne", padx=(0, 18), pady = 10) # 
    # play_button2.pack(side="left")
    play_button2.pack(side="right")

    # 将框架放置在界面上
    win_frame.pack()


    canvas = create_canvas() # 新建canvas

    draw_board(True) # 第一次绘制
    check_level() # 更新关卡

    win.update()
    win.after(fps, game_loop) # 在fps 毫秒后调用 game_loop方法
    
    return win


def main():
    global win
    root.quit()  # 退出事件循环
    root.destroy()

    win = create_win()

    test_use2() # 测试用
    
    global change_eng_input
    if change_eng_input==False:
        change_eng_input = True # 已切换英文
        switch_input()

    win.mainloop() # 


def open_link():
    webbrowser.open('https://github.com/Frank-Star-fn/Tetris_v2')

def create_root():
    global root 
    root = tk.Tk()
    root.title("俄罗斯方块")
    root.protocol("WM_DELETE_WINDOW", closing_root)
    root.configure(bg=BG_COLOR) # 

    # 获取屏幕的高度
    screen_width = root.winfo_screenheight()
    screen_height = root.winfo_screenheight()

    # 设置界面大小
    global width
    root_width = width
    root_height = screen_height//2 -75 # 
    root.geometry(f"{root_width}x{root_height}")

    x = Window_X
    y = Window_Y+50
    root.geometry(f'+{x}+{y}') # 设置窗口位置

    text_rule = ('\n游戏规则：填满一行即消除，堆满方块则失败。\n\n' + 
                 '操作：左右键移动，上键旋转，下键快速下落，\n' + 
                 STOP_KEY+'键暂停，'+SKILL_KEY+'键释放技能。\n')

    label_rule = tk.Label(root, text=text_rule, font=('黑体', 13), bg=BG_COLOR)
    label_rule.pack(side=tk.TOP, pady=0) # 

    # 计算按钮的位置
    button_width = 150
    button_height = 80
    button_x = (root_width // 2) - (button_width // 2) 
    button_y = (root_height // 2) - (button_height // 2)  # 

    button = tk.Button(root, text="开始游戏", font=('黑体', 20), bg=BTN_COLOR, command=main) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
    button.pack(side=tk.TOP, pady=10) #

    # 创建一个播放音乐的按钮
    play_button = tk.Button(root, text="播放/停止音乐", bg=BTN_COLOR, command=music.play_random_music)
    play_button.pack(side=tk.TOP, pady=10)

    label_web = tk.Label(root, text='俄罗斯方块-项目链接', fg='blue', cursor='hand2', bg=BG_COLOR)
    label_web.pack(side='bottom', anchor='s') # 放在底部
    label_web.bind('<Button-1>', lambda e: open_link())


    # draw image
    global image_tk
    canvas_root = Canvas(root, width=500, height=550, highlightthickness=0, bg=BG_COLOR)
    canvas_root.pack()

    # 缩小图片
    new_width = 8 * cell_size
    new_height = 4 * cell_size
    resized_image = image.resize((new_width, new_height))
    image_tk = ImageTk.PhotoImage(resized_image)  # 转换为Tkinter对象
    
    # 位置
    x = 3 * cell_size
    y = 10 # 
    canvas_root.create_image(x, y, image=image_tk, anchor='nw') # 绘制图像

    return root 


def init(first = False): # 初始化
    global level_now, level_old, fps, oldfps, score, current_block, next_block_kind, revive_num
    global block_list, win, root, vis, visold, is_up_key_pressed
    global is_paused, skill_point, skill_using, fall_ci, boss_hp, boss_hp_old, image_id, left_turn, is_game_over

    level_now = 1 # 关卡数
    level_old = 1
    fps = 800 # 刷新页面的毫秒间隔
    oldfps = 800
    score = 0 # 得分
    current_block = None
    next_block_kind = ""
    revive_num = 1 # 复活次数
    block_list = []
    for i in range(R):
        i_row = ['' for j in range(C)]
        block_list.append(i_row)
    vis = [0 for i in range(C)]
    visold = [1 for i in range(C)]
    is_up_key_pressed = False
    is_paused = False
    skill_point = 1 # 技能点数
    skill_using = False
    fall_ci = 0
    boss_hp = 300
    boss_hp_old = boss_hp
    image_id = 0
    left_turn = 30
    is_game_over = False

    test_use() # 测试用

    if first==False: # 不是第一次初始化
        try:
            win.quit()  # 退出事件循环
            win.destroy()  # 关闭窗口
        except:
            print("Error in operating interface") 

    root = create_root() # 主循环
    root.mainloop() # 启动主循环


def test_use2(): # 测试用
    global fps, SHAPES1
    # fps = 100 # 改下落速度
    # SHAPES1 = { # 改方块类型
    #     "I1p6": [(0,3),(0,2),(0,1),(0,0),(0,-1),(0,-2)], # 1*6
    # }

def test_use(): # 测试用, 直接改数据
    global score, revive_num, skill_point, boss_hp, left_turn
    # score = 2000 # 改初始score 
    # revive_num = 0 # 改复活次数
    # skill_point = 3 # 改初始技能点
    # boss_hp = 100 # 改boss血量
    # left_turn = 2 # 改剩余回合数


if __name__ == "__main__":
    init(True) # 初始化
    