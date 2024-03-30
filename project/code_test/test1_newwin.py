import tkinter as tk

def open_store():
    store_window = tk.Toplevel(main_window)
    store_window.title("商店")
    store_window.geometry("400x300")
    
    # 在子页面中添加其他部件
    label = tk.Label(store_window, text="欢迎来到商店！")
    label.pack()

# 创建主窗口
main_window = tk.Tk()
main_window.title("主页面")

# 创建商店按钮
store_button = tk.Button(main_window, text="商店", command=open_store)
store_button.pack()

# 运行主循环
main_window.mainloop()
