import copy

# 第1关的各方块
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

# 第7关, boss关
SHAPES7 = copy.deepcopy(SHAPES6)
SHAPES7["King"]=[(0,0),(0,1),(0,-1),(1,0),(-1,0),(0,2),(0,-2),(-1,-2),(1,-2),(-1,2),(1,2)] # Very Hard

# 其他方块：
# SHAPES7["GiantO7p7"]=[(0,-3),(0,-2),(0,-1),(0,0),(0,1),(0,2),(0,3),
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



# 是否可以旋转
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