import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import messagebox
import random
import copy
import webbrowser
import pyautogui
import time

# 常量定义
cell_size = 35 #
C = 14 # 12
R = 22 # 20
Bottom_h = 12 # 
height = R * cell_size + Bottom_h # 
width = C * cell_size
level_score = [300, 600, 900, 1200, 1500] # 进入下一关所需的得分
level_fps = [0, 800, 750, 700, 680, 660, 640] # 每关对应的fps
color_bottom = "#222222" # 黑色
color_bottom2 = "#CCCCAA" # 淡黄

# 全局对象定义
root,win,canvas,label = 0,0,0,0

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

# 从第二局开始，不用初始化的全局变量
change_eng_input = False # 未切换英文输入法


# 加入闯关机制
# 定义各种形状
# 第1关
SHAPES1 = {
    "Small":[(0, 0)], # 1*1
    "Small2":[(0, 0)], # 1*1
    "Boom":[(0, 0)], # 1*1,炸附近3*3,每个1分
    
    "I1p2": [(0, 1), (0, 0)], # 1*2
    "Dots2" : [(1, 0), (-1, 0)],
    "Dots2v2" : [(0, 0), (1, 1)],

    "I1p3": [(0, 1), (0, 0), (0, -1)], # 1*3
    "Corner": [(0, 1), (0, 0), (1, 0)], # Corner

    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],

    "AddBoom": [(-1,0), (0,-1), (0,0), (1,0), (0,1)], # +,消除三行三列
    
    "I1p6": [(0,3),(0,2),(0,1),(0,0),(0,-1),(0,-2)], # 1*6
    "I2p3": [(0,-1), (0,0),(1,0),(1,-1),(-1,0),(-1,-1)],# 2*3
}

# 第2关, 增加方块: "O3p3","F"
SHAPES2 = copy.deepcopy(SHAPES1)
SHAPES2["O3p3"]=[(0,0),(0,1),(0,-1),(-1,0),(-1,1),(-1,-1),(1,0),(1,1),(1,-1)] # 3*3
SHAPES2["F"]=[(0,2), (0,1), (0,0),(0,-1),(1,-1),(1,1)]

# 第3关, 增加方块: "O4p4","Add"
SHAPES3 = copy.deepcopy(SHAPES2)
SHAPES3["O4p4"]=[(0,0),(-1,-1),(0,-1),(-1,0),(-2,-2),(-2,-1),(-2,0),(-1,-2),(0,-2),
               (1,1),(1,0),(1,-1),(1,-2),(0,1),(-1,1),(-2,1)] # 4*4
SHAPES3["Add"]=[(-1,0), (0,-1), (0,0), (1,0), (0,1)] # +

# 第4关, 增加方块: "BigT", "H"
SHAPES4 = copy.deepcopy(SHAPES3)
SHAPES4["BigT"]=[(0,0),(0,1),(0,2),(1,0),(2,0),(-1,0),(-2,0)]
SHAPES4["H"]=[(0,0),(1,0),(-1,0),(1,-1),(1,1),(-1,-1),(-1,1)] 

# 第5关, 增加方块: "Dots4"
SHAPES5 = copy.deepcopy(SHAPES4)
SHAPES5["Dots4"]=[(1,1),(1,-1),(-1,-1),(-1,1)] # Hard # 注意不要有多余的逗号

# 第6关, 增加方块: "O5p5"
SHAPES6 = copy.deepcopy(SHAPES5)
SHAPES6["O5p5"]=[(0,-2),(0,-1),(0,0),(0,1),(0,2),
                      (1,-2),(1,-1),(1,0),(1,1),(1,2),
                      (2,-2),(2,-1),(2,0),(2,1),(2,2),
                      (-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),
                      (-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),] # 5*5, Hard

# SHAPES6["King"]=[(0,0),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)] # Very Hard
# SHAPES6["GiantO7p7"]=[(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),
#               (1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),
#               (2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),
#               (3,-3),(3,-2),(3,-1),(3,0),(3,1),(3,2),(3,3),
#               (-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),
#               (-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),
#               (-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),] # 7*7, Very Hard

# SHAPES = {
    # "Dots4v2":[(1,0),(-1,0),(0,-1),(0,1)], # Very Hard

    # "BigAdd":[(0,0),(0,1),(0,2),(0,-1),(0,-2),(1,0),(2,0),(-1,0),(-2,0)], # Super Hard
    
    # "King":[(0,0),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)], # Very Hard
    # "Num5":[(0,0), (1,1),(-1,-1),(1,0),(-1,0), (0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)], # Super Hard
    
    # "GiantO7p7":[(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),
    #           (1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),
    #           (2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),
    #           (3,-3),(3,-2),(3,-1),(3,0),(3,1),(3,2),(3,3),
    #           (-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),
    #           (-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),
    #           (-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),], # 7*7, Very Hard
# }

Rotate = { # 可以旋转：True, 不能旋转：False
    "Small": False, 
    "Small2": False, 
    "Boom": False, 
    
    "I1p2": True,
    "Dots2" : True,
    "Dots2v2" : True,

    "I1p3": True,
    "Corner": True,

    "O": False, 
    "S": True,
    "T": True,
    "I": True,
    "L": True,
    "J": True,
    "Z": True,
    "Dots4": False, 
    "Dots4v2": False, 

    "Add": False, 
    "AddBoom": False, 

    "I1p6": True,
    "I2p3": True,
    "F": True,
    
    "BigT": True,
    "H": True,

    "O3p3": False,
    "BigAdd": False,

    "King": True,
    "Num5": True,

    "O4p4" : False,

    "O5p5": False,

    "GiantO7p7": False,
}

# 定义各种形状的颜色
SHAPESCOLOR = {
    "Small": "#0011CC", # 蓝色
    "Small2": "#004499", # 深蓝绿
    "Boom":"#DD0000", # 红色
    
    "I1p2": "#AACC66", # 草绿色
    "Dots2" : "green", 
    "Dots2v2" : "#00AA11",

    "I1p3": "#8899FF", # 浅蓝色
    "Corner": "#EE8877", # 砖红色

    "O": "#d25b6a",
    "S": "#d2835b",
    "T": "#e5e234",
    "I": "#83d05d",
    "L": "#2862d2",
    "J": "#35b1c0",
    "Z": "#5835c0",
    "Dots4":"#333333", # 黑灰
    "Dots4v2":"#777777",

    "Add": "#666666", # 灰色
    "AddBoom": "#880088", # 紫色

    "I1p6": "#004411", # 深绿色
    "I2p3": "#992244", # 红色
    "F": "black", 
    
    "BigT":"#CC0088", # 紫色
    "H":"#AAAA22", # 土黄色

    "O3p3":"#004488", # 深蓝色
    "BigAdd":"#884400", # 棕色

    "King":"#FFFF66", # 金色
    "Num5":"#336633", # 深绿色

    "O4p4" : "#AA0000", # 红色

    "O5p5":"#701010", # 深红色

    "GiantO7p7":"#500000", # 暗红色
}
    # "#FF4499", # 粉色
    # "#FF88AA", # 浅粉色
    # "black", 
    # "#FF2277", # 粉色
    # "#664433", # 棕色
    # "#AA7744", # 浅棕色
    # "#FF7744", # 深橙色
    # "#CCDDFF", # 很浅的蓝色
    # "I": "#007777", # 深蓝绿色 
    # "I2": "#009999", # 蓝绿色
    # "I3": "#00AAAA", # 稍浅蓝绿色
    # "I4": "#00BBBB", # 浅蓝绿色
    # "O": "blue", # 亮蓝色
    # "S": "red",
    # "T": "yellow", # 金黄色
    # "L": "purple",
    # "J": "orange",
    # "Z": "Cyan", # 亮青色




def draw_cell_by_cr(c, r, color="#CCCCCC", tag_kind=""):
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
    canvas.delete("falling") # 

    dc, dr = direction
    new_c, new_r = c+dc, r+dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块
    draw_cells(new_c, new_r, cell_list, SHAPESCOLOR[shape_type])
    
    if dc!=0: # 左右移动
        draw_bottom() # 更新底部指示条


def draw_vertical_line(ci): # 
    cr = [ci, 0]
    kind = 'Boom'
    block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': SHAPES6[kind], # 方块列表
        'cr': cr # 中心点的行列
    }
    color = SHAPESCOLOR[block['kind']]

    if ci==0:
        for i in range(0,R):
            draw_cell_by_cr(ci,i,color) # 变红
    elif ci<C:
        for i in range(0,R):
            draw_cell_by_cr(ci,i,color) # 变红
            draw_cell_by_cr(ci-1,i) # 变灰
    else: # ci==C
        for i in range(0,R):
            draw_cell_by_cr(ci-1,i) # 变灰


def generate_new_block():
    shapes = [None, SHAPES1, SHAPES2, SHAPES3, SHAPES4, SHAPES5, SHAPES6]
    shape_now = SHAPES1

    global level_now
    try:
        shape_now = shapes[level_now]
    except:
        print("ERROR level") # 

    global next_block_kind
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
        # draw_vertical_line() # 召唤流星雨
        kind = next_block_kind # 

    # 对应横纵坐标，以左上角为原点，水平向右为x轴正方向，
    # 竖直向下为y轴正方向，x对应横坐标，y对应纵坐标
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': shape_now[kind], # 方块列表
        'cr': cr # 中心点的行列
    }
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


def draw_label():
    global score, level_now, revive_num, next_block_kind, skill_point
    label.config(text = "得分{} 关卡{} 下一个{}\n复活次数{} 技能点数{}"
                 .format(score, level_now, next_block_kind, revive_num, skill_point))


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



# 更新得分
def update_score(cnt):
    global score
    score += cnt # 得分增加
    check_level()
    draw_board() # 重新绘制
    draw_label()


def boom_clear(block):
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
                block_list[dr][dc]='' # 消除
                cnt+=1
    
    update_score(cnt)
    # draw_board() # 重新绘制


def addBoom_clear(block):
    c,r = block['cr']
    cnt=0
    for i in range(-1,2):
        for j in range(0,R):
            dc=c+i
            if dc<0 or dc>=C: # C=列数
                continue 
            if(block_list[j][dc]!=''): # 
                block_list[j][dc]='' # 消除
                cnt+=1

    for i in range(-1,2):
        for j in range(0,C):
            dr=r+i
            if dr<0 or dr>=R: # R=行数
                continue 
            if(block_list[dr][j]!=''): # 
                block_list[dr][j]='' # 消除
                cnt+=1

    update_score(cnt)
    # draw_board() # 重新绘制


def check_and_clear():
    has_complete_row = False
    # 连续消除得分更高
    score1=10 # 可以增加的分
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            # 当前行可消除
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_list[cur_ri] = block_list[cur_ri-1][:]
                block_list[0] = ['' for j in range(C)]
            else:
                block_list[ri] = ['' for j in range(C)]
            global score
            score += score1 # 得分增加
            score1 += 10 # 连续消除得分：10,20,30,40,...
            # 消除1行：10分, 消除2行：30分, 
            # 消除3行：60分, 消除4行：100分, 以此类推

    if has_complete_row:
        check_level() # 更新当前关卡
        draw_board() # 重新绘制
        draw_label()


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
    if is_paused: # 暂停中
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
    if is_paused: # 暂停中
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
    if is_paused: # 暂停中
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


def game_loop():
    global skill_using, fall_ci, fps, oldfps, canvas, vis, visold

    if skill_using: # 正在使用技能
        if fall_ci<=C: # 
            draw_vertical_line(fall_ci) # 
            fall_ci += 1
            win.after(fps, game_loop) # 
            return
        else:
            fps = oldfps
            skill_using = False # 技能释放结束
            canvas.destroy() # 删除原有canvas
            canvas = create_canvas() # 新建canvas
            draw_board(True) # 第一次绘制
            vis = [0 for i in range(C)]
            visold = [1 for i in range(C)]
            draw_bottom() # 更新底部指示条
    
    if is_paused: # 暂停中
        win.after(fps, game_loop) # 
        return  
    
    win.update()
    global current_block
    if current_block is None:
        new_block = generate_new_block()
        
        if skill_using: # 正在使用技能
            # 清屏
            global block_list
            block_list = []
            for i in range(R):
                i_row = ['' for j in range(C)]
                block_list.append(i_row)

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
        if not check_move(current_block, [0, 0]):
            global revive_num
            if revive_num<=0:
                messagebox.showinfo("游戏结束！", "最终得分：%s分" % score)
                init()
                return
            else: # revive_num>=1
                revive()
                
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

    if is_paused: # 暂停
        global score, level_now, revive_num, next_block_kind
        label.config(text = "得分{} 关卡{} 下一个{}\n复活次数{} 技能点数{}\n暂停中，按p键继续游戏"
                 .format(score, level_now, next_block_kind, revive_num, skill_point)) # p
        
    else: # 继续
        draw_label()


def use_skill(): # 
    global next_block_kind
    global skill_point

    if next_block_kind!="Skill": # 下一个不是用技能
        skill_point -= 1 # 消耗技能点
        next_block_kind = "Skill" # 下一个改为使用技能
        draw_label()

def print_lack_skill():
    # print("技能点不足") # 
    global score, level_now, revive_num, next_block_kind, skill_point
    label.config(text = "得分{} 关卡{} 下一个{}\n复活次数{} 技能点数{}(技能点不足)"
                 .format(score, level_now, next_block_kind, revive_num, skill_point))


def skill(): # 放技能
    global skill_point
    if skill_point>=1: # 技能点足够
        use_skill()
    else:
        print_lack_skill()
        


def press_key(event):
    if event.char.lower() == 'p':
        pause()
    else:
        global is_paused
        if is_paused == False: # 不在暂停状态
            if event.char.lower() == 'o':
                skill()


# def clear_canvas():

def create_canvas():
    canvas = tk.Canvas(win, width=width, height=height)
    canvas.pack()
    check_level() # 更新关卡
    draw_label() # 更新label，标题中展示分数和关卡
    canvas.focus_set() # 聚焦到canvas画板对象上
    canvas.bind("<KeyPress-Left>", horizontal_move_block)
    canvas.bind("<KeyPress-Right>", horizontal_move_block)
    canvas.bind("<KeyPress-Up>", rotate_block)
    canvas.bind("<KeyRelease-Up>", on_up_key_release) # 
    canvas.bind("<KeyPress-Down>", land)
    canvas.bind("<KeyPress>", press_key) # 
    return canvas


def create_win():
    win = tk.Tk() # 游戏界面
    win.title("俄罗斯方块")
    win.protocol("WM_DELETE_WINDOW", closing_win) # 

    global label, canvas
    label = Label(win, text="")
    label_font = font.Font(size=15) # 
    label.configure(font=label_font)
    label.pack(side='top', anchor='w') # 上面，向左对齐

    canvas = create_canvas() # 新建canvas
    draw_board(True) # 第一次绘制

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

    win.mainloop()


def open_link():
    webbrowser.open('https://github.com/Frank-Star-fn/Tetris_v2')

def create_root():
    global root 
    root = tk.Tk()
    root.title("俄罗斯方块")
    root.protocol("WM_DELETE_WINDOW", closing_root)

    # 获取屏幕的高度
    screen_height = root.winfo_screenheight()

    # 设置界面大小
    global width
    root_width = width
    root_height = screen_height//3
    root.geometry(f"{root_width}x{root_height}")

    # 计算按钮的位置
    button_width = 150
    button_height = 80
    button_x = (root_width // 2) - (button_width // 2) 
    button_y = (root_height // 2) - (button_height // 2)  # 

    button = tk.Button(root, text="开始游戏", font=('黑体', 20), command=main) # 创建按钮
    button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 

    text_rule = '\n游戏规则：填满一行即消除，堆满方块则失败。\n\n操作：左右键移动，上键旋转，下键快速下落，\np键暂停，o键释放技能。'
    label_rule = tk.Label(root, text=text_rule, font=('黑体', 13))
    label_rule.pack() # 

    label_web = tk.Label(root, text='俄罗斯方块-项目链接', fg='blue', cursor='hand2')
    label_web.pack(side='bottom', anchor='s') # 放在底部
    label_web.bind('<Button-1>', lambda e: open_link())

    root.deiconify() # 显示开始界面
    return root 


def init(first = False):
    global level_now, level_old, fps, oldfps, score, current_block, next_block_kind, revive_num
    global block_list, win, root, vis, visold, is_up_key_pressed, is_paused, skill_point, skill_using, fall_ci

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
    # fps = 100 # 
    # SHAPES1 = { # 
    #     "I1p6": [(0,3),(0,2),(0,1),(0,0),(0,-1),(0,-2)], # 1*6
    # }

def test_use(): # 测试用
    global score, revive_num, skill_point
    # score = 599 # 直接改初始score 
    # revive_num = 0 # 直接改复活次数
    # skill_point = 999 # 直接改技能点


if __name__ == "__main__":
    init(True) # 初始化
    
