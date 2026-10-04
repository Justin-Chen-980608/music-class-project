#!/usr/bin/env python
# coding: utf-8

# In[101]:


import tkinter as tk
from tkinter import messagebox as msgbox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from tkinter import ttk
import numpy as np
import sqlite3 as s
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
#new
#pyinstaller --onefile --windowed --hidden-import=matplotlib.backends.backend_tkagg "點名系統.py"
#pyinstaller --windowed "點名系統.py"

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3 as s

def delete_attendance_data():
    w_3 = tk.Toplevel()
    w_3.title("刪除出席紀錄")
    w_3.geometry("500x460")
    w_3.config(bg="#B3D9D9")

    # === Label ===
    tk.Label(w_3, text="學生姓名：", bg="#B3D9D9").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(w_3, text="日期（day）：", bg="#B3D9D9").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(w_3, text="星期（date）：", bg="#B3D9D9").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(w_3, text="時間：", bg="#B3D9D9").grid(row=3, column=0, padx=10, pady=5)
    tk.Label(w_3, text="課程：", bg="#B3D9D9").grid(row=4, column=0, padx=10, pady=5)
    tk.Label(w_3, text="出席狀態：", bg="#B3D9D9").grid(row=5, column=0, padx=10, pady=5)

    # === Variables ===
    d_name = tk.StringVar()
    d_day = tk.StringVar()
    d_date = tk.StringVar()
    d_time = tk.StringVar()
    d_course = tk.StringVar()
    d_atd = tk.StringVar()

    # === Comboboxes ===
    combo_name = ttk.Combobox(w_3, textvariable=d_name, state="readonly", width=25)
    combo_day = ttk.Combobox(w_3, textvariable=d_day, state="readonly", width=25)
    combo_date = ttk.Combobox(w_3, textvariable=d_date, state="readonly", width=25)
    combo_time = ttk.Combobox(w_3, textvariable=d_time, state="readonly", width=25)
    combo_course = ttk.Combobox(w_3, textvariable=d_course, state="readonly", width=25)
    combo_atd = ttk.Combobox(w_3, textvariable=d_atd, state="readonly", width=25, values=["y", "n"])

    combo_name.grid(row=0, column=1)
    combo_day.grid(row=1, column=1)
    combo_date.grid(row=2, column=1)
    combo_time.grid(row=3, column=1)
    combo_course.grid(row=4, column=1)
    combo_atd.grid(row=5, column=1)

    # === Tree 顯示所有資料 ===
    columns = ("name", "day", "date", "time", "課程", "atd")
    tree6 = ttk.Treeview(w_3, columns=columns, show="headings", height=8)
    for col in columns:
        tree6.heading(col, text=col)
        tree6.column(col, width=80, anchor="center")
    tree6.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    # === 載入學生名單 ===
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM class")
    combo_name["values"] = [row[0] for row in c.fetchall()]
    conn.close()

    # === 事件綁定 ===
    combo_name.bind("<<ComboboxSelected>>", lambda e: update_day())
    combo_day.bind("<<ComboboxSelected>>", lambda e: update_date())
    combo_date.bind("<<ComboboxSelected>>", lambda e: update_time())
    combo_time.bind("<<ComboboxSelected>>", lambda e: update_course())

    # === 更新下拉選單 ===
    def update_day():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT day FROM class WHERE name=?", (d_name.get(),))
        combo_day["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_day.set(""); combo_date.set(""); combo_time.set(""); combo_course.set(""); combo_atd.set("")

    def update_date():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM class WHERE name=? AND day=?", (d_name.get(), d_day.get()))
        combo_date["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_date.set(""); combo_time.set(""); combo_course.set(""); combo_atd.set("")

    def update_time():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT time FROM class WHERE name=? AND day=? AND date=?", 
                  (d_name.get(), d_day.get(), d_date.get()))
        combo_time["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_time.set(""); combo_course.set(""); combo_atd.set("")

    def update_course():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT 課程 FROM class WHERE name=? AND day=? AND date=? AND time=?", 
                  (d_name.get(), d_day.get(), d_date.get(), d_time.get()))
        combo_course["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_course.set(""); combo_atd.set("")

    # === 查詢 ===
    def query_data():
        tree6.delete(*tree6.get_children())
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        sql = "SELECT * FROM class WHERE 1=1"
        params = []
        if d_name.get():
            sql += " AND name=?"; params.append(d_name.get())
        if d_day.get():
            sql += " AND day=?"; params.append(d_day.get())
        if d_date.get():
            sql += " AND date=?"; params.append(d_date.get())
        if d_time.get():
            sql += " AND time=?"; params.append(d_time.get())
        if d_course.get():
            sql += " AND 課程=?"; params.append(d_course.get())
        if d_atd.get():
            sql += " AND atd=?"; params.append(d_atd.get())
        for rec in c.execute(sql, params):
            tree6.insert("", "end", values=rec)
        conn.close()

    tk.Button(w_3, text="查詢出席紀錄", command=query_data).grid(row=6, column=0, pady=10)

    # === 刪除 ===
    def delete_selected():
        if not (d_name.get() and d_day.get() and d_date.get() and d_time.get() and d_course.get() and d_atd.get()):
            msgbox.showwarning("警告", "請完整選擇所有欄位！")
            return

        confirm = msgbox.askyesno("確認刪除", "確定要刪除此出席紀錄嗎？")
        if not confirm:
            return

        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("""
            DELETE FROM class 
            WHERE name=? AND day=? AND date=? AND time=? AND 課程=? AND atd=?
        """, (d_name.get(), d_day.get(), d_date.get(), d_time.get(), d_course.get(), d_atd.get()))
        conn.commit()
        conn.close()

        msgbox.showinfo("完成", "出席紀錄刪除成功。")
        query_data()  # 更新列表

    tk.Button(w_3, text="刪除選取紀錄", command=delete_selected, bg="red", fg="white").grid(row=6, column=1, pady=10)






def show_attendance_window():
    global w_4, tree3, start_date_var, end_date_var, student_var

    w_4 = tk.Toplevel()
    w_4.title("出席率查詢")
    w_4.geometry("750x205")
    w_4.config(bg='#B3D9D9')

    # --- 選擇時間範圍 ---
    tk.Label(w_4, text='起始日期 (YYYYMMDD)', bg='#B3D9D9').place(x=520,y=10)
    start_date_var = tk.StringVar()
    tk.Entry(w_4, width=10, textvariable=start_date_var).place(x=660,y=11)

    tk.Label(w_4, text='結束日期 (YYYYMMDD)', bg='#B3D9D9').place(x=520,y=50)
    end_date_var = tk.StringVar()
    tk.Entry(w_4, width=10, textvariable=end_date_var).place(x=660,y=51)

    # --- 選擇學生 ---
    tk.Label(w_4, text='學生', bg='#B3D9D9').place(x=520,y=90)
    student_var = tk.StringVar()
    combo_student = ttk.Combobox(w_4, textvariable=student_var, state="readonly", width=20)
    conn = sqlite3.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM class")
    combo_student['values'] = [row[0] for row in c.fetchall()]
    conn.close()
    combo_student.place(x=560,y=91)

    # --- 查詢所有學生出席率 ---
    tk.Button(w_4, text='查詢出席率', bg="#FF6666", fg="white", command=query_attendance_range).place(x=520,y=150)

    # --- 折線圖按鈕 ---
    tk.Button(w_4, text='查看折線圖', bg="#66CCFF", fg="white", command=show_attendance_chart_window).place(x=620,y=150)

    # --- Treeview 顯示出席率 ---
    tree3 = ttk.Treeview(w_4, show='headings', columns=('姓名','出席率'))
    tree3.column('姓名', anchor='center', width=200)
    tree3.column('出席率', anchor='center', width=100)
    tree3.heading('姓名', text='姓名')
    tree3.heading('出席率', text='出席率 (%)')
    tree3.place(x=10, y=10, width=500, height=180)


# --- 查詢函式，更新 tree3 ---
def query_attendance_range():
    s_date = start_date_var.get()
    e_date = end_date_var.get()

    if not s_date or not e_date:
        msgbox.showwarning("警告", "請輸入完整的日期範圍！")
        return

    conn = sqlite3.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT name, SUM(CASE WHEN atd='y' THEN 1 ELSE 0 END), COUNT(*) FROM class WHERE day BETWEEN ? AND ? GROUP BY name", (s_date, e_date))
    records = c.fetchall()
    conn.close()

    tree3.delete(*tree3.get_children())
    for i, r in enumerate(records):
        name = r[0]
        attend_rate = round(r[1]/r[2]*100, 2) if r[2]>0 else 0
        tree3.insert(parent='', index=i, iid=i, text='', values=(name, attend_rate))


# --- 按下折線圖按鈕，跳到新視窗 ---
def show_attendance_chart_window():
    student_name = student_var.get()
    if not student_name:
        msgbox.showwarning("警告", "請先選擇學生！")
        return

    # --- 讓使用者輸入年份 ---
    year_win = tk.Toplevel()
    year_win.title("輸入年份")
    year_win.geometry("300x120")
    year_win.config(bg="#B3D9D9")

    tk.Label(year_win, text="請輸入年份 (例如：2025)", bg="#B3D9D9").pack(pady=10)
    year_var = tk.StringVar()
    tk.Entry(year_win, textvariable=year_var, width=10).pack()

    def generate_chart():
        year = year_var.get()
        if not year.isdigit() or len(year) != 4:
            msgbox.showwarning("錯誤", "請輸入正確的年份（例如 2025）")
            return

        conn = sqlite3.connect('./點名系統.db')
        c = conn.cursor()
        # 假設 day 欄位格式為 YYYYMMDD
        c.execute("""
            SELECT day, atd FROM class 
            WHERE name=? AND substr(day,1,4)=? 
            ORDER BY day
        """, (student_name, year))
        records = c.fetchall()
        conn.close()

        if not records:
            msgbox.showinfo("訊息", f"{year} 年無出席資料。")
            return

        # --- 統計每個月的出席率 ---
        month_data = {m: {"present": 0, "total": 0} for m in range(1, 13)}

        for day, atd in records:
            if len(str(day)) >= 6:
                month = int(str(day)[4:6])
                month_data[month]["total"] += 1
                if atd == "y":
                    month_data[month]["present"] += 1

        months = []
        rates = []
        for m in range(1, 13):
            total = month_data[m]["total"]
            present = month_data[m]["present"]
            rate = (present / total * 100) if total > 0 else 0
            months.append(f"{m}月")
            rates.append(rate)

        # --- 顯示長條圖 ---
        chart_win = tk.Toplevel()
        chart_win.title(f"{student_name} - {year} 年各月出席率長條圖")
        chart_win.geometry("900x400")
        chart_frame = tk.Frame(chart_win)
        chart_frame.pack(fill='both', expand=True)

        fig = Figure(figsize=(9, 3.5), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(months, rates, color="#66CCFF")
        ax.set_title(f"{student_name} {year} 年各月出席率", fontsize=12 , pad=20)
        ax.set_xlabel("月份")
        ax.set_ylabel("出席率 (%)")
        ax.set_ylim(0, 100)
        for i, v in enumerate(rates):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

        year_win.destroy()

    tk.Button(year_win, text="生成圖表", command=generate_chart, bg="#66CCFF", fg="white").pack(pady=10)













def fi_query_task():
    global tm,na,tree1,d_name1, d_date1, d_time1, d_course1, combo_name1, combo_date1, combo_time1, combo_course1, w_3 ,tmsh ,tmsh2,combo_yn
    w_3=tk.Toplevel()                                                      
    w_3.title('點名')
    w_3.geometry("1050x300")
    w_3.config(bg='#B3D9D9')
    tk.Label(w_3, text='名字', font='12', bg='#B3D9D9').place(x=10,y=10)
    d_name1 = tk.StringVar()
    combo_name1 = ttk.Combobox(w_3, textvariable=d_name1, state="readonly")
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM student")
    combo_name1["values"] = [row[0] for row in c.fetchall()]
    combo_name1.place(x = 70 , y = 15)

    tk.Label(w_3, text='星期', font='12', bg='#B3D9D9').place(x = 270, y = 10)
    d_date1 = tk.StringVar()
    combo_date1 = ttk.Combobox(w_3, textvariable=d_date1, state="readonly")
    combo_date1.place(x = 330, y = 15)

    tk.Label(w_3, text='時間', font='12', bg='#B3D9D9').place(x = 530, y = 10)
    d_time1 = tk.StringVar()
    combo_time1 = ttk.Combobox(w_3, textvariable=d_time1, state="readonly")
    combo_time1.place(x = 590, y = 15)

    tk.Label(w_3, text='課程', font='12', bg='#B3D9D9').place(x = 790, y = 10)
    d_course1 = tk.StringVar()
    combo_course1 = ttk.Combobox(w_3, textvariable=d_course1, state="readonly")
    combo_course1.place(x = 850, y = 15)

    tk.Button(w_3, text='點名', command=insert_student_task, bg="#FF6666", fg="white").place(x=450,y=60)

    conn.close()

    # --- 綁定事件：連動選單 ---
    combo_name1.bind("<<ComboboxSelected>>", lambda e: update_dates1())
    combo_date1.bind("<<ComboboxSelected>>", lambda e: update_times1())
    combo_time1.bind("<<ComboboxSelected>>", lambda e: update_courses1())
    na=tk.StringVar()
    tk.Radiobutton(w_3, text='未出席', variable=na ,value='n',bg='#FF8800').place(x=10,y=60)
    tk.Radiobutton(w_3, text='出席', variable=na ,value='y',bg='#FF8800').place(x=100,y=60)
    na.set('n')#預設選項
    tm = tk.StringVar()
    tk.Label(w_3, text='年/月/日(ex:20250608)', font='10', bg='#B3D9D9').place(x = 160, y = 60)
    tk.Entry(w_3, width=10, textvariable = tm).place(x=350, y=65)

    tmsh = tk.IntVar()
    tk.Label(w_3, text='年/月/日(ex:20250608)', font='10', bg='#B3D9D9').place(x = 80, y = 110)
    tk.Entry(w_3, width=10, textvariable = tmsh).place(x=270, y=115)
    tk.Button(w_3, text='查詢',width=10, command=qu_fin).place(x=350,y=110)

    tmsh2 = tk.StringVar()
    tk.Label(w_3, text='姓名', font='10', bg='#B3D9D9').place(x = 150, y = 160)
    tk.Entry(w_3, width=10, textvariable = tmsh2).place(x=270, y=165)
    tk.Button(w_3, text='查詢',width=10, command=qu_fin2).place(x=350,y=160)

    tk.Label(w_3, text='是否出席', font='10', bg='#B3D9D9').place(x = 150, y = 210)
    pc = ["y", "n"]
    combo_yn = ttk.Combobox(w_3, values=pc , width=5)
    combo_yn.place(x=270, y=210)
    combo_yn.set("y")
    tk.Button(w_3, text='查詢',width=10, command=qu_fin3).place(x=350,y=210)

    tree1=ttk.Treeview(w_3,show='headings',column=('日期','名字','星期','時間','課程','是否出席'))#顯示層級數據
    tree1.column('星期', anchor='center', width=80)#對齊方式，可選n, ne, e, se, s, sw, w, nw, center
    tree1.column('日期', anchor='center', width=80)
    tree1.column('名字', anchor='center', width=80)
    tree1.column('時間', anchor='center', width=80)
    tree1.column('課程', anchor='center', width=80)
    tree1.column('是否出席', anchor='center', width=80)
    tree1.heading('星期', text='星期')
    tree1.heading('日期', text='日期')
    tree1.heading('名字', text='名字')
    tree1.heading('課程', text='課程')
    tree1.heading('時間', text='時間')
    tree1.heading('是否出席', text='是否出席')
    tree1.place(x=500, y=80, width=500, height=200)    
    w_3.mainloop()
def insert_student_task():
    time_=tm.get()
    data_=d_date1.get()
    name=d_name1.get()
    tt=d_time1.get()
    class_=d_course1.get()
    attend=na.get()
    ans=msgbox.askokcancel('資料新增','確定寫入資料',icon='info')
    if ans==True:
        conn=s.connect('./點名系統.db')#建立資料庫連線
        x=(time_,data_,name,class_,tt,attend)#tuple
        #sql='insert into task (日期,名稱,完成度,重要度) values(?,?,?,?)' #新增語法
        sql='insert into class(day,date,name,課程,time,atd) values(?,?,?,?,?,?)' 
        conn.execute(sql,x)
        conn.commit()#新增、刪除、修改，查詢不用
        conn.close()
        msgbox.showinfo('訊息','新增成功!')    
def qu_fin():
    q_na=tmsh.get()

    tree1.delete(*tree1.get_children())#清空treeview內容
    conn=s.connect('./點名系統.db')#建立資料庫連線
    results=conn.execute('select * from class where day=?',(q_na,)) 
    i=0
    for record in results:        
        tree1.insert(parent='', index=i, iid=i, text='', values=(record[1],record[2],record[0],record[3],record[4],record[5],))
        i=i+1


    conn.close()
def qu_fin2():
    q_na=tmsh2.get()

    tree1.delete(*tree1.get_children())#清空treeview內容
    conn=s.connect('./點名系統.db')#建立資料庫連線
    results=conn.execute('select * from class where name=?',(q_na,)) 
    i=0
    for record in results:        
        tree1.insert(parent='', index=i, iid=i, text='', values=(record[1],record[2],record[0],record[3],record[4],record[5],))
        i=i+1
def qu_fin3():
    q_na=combo_yn.get()

    tree1.delete(*tree1.get_children())#清空treeview內容
    conn=s.connect('./點名系統.db')#建立資料庫連線
    results=conn.execute('select * from class where atd=?',(q_na,)) 
    i=0
    for record in results:        
        tree1.insert(parent='', index=i, iid=i, text='', values=(record[1],record[2],record[0],record[3],record[4],record[5],))
        i=i+1    

    conn.close()
def update_dates1():
    """當選了名字後，更新可選的日期"""
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT date FROM student WHERE name=?", (d_name1.get(),))
    combo_date1["values"] = [row[0] for row in c.fetchall()]
    conn.close()

    combo_date1.set("")
    combo_time1.set("")
    combo_course1.set("")


def update_times1():
    """當選了日期後，更新可選的時間"""
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT time FROM student WHERE name=? AND date=?", 
              (d_name1.get(), d_date1.get()))
    combo_time1["values"] = [row[0] for row in c.fetchall()]
    conn.close()

    combo_time1.set("")
    combo_course1.set("")


def update_courses1():
    """當選了時間後，更新可選的課程"""
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT 課程 FROM student WHERE name=? AND date=? AND time=?", 
              (d_name1.get(), d_date1.get(), d_time1.get()))
    combo_course1["values"] = [row[0] for row in c.fetchall()]
    conn.close()

    combo_course1.set("")
def whatclass():
    global na,tree,combobox4
    w_4=tk.Toplevel()                                                      
    w_4.title('點名')
    w_4.geometry("350x320")
    w_4.config(bg='#B3D9D9')
    values=["週一","週二","週三","週四","週五","週六","週日"]
    combobox4=ttk.Combobox(w_4,values=values,width=10)
    combobox4.place(x=60,y=13)
    combobox4.set("週一") 
    tk.Button(w_4, text='查詢',width=10, command=wcss).place(x=220,y=12)
    tree=ttk.Treeview(w_4,show='headings',column=('星期','名字','時間','課程'))#顯示層級數據
    tree.column('星期', anchor='center', width=80)#對齊方式，可選n, ne, e, se, s, sw, w, nw, center
    tree.column('名字', anchor='center', width=80)
    tree.column('時間', anchor='center', width=80)
    tree.column('課程', anchor='center', width=80)
    tree.heading('星期', text='星期')
    tree.heading('名字', text='名字')
    tree.heading('時間', text='時間')
    tree.heading('課程', text='課程')
    tree.place(x=10,y=50)    
    w_4.mainloop()
def wcss():
    weekday=combobox4.get()

    tree.delete(*tree.get_children())#清空treeview內容
    conn=s.connect('./點名系統.db')#建立資料庫連線
    results=conn.execute('select * from student where date=? order by time(time) ',(weekday,)) 
    i=0
    for record in results:        
        tree.insert(parent='', index=i, iid=i, text='', values=(record[1],record[0],record[2],record[3]))
        i=i+1
    conn.close()


def del_task():
    w_2 = tk.Toplevel()
    w_2.title("刪除學生資料")
    w_2.geometry("420x400")
    w_2.config(bg="#B3D9D9")

    # === Label 與輸入框 ===
    tk.Label(w_2, text="選擇學生：", bg="#B3D9D9").grid(row=0, column=0, padx=10, pady=5)
    tk.Label(w_2, text="選擇日期：", bg="#B3D9D9").grid(row=1, column=0, padx=10, pady=5)
    tk.Label(w_2, text="選擇時間：", bg="#B3D9D9").grid(row=2, column=0, padx=10, pady=5)
    tk.Label(w_2, text="選擇課程：", bg="#B3D9D9").grid(row=3, column=0, padx=10, pady=5)

    d_name = tk.StringVar()
    d_date = tk.StringVar()
    d_time = tk.StringVar()
    d_course = tk.StringVar()

    combo_name = ttk.Combobox(w_2, textvariable=d_name, state="readonly", width=20)
    combo_date = ttk.Combobox(w_2, textvariable=d_date, state="readonly", width=20)
    combo_time = ttk.Combobox(w_2, textvariable=d_time, state="readonly", width=20)
    combo_course = ttk.Combobox(w_2, textvariable=d_course, state="readonly", width=20)

    combo_name.grid(row=0, column=1)
    combo_date.grid(row=1, column=1)
    combo_time.grid(row=2, column=1)
    combo_course.grid(row=3, column=1)

    # === Tree5 顯示資料 ===
    columns = ("name", "date", "time", "課程")
    tree5 = ttk.Treeview(w_2, columns=columns, show="headings", height=8)
    for col in columns:
        tree5.heading(col, text=col)
        tree5.column(col, width=100, anchor="center")
    tree5.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    # === 載入學生名單 ===
    conn = s.connect('./點名系統.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT name FROM student")
    combo_name["values"] = [row[0] for row in c.fetchall()]
    conn.close()

    # === 事件綁定 ===
    combo_name.bind("<<ComboboxSelected>>", lambda e: update_dates())
    combo_date.bind("<<ComboboxSelected>>", lambda e: update_times())
    combo_time.bind("<<ComboboxSelected>>", lambda e: update_courses())

    # === 更新下拉選單 ===
    def update_dates():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT date FROM student WHERE name=?", (d_name.get(),))
        combo_date["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_date.set(""); combo_time.set(""); combo_course.set("")

    def update_times():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT time FROM student WHERE name=? AND date=?", (d_name.get(), d_date.get()))
        combo_time["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_time.set(""); combo_course.set("")

    def update_courses():
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("SELECT DISTINCT 課程 FROM student WHERE name=? AND date=? AND time=?", 
                  (d_name.get(), d_date.get(), d_time.get()))
        combo_course["values"] = [row[0] for row in c.fetchall()]
        conn.close()
        combo_course.set("")

    # === 查詢按鈕 ===
    def query_data():
        tree5.delete(*tree5.get_children())
        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        sql = "SELECT * FROM student WHERE 1=1"
        params = []
        if d_name.get():
            sql += " AND name=?"; params.append(d_name.get())
        if d_date.get():
            sql += " AND date=?"; params.append(d_date.get())
        if d_time.get():
            sql += " AND time=?"; params.append(d_time.get())
        if d_course.get():
            sql += " AND 課程=?"; params.append(d_course.get())
        for rec in c.execute(sql, params):
            tree5.insert("", "end", values=rec)
        conn.close()

    tk.Button(w_2, text="查詢資料", command=query_data).grid(row=4, column=0, pady=10)

    # === 刪除按鈕 ===
    def delete_selected():
        if not (d_name.get() and d_date.get() and d_time.get() and d_course.get()):
            messagebox.showwarning("警告", "請完整選擇學生、日期、時間與課程！")
            return

        confirm = messagebox.askyesno("確認刪除", "確定要刪除這筆資料嗎？")
        if not confirm:
            return

        conn = s.connect('./點名系統.db')
        c = conn.cursor()
        c.execute("DELETE FROM student WHERE name=? AND date=? AND time=? AND 課程=?",
                  (d_name.get(), d_date.get(), d_time.get(), d_course.get()))
        conn.commit()
        conn.close()

        messagebox.showinfo("完成", "資料已刪除。")
        query_data()  # 重新刷新列表

    tk.Button(w_2, text="刪除選取資料", command=delete_selected, bg="red", fg="white").grid(row=4, column=1, pady=10)


def in_task(): #編號、日期、名稱、完成度、重要度、角色
    global name,combobox,combobox1,combobox2    
    w_1=tk.Toplevel()                                                      
    w_1.title('新增功能')
    w_1.geometry("700x50")
    w_1.config(bg='#B3D9D9')

    name=tk.StringVar()
    tk.Label(w_1, text='名字',font='12',bg='#B3D9D9').place(x=170,y=10)
    tk.Label(w_1, text='日期',font='12',bg='#B3D9D9').place(x=10,y=10)
    tk.Label(w_1, text='課程',font='12',bg='#B3D9D9').place(x=500,y=10)
    tk.Label(w_1, text="time",font='12',bg='#B3D9D9').place(x=320,y=10)
    tk.Entry(w_1, width=10, textvariable=name).place(x=230, y=13)
    values=["週一","週二","週三","週四","週五","週六","週日"]
    combobox=ttk.Combobox(w_1,values=values,width=10)
    combobox.place(x=60,y=13)
    combobox.set("週一") 
    TT = [
    "1:00","1:30","2:00","2:30","3:00","3:30","4:00","4:30",
    "5:00","5:30","6:00","6:30","7:00","7:30","8:00","8:30",
    "9:00","9:30","10:00","10:30","11:00","11:30","12:00","12:30",
    "13:00","13:30","14:00","14:30","15:00","15:30","16:00","16:30",
    "17:00","17:30","18:00","18:30","19:00","19:30","20:00","20:30",
    "21:00","21:30","22:00","22:30","23:00","23:30","24:00"

    ]
    combobox1=ttk.Combobox(w_1,values=TT,width=10)
    combobox1.place(x=380,y=13)
    combobox1.set("6:00") 
    class_ = [
    "電吉他","木吉他","電貝斯","鋼琴","爵士鼓"
    ]
    combobox2=ttk.Combobox(w_1,values=class_,width=10)
    combobox2.place(x=550,y=13)
    combobox2.set("電吉他") 

    tk.Button(w_1,text ='新增', command=insert_task).place(x=650,y=10)    
    w_1.mainloop()
def insert_task():
    name_ = name.get()
    class__ = combobox2.get()
    time_ = combobox1.get()
    date = combobox.get()
    ans=msgbox.askokcancel('資料新增','確定寫入資料',icon='info')
    if ans==True:
        conn=s.connect('./點名系統.db')#建立資料庫連線
        x=(name_,date,time_,class__)#tuple
        #sql='insert into task (日期,名稱,完成度,重要度) values(?,?,?,?)' #新增語法
        sql='insert into student(name,date,time,課程) values(?,?,?,?)' 
        conn.execute(sql,x)
        conn.commit()#新增、刪除、修改，查詢不用
        conn.close()
        msgbox.showinfo('訊息','新增成功!')        
win = tk.Tk()
win.title("點名系統")
win.geometry('500x150')
win.config(bg='#A9A9A9')
text_label = tk.Label(
    win,
    text="歡迎使用點名系統！\n請從上方選單中選擇功能。",
    font=("Arial", 30),
    bg="#FFFFFF",
    fg="black",
    justify="center"
)
text_label.place(x=10, y=40)
menu = tk.Menu(win)
win.config(menu=menu)
simu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="新增學生", menu=simu_menu)
simu_menu.add_command(label="輸入學生", command=in_task)
aimu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="刪除", menu=aimu_menu)
aimu_menu.add_command(label="刪除學生資料", command=del_task)
aimu_menu.add_command(label="刪除點名資料", command=delete_attendance_data)
bimu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="上課表", menu=bimu_menu)
bimu_menu.add_command(label="上課表", command=whatclass)
cimu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="點名", menu=cimu_menu)
cimu_menu.add_command(label="點名", command=fi_query_task)
dimu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="出席率", menu=dimu_menu)
dimu_menu.add_command(label="出席率", command=show_attendance_window)
eimu_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="關閉視窗", menu=eimu_menu)
eimu_menu.add_command(label="結束", command=win.destroy)
win.mainloop()


# In[99]:




# In[ ]:




