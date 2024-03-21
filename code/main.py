import tkinter as tk
from tkinter import messagebox
import random
import copy

# 常量定义
cell_size = 30
C = 14 # 12
R = 24 # 20
height = R * cell_size
width = C * cell_size
level_score = [300, 600, 900, 1200] # 进入下一关所需的得分
level_fps = [0, 800, 750, 700, 680, 660] # 每关对应的fps

# 全局对象定义
root = tk.Tk() # 开始界面
win = tk.Tk() # 游戏界面
canvas = tk.Canvas(win, width=width, height=height, )

# 全局变量定义
level_now = 1 # 关卡数
score = 0 # 得分
fps = 800 # old 200, 刷新页面的毫秒间隔
revive_num = 1 # 复活次数
current_block = None
block_list = []
first_game = True


# 加入闯关机制
# 定义各种形状
# 第1关
SHAPES1 = {
    "Small":[(0, 0)], # 1*1
    "Small2":[(0, 0)], # 1*1
    "Boom":[(0, 0)], # 1*1,炸附近3*3,每个1分
    
    "SmallI": [(0, 1), (0, 0)], # 1*2
    "Dots2" : [(1, 0), (-1, 0)],
    "Dots2v2" : [(0, 0), (1, 1)],

    "I1p3": [(0, 1), (0, 0), (0, -1)], # 1*3
    "SmallL": [(0, 1), (0, 0), (1, 0)], # corner

    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],

    "AddBoom": [(-1,0), (0,-1), (0,0), (1,0), (0,1)], # +,消除三行三列
    
    "I1p6": [(0,2), (0,1), (0,0),(0,-1),(0,-2),(0,-3)], # 1*6
    "I2p3": [(0,-1), (0,0),(1,0),(1,-1),(-1,0),(-1,-1)],# 2*3
}

# 第2关, 增加方块: "BigO","F"
SHAPES2 = copy.deepcopy(SHAPES1)
SHAPES2["BigO"]=[(0,0),(0,1),(0,-1),(-1,0),(-1,1),(-1,-1),(1,0),(1,1),(1,-1)] # 3*3
SHAPES2["F"]=[(0,2), (0,1), (0,0),(0,-1),(1,-1),(1,1)]

# 第3关, 增加方块: "HugeO","Add"
SHAPES3 = copy.deepcopy(SHAPES2)
SHAPES3["HugeO"]=[(0,0),(-1,-1),(0,-1),(-1,0),(-2,-2),(-2,-1),(-2,0),(-1,-2),(0,-2),
               (1,1),(1,0),(1,-1),(1,-2),(0,1),(-1,1),(-2,1)] # 4*4
SHAPES3["Add"]=[(-1,0), (0,-1), (0,0), (1,0), (0,1)] # +

# 第4关, 增加方块: "BigT", "Dots4"
SHAPES4 = copy.deepcopy(SHAPES3)
SHAPES4["BigT"]=[(0,0),(0,1),(0,2),(0,-1),(0,-2),(1,0),(2,0)]
SHAPES4["Dots4"]=[(1,1),(1,-1),(-1,-1),(-1,1)] # Hard # 注意不要有多余的逗号

# 第5关, 增加方块: "GiantO"(Very Hard)
SHAPES5 = copy.deepcopy(SHAPES4)
SHAPES5["GiantO"]=[(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),
              (1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),
              (2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),
              (3,-3),(3,-2),(3,-1),(3,0),(3,1),(3,2),(3,3),
              (-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),
              (-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),
              (-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),] # 7*7, Very Hard
# SHAPES5["King"]=[(0,0),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)] # Very Hard


SHAPES = {
    # "Small":[(0, 0)], # 1*1
    # "Small2":[(0, 0)], # 1*1
    # "Boom":[(0, 0)], # 1*1,炸附近3*3,每个1分
    
    # "SmallI": [(0, 1), (0, 0)], # 1*2
    # "Dots2" : [(1, 0), (-1, 0)],
    # "Dots2v2" : [(0, 0), (1, 1)],

    # "I1p3": [(0, 1), (0, 0), (0, -1)], # 1*3
    # "SmallL": [(0, 1), (0, 0), (1, 0)], # corner

    # "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    # "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    # "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    # "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    # "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    # "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    # "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    # "Dots4":[(1,1),(1,-1),(-1,-1),(-1,1)], # Hard
    # "Dots4v2":[(1,0),(-1,0),(0,-1),(0,1)], # Very Hard

    # "Add": [(-1,0), (0,-1), (0,0), (1,0), (0,1)], # +
    # "AddBoom": [(-1,0), (0,-1), (0,0), (1,0), (0,1)], # +
    
    # "I1p6": [(0,2), (0,1), (0,0),(0,-1),(0,-2),(0,-3)], # 1*6
    # "I2p3": [(0,-1), (0,0),(1,0),(1,-1),(-1,0),(-1,-1)],# 2*3
    # "F": [(0,2), (0,1), (0,0),(0,-1),(1,-1),(1,1)], 

    # "BigT":[(0,0),(0,1),(0,2),(0,-1),(0,-2),(1,0),(2,0)],

    # "BigO": [(0,0),(0,1),(0,-1),(-1,0),(-1,1),(-1,-1),(1,0),(1,1),(1,-1)], # 3*3
    # "BigAdd":[(0,0),(0,1),(0,2),(0,-1),(0,-2),(1,0),(2,0),(-1,0),(-2,0)], # Super Hard
    
    # "King":[(0,0),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)], # Very Hard
    # "Num5":[(0,0), (1,1),(-1,-1),(1,0),(-1,0), (0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)], # Super Hard
    
    # "HugeO" : [(0,0),(-1,-1),(0,-1),(-1,0),(-2,-2),(-2,-1),(-2,0),(-1,-2),(0,-2),
    #            (1,1),(1,0),(1,-1),(1,-2),(0,1),(-1,1),(-2,1)], # 4*4
    
    # "GiantO":[(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),
    #           (1,-3),(1,-2),(1,-1),(1,0),(1,1),(1,2),(1,3),
    #           (2,-3),(2,-2),(2,-1),(2,0),(2,1),(2,2),(2,3),
    #           (3,-3),(3,-2),(3,-1),(3,0),(3,1),(3,2),(3,3),
    #           (-1,-3),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),(-1,3),
    #           (-2,-3),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2),(-2,3),
    #           (-3,-3),(-3,-2),(-3,-1),(-3,0),(-3,1),(-3,2),(-3,3),], # 7*7, Very Hard
}


# 定义各种形状的颜色
SHAPESCOLOR = {
    "Small": "#0011CC", # 蓝色
    "Small2": "#004499", # 深蓝绿
    "Boom":"#DD0000", # 红色
    
    "SmallI": "#AACC66", # 草绿色
    "Dots2" : "green", 
    "Dots2v2" : "#00AA11",

    "I1p3": "#8899FF", # 浅蓝色
    "SmallL": "#EE8877", # 砖红色

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

    "BigO":"#004488", # 深蓝色
    "BigAdd":"#884400", # 棕色

    "King":"#FFFF66", # 金色
    "Num5":"#336633", # 深绿色

    "HugeO" : "#AA0000", # 深红色
    "Nazi":"#000000", # 黑色

    "GiantO":"#500000", # 暗红色
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



def draw_cell_by_cr(canvas, c, r, color="#CCCCCC", tag_kind=""):
    """
    :param canvas: 画板，用于绘制一个方块的Canvas对象
    :param c: 方块所在列
    :param r: 方块所在行
    :param color: 方块颜色，默认为#CCCCCC，轻灰色
    :return:
    """
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = c * cell_size + cell_size
    y1 = r * cell_size + cell_size
    if tag_kind == "falling":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color,outline="white", width=2, tag=tag_kind)
    elif tag_kind == "row":
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2, tag="row-%s" % r)
    else:
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)




# 绘制面板, 只有在第一次绘制时才绘制背景色方块
def draw_board(canvas, block_list, isFirst=False):
    # 删掉原来所有的行
    for ri in range(R):
        canvas.delete("row-%s" % ri)

    for ri in range(R):
        for ci in range(C):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_cell_by_cr(canvas, ci, ri, SHAPESCOLOR[cell_type], tag_kind="row")
            elif isFirst:
                draw_cell_by_cr(canvas, ci, ri)


def draw_cells(canvas, c, r, cell_list, color="#CCCCCC"):
    """
    绘制指定形状指定颜色的俄罗斯方块
    :param canvas: 画板
    :param r: 该形状设定的原点所在的行
    :param c: 该形状设定的原点所在的列
    :param cell_list: 该形状各个方格相对自身所处位置
    :param color: 该形状颜色
    :return:
    """
    for cell in cell_list:
        #
        # print("cell =", cell) #

        cell_c, cell_r = (0, 0)
        try:
            cell_c, cell_r = cell # 
        except:
            print("ERROR cell")
            print("cell =", cell)

        ci = cell_c + c
        ri = cell_r + r
        # 判断该位置方格在画板内部(画板外部的方格不再绘制)
        if 0 <= c < C and 0 <= r < R:
            draw_cell_by_cr(canvas, ci, ri, color, tag_kind="falling")


def draw_block_move(canvas, block, direction=[0, 0]):
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

    # 移动前，清除原有位置绘制的俄罗斯方块
    canvas.delete("falling")

    dc, dr = direction
    new_c, new_r = c+dc, r+dr
    block['cr'] = [new_c, new_r]
    # 在新位置绘制新的俄罗斯方块就好
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])


def generate_new_block():
    shape_now = SHAPES
    global level_now
    if level_now==1:
        shape_now = SHAPES1
    elif level_now==2:
        shape_now = SHAPES2
    elif level_now==3:
        shape_now = SHAPES3
    elif level_now==4:
        shape_now = SHAPES4
    elif level_now==5:
        shape_now = SHAPES5
    else:
        print("ERROR level") # 

    # 随机生成新的俄罗斯方块
    kind = random.choice(list(shape_now.keys()))

    # 对应横纵坐标，以左上角为原点，水平向右为x轴正方向，
    # 竖直向下为y轴正方向，x对应横坐标，y对应纵坐标
    cr = [C // 2, 0]
    new_block = {
        'kind': kind,  # 对应俄罗斯方块的类型
        'cell_list': shape_now[kind],
        'cr': cr
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

def draw_title():
    global score
    global level_now
    win.title("得分: %s 关卡: %d 复活次数: %d" % (score, level_now, revive_num))

def check_level(score): # 更新当前关卡
    global fps
    global level_now

    len1=len(level_score)
    for i in range(len1-1,-1,-1): # 
        if score>=level_score[i]:
            level_now = i+2
            fps = level_fps[level_now]
            break
            
    # print("level_now =", level_now) # 
    # print("fps =", fps) # 


# 更新得分
def update_score(cnt):
    global score
    score += cnt # 得分增加
    check_level(score)
    draw_board(canvas, block_list)
    draw_title()


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
            # 消除1行：10分
            # 消除2行：30分
            # 消除3行：60分
            # 消除4行：100分
            # ...类推

    if has_complete_row:
        check_level(score) # 更新当前关卡
        draw_board(canvas, block_list)
        draw_title()


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
        # block_list 在对应位置记下其类型
        block_list[r][c] = shape_type

        draw_cell_by_cr(canvas, c, r, SHAPESCOLOR[shape_type], tag_kind="row")


def horizontal_move_block(event):
    """
    左右水平移动俄罗斯方块
    """
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(canvas, current_block, direction)


def rotate_block(event):
    global current_block
    if current_block is None:
        return

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
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        draw_cells(canvas, cc, cr, rotate_list,SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate


def land(event):
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
        draw_block_move(canvas, current_block, down)

def revive(canvas): # 复活
    # print("revive!") #
    R2 = R//2
    for i in range(0, R2):
        block_list[i] = ['' for j in range(0, C)]

    global revive_num
    revive_num-=1
    draw_board(canvas, block_list)
    draw_title()

def game_loop():
    win.update()
    global current_block
    global canvas
    if current_block is None:
        new_block = generate_new_block()
        # 新生成的俄罗斯方块需要先在生成位置绘制出来
        draw_block_move(canvas, new_block)
        current_block = new_block
        if not check_move(current_block, [0, 0]):
            global revive_num
            if revive_num<=0:
                messagebox.showinfo("Game Over!", "Your Score is %s" % score)
                try:
                    win.withdraw() # 
                except:
                    print("ERROR when win.withdraw()") #

                init()
                return
            
            else: # revive_num>=1
                revive(canvas)
                
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
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


def on_closing():
    root.quit()  # 退出事件循环
    root.destroy()  # 关闭窗口
    win.quit()  # 退出事件循环
    win.destroy()  # 关闭窗口


def main():
    global first_game
    if first_game: # 第一次运行
        first_game = False

        root.withdraw()
        win.deiconify()

        canvas.pack()
        
        check_level(score) # 更新关卡
        draw_title() # 更新标题，标题中展示分数和关卡
        draw_board(canvas, block_list, True)
        canvas.focus_set() # 聚焦到canvas画板对象上

        canvas.bind("<KeyPress-Left>", horizontal_move_block)
        canvas.bind("<KeyPress-Right>", horizontal_move_block)
        canvas.bind("<KeyPress-Up>", rotate_block)
        canvas.bind("<KeyPress-Down>", land)
        win.protocol("WM_DELETE_WINDOW", on_closing)

        win.update()
        win.after(fps, game_loop) # 在fps 毫秒后调用 game_loop方法
        win.mainloop()

    else: # 不是第一次运行
        root.withdraw()
        win.deiconify()
    
        check_level(score) # 更新关卡
        draw_title() # 更新标题，标题中展示分数和关卡
        draw_board(canvas, block_list, True)
        canvas.focus_set() # 聚焦到canvas画板对象上

        win.update()
        win.after(fps, game_loop) # 在fps 毫秒后调用 game_loop方法


def test_use(): # 测试用
    global score, revive_num, fps, SHAPES1
    # score = 0 # 1200 # 直接改初始score 
    # revive_num = 0 # 直接改复活次数
    # fps = 100
    # SHAPES1 = {
    #     "I1p6": [(0,2), (0,1), (0,0),(0,-1),(0,-2),(0,-3)], # 1*6
    # }
    

def init(first = False):
    global level_now, fps, score, current_block, revive_num, block_list, win, root 
    level_now = 1 # 关卡数
    fps = 800 # old 200, 刷新页面的毫秒间隔
    score = 0 # 得分
    current_block = None
    revive_num = 1 # 复活次数
    block_list = []
    for i in range(R):
        i_row = ['' for j in range(C)]
        block_list.append(i_row)

    test_use() # 测试用

    if first: # 第一次初始化
        root.title("俄罗斯方块")
        root.protocol("WM_DELETE_WINDOW", on_closing)

        # 获取屏幕的宽度和高度
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # 设置界面大小
        global width
        root_width = width
        root_height = screen_height//3
        root.geometry(f"{root_width}x{root_height}")
        # print("screen_width =", screen_width) # 

        # 计算按钮的位置
        button_width = 120
        button_height = 80
        button_x = (root_width // 2) - (button_width // 2) 
        button_y = (root_height // 2) - (button_height // 2) - 20 # 

        button = tk.Button(root, text="开始游戏", command=main) # 创建按钮
        button.place(x=button_x, y=button_y, width=button_width, height=button_height) # 
        # button.pack()

        try:
            win.withdraw() # 撤回游戏界面
        except:
            print("ERROR when win.withdraw()") 
        root.deiconify() # 显示开始界面
        root.mainloop() # 启动主循环
        
    else: # 不是第一次初始化
        try:
            win.withdraw() # 撤回游戏界面
            root.deiconify() # 显示开始界面
        except:
            print("Error in operating interface") 
        

if __name__ == "__main__":
    init(True) # 初始化
    
