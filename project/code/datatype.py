C = 14 # 12
R = 22 # 20

class DataOut:
    def __init__(self):
        # 局外变量
        self.win_times = 0
        self.gold = 0
        self.init_revive_num = 0 # 初始复活次数
        self.init_skill_points = 0 # 初始技能点数
        self.highest_score = 0  # 最高分
        self.new_check_date = None # 最近的签到日期

class Data:
    def __init__(self):
        # 每局都初始化的全局变量(局内变量)
        self.level_now = 1 # 关卡数
        self.level_old = 1
        self.score = 0 # 得分
        self.fps = 800 # 刷新页面的毫秒间隔
        self.oldfps = 800
        self.revive_num = 1 # 复活次数
        self.current_block = None
        self.next_block_kind = ""
        self.block_list = []
        for i in range(R):
            i_row = ['' for j in range(C)]
            self.block_list.append(i_row)

        self.is_up_key_pressed = False
        self.is_paused = False
        self.skill_point = 1 # 技能点
        self.skill_using = False
        self.fall_ci = 0
        self.boss_hp = 300
        self.boss_hp_old = self.boss_hp
        self.image_id = 0
        self.image_block_id = 0
        self.left_turn = 30 # 剩余回合数