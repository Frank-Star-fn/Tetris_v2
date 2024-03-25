import tkinter as tk
import random
import time

Duration_Time = 500 # 持续时间
Size = 3 # 大小
Width = 600
Height = 600
Fragments_Num = 50


def boss_explode_animation(canvas, x, y, size=Size, duration=Duration_Time):
    # 创建爆炸效果的碎片
    fragments = []
    for _ in range(Fragments_Num):
        dx = random.randint(0, 10)
        dy = random.randint(0, 10)
        if dx*dx+dy*dy<=4: # 避免太慢
            dx = random.randint(0, 11)
            dy = random.randint(0, 11)

        t1 = random.randint(0, 1)
        if t1==0:
            dx = -dx
        t2 = random.randint(0, 1)
        if t2==0:
            dy = -dy

        sz = random.randint(0, size) # 随机大小
        fragment = canvas.create_rectangle(x-sz, y-sz, x+sz, y+sz, outline="red", fill="orange")
        fragments.append((fragment, dx, dy))

    if canvas.winfo_exists():  # 检查窗口是否存在
        # 在这里更新窗口或部件的内容
        canvas.after(0, update_fragments, canvas, fragments, duration, 0) # 更新碎片的位置，创建动画效果


def update_fragments(canvas, fragments, duration, elapsed_time):
    try:
        if canvas.winfo_exists == False: # 
            return

        # 计算动画已经进行的时间
        elapsed_time += 10 #

        if elapsed_time < duration:
            # 更新碎片的位置
            for fragment, dx, dy in fragments:
                canvas.move(fragment, dx, dy)
            
            if canvas.winfo_exists():  # 检查窗口是否存在
                canvas.after(10, update_fragments, canvas, fragments, duration, elapsed_time)

        else:
            # 删除爆炸效果中的所有碎片
            for fragment, _, _ in fragments:
                canvas.delete(fragment)
    except:
        print("ERROR when update_fragments")


# def change_color(canvas, r, g, b):
#     # 逐渐变暗
#     if r > 0 or g > 0 or b > 0:
#         r = max(0, r - 2)
#         g = max(0, g - 2)
#         b = max(0, b - 2)
#         color = "#{:02x}{:02x}{:02x}".format(r, g, b)
#         canvas.config(bg=color)
#         canvas.after(4, change_color, canvas, r, g, b)


# def explode(canvas):
#     change_color(canvas, 100, 100, 100)
#     canvas.after(0, boss_explode_animation, canvas, Width//2, Height//2)


        
# def main():
#     root = tk.Tk()
#     root.title("Boss Explode Animation")
    
#     # canvas = tk.Canvas(root, width=Width, height=Height, bg="black")
#     canvas = tk.Canvas(root, width=Width, height=Height, bg="#646464")
#     canvas.pack()
    
#     # 在画布上创建一个按钮，点击时触发Boss自爆动画
#     button = tk.Button(root, text="Boss Explode", command=lambda: explode(canvas))
#     button.pack()
    
#     root.mainloop()

# if __name__ == "__main__":
#     main()
