import tkinter as tk

def open_new_window():
    # root.withdraw() # 隐藏

    new_window = tk.Toplevel(root)  # 创建新窗口
    new_window.geometry(f"{400}x{400}")
    new_window.title("New Window")
    
    # 添加一些组件到新窗口
    label = tk.Label(new_window, text="New Window Content")
    label.pack()
    
    # 设置焦点到新窗口
    new_window.focus_set()

root = tk.Tk()
root.geometry(f"{400}x{400}")

# 添加按钮用于打开新窗口
button = tk.Button(root, text="Open New Window", command=open_new_window)
button.pack()

root.mainloop()
