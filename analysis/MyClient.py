from tkinter import *
from tkinter import messagebox
import webbrowser
import sys
import MySpider
import grid

all = []  # all保存评论文本的列表设置为全局变量
page = 1  # i为爬取的评论的页数
file_id = ""


def Register_check(u1, u2):  # 检查用户登录信息函数
    if u1 == '123' and u2 == '123':
        messagebox.showinfo("登录", "用户名与密码匹配")
        root1.quit()
        root1.withdraw()
    else:
        messagebox.showerror("登录", "用户名与密码不匹配，请重试")


def Register():  # 登录界面
    global root1  # 将登录界面设置为全局变量以便在检查用户信息后退出
    root1 = Tk()

    root1.title('情感分析系统')
    # root1.geometry('300x200')

    group = LabelFrame(root1, text="用户登录界面", padx=5, pady=5)
    group.grid(row=0, column=0, padx=10, pady=5, rowspan=2, columnspan=2)
    Label(group, text="用户：").grid(row=0, column=0, padx=10, pady=5)
    Label(group, text="密码：").grid(row=1, column=0, padx=10, pady=5)

    v1 = StringVar()
    v2 = StringVar()

    e1 = Entry(group, textvariable=v1)  # 输入框
    e2 = Entry(group, textvariable=v2, show="*")
    e1.grid(row=0, column=1, padx=10, pady=5)
    e2.grid(row=1, column=1, padx=10, pady=5)

    Button(root1, text="退出", width=10, command=lambda: sys.exit(0)).grid(row=2, column=0, sticky=W, padx=10, pady=5)
    Button(root1, text="登录", width=10, command=lambda: Register_check(v1.get(), v2.get())).grid(row=2, column=1,
                                                                                                sticky=E, padx=10,
                                                                                                pady=5)

    mainloop()


def main():  # 主菜单
    root2 = Tk()

    root2.title('情感分析系统')
    root2.geometry('1200x700')

    def Select_name():  # 输入电影名菜单
        top = Toplevel()
        top.title("情感分析系统")

        Label(top, text="请输入电影名").grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        v = StringVar()
        e = Entry(top, textvariable=v)
        e.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        def Select_name_delete():  # 输入电影名界面的撤销按钮绑定函数
            e.delete(0, END)

        def Select_name_comfirm():  # 输入电影名界面的确定按钮绑定函数
            film_name = v.get()
            global flag
            flag = 0
            global film_id
            film_id = MySpider.Select(str(film_name))  # 通过Select函数获取电影名对应id
            film_url = (
                        "https://movie.douban.com/subject/%s/comments?start=0&limit=20&sort=new_score&status=P" % film_id)
            global all
            all = []
            all.extend(MySpider.Get_Comment(film_url))
            MySpider.Save_Comment(all)

            top.withdraw()
            messagebox.showinfo("情感分析系统", "爬取成功")
            t.delete("1.0",END)
            t.insert(INSERT, film_url)
            t.tag_add("link", "1.0", END)
            t.tag_config("link", foreground="blue", underline=True)

        Button(top, text="撤销", width=10, command=Select_name_delete).grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(top, text="确定", width=10, command=Select_name_comfirm).grid(row=2, column=1, sticky=E, padx=10, pady=5)

    Button(root2, text="爬取电影评论", width=10, command=Select_name).grid(row=0, column=0, sticky=W, ipadx=40, ipady=20)

    def Select_book_name():  # 输入书名菜单
        top = Toplevel()
        top.title("情感分析系统")

        Label(top, text="请输入书名").grid(row=0, column=0, padx=10, pady=5, columnspan=2)

        v = StringVar()
        e = Entry(top, textvariable=v)
        e.grid(row=1, column=0, padx=10, pady=5, columnspan=2)

        def Select_name_delete():  # 输入电影名界面的撤销按钮绑定函数
            e.delete(0, END)

        def Select_name_comfirm():  # 输入电影名界面的确定按钮绑定函数
            book_name = v.get()
            global flag
            flag = 1
            global book_id
            book_id = MySpider.Select_book(str(book_name))  # 通过Select函数获取电影名对应id
            book_url = (
                        "https://book.douban.com/subject/%s/comments?start=0&limit=20&sort=new_score&status=P" % book_id)

            all = []
            all.extend(MySpider.Get_Comment(book_url))
            MySpider.Save_Comment(all)

            top.withdraw()
            messagebox.showinfo("情感分析系统", "爬取成功")
            t.delete("1.0", END)
            t.insert(INSERT, book_url)
            t.tag_add("link", "1.0", END)
            t.tag_config("link", foreground="blue", underline=True)

        Button(top, text="撤销", width=10, command=Select_name_delete).grid(row=2, column=0, sticky=W, padx=10, pady=5)
        Button(top, text="确定", width=10, command=Select_name_comfirm).grid(row=2, column=1, sticky=E, padx=10, pady=5)

    Button(root2, text="爬取图书评论", width=10, command=Select_book_name).grid(row=1, column=0, sticky=W, ipadx=40, ipady=20)
    def Add_comment():  # 增加评论按钮函数
        top = Toplevel()
        top.geometry('300x150')
        top.title("情感分析系统")

        label = Label(top, text="请选择要增加的评论页数")
        label.pack(side='top', fill='x', padx=10, pady=15)

        w = Spinbox(top, from_=0, to=5)
        w.pack(padx=10, pady=15)

        def Add_comment_comfirm():  # 增加评论按钮函数的确定按钮函数
            num = w.get()
            global page
            page = page + int(num)
            global all
            all = []
            for number in range(0, page):
                if flag == 0:
                    all.extend(MySpider.Get_Comment(
                        "https://movie.douban.com/subject/%s/comments?start=%d&limit=20&sort=new_score&status=P" % (
                            film_id, (number * 20))))
                if flag == 1:
                    all.extend(MySpider.Get_Comment(
                        "https://book.douban.com/subject/%s/comments?start=%d&limit=20&sort=new_score&status=P" % (
                            book_id, (number * 20))))
            MySpider.Save_Comment(all)
            top.withdraw()
            messagebox.showinfo("情感分析系统", "增加评论成功")

        b1 = Button(top, text="确定", width=10, command=Add_comment_comfirm)
        b1.pack(side='bottom', padx=10, pady=5)

    Button(root2, text="增加评论", width=10, command=Add_comment).grid(row=2, column=0, sticky=W, ipadx=40, ipady=20)

    def Delete_comment():  # 删除评论按钮函数
        top = Toplevel()
        top.geometry('300x150')
        top.title("情感分析系统")

        label = Label(top, text="请选择要删除的评论页数")
        label.pack(side='top', fill='x', padx=10, pady=15)

        global page
        w = Spinbox(top, from_=0, to=page)
        w.pack(padx=10, pady=15)

        def Delete_comment_comfirm():  # 删除评论按钮函数的确定按钮函数
            num = w.get()
            global page
            page = page - int(num)

            global all
            all = []
            for number in range(0, page):
                if flag == 0:
                    all.extend(MySpider.Get_Comment(
                        "https://movie.douban.com/subject/%s/comments?start=%d&limit=20&sort=new_score&status=P" % (
                            film_id, (number * 20))))
                if flag == 1:
                    all.extend(MySpider.Get_Comment(
                        "https://book.douban.com/subject/%s/comments?start=%d&limit=20&sort=new_score&status=P" % (
                            book_id, (number * 20))))
            MySpider.Save_Comment(all)
            top.withdraw()
            messagebox.showinfo("情感分析系统", "删除评论成功")

        b1 = Button(top, text="确定", width=10, command=Delete_comment_comfirm)
        b1.pack(side='bottom', padx=10, pady=5)

    Button(root2, text="删除评论", width=10, command=Delete_comment).grid(row=3, column=0, sticky=W, ipadx=40, ipady=20)

    def Show_comment():
        text.delete("1.0", END)
        with open("Comment.txt", 'r', encoding='utf-8') as f1:
            sentence = f1.readlines()
            for s in sentence:
                text.insert(END, s)

    Button(root2, text="显示评论文本", width=10, command=Show_comment).grid(row=4, column=0, sticky=W, ipadx=40, ipady=20)

    def Analyse_comment():
        text.delete(1.0, END)
        MySpider.Analyse("Comment.txt")
        with open("Analyse.txt", 'r', encoding='utf-8') as f1:
            sentence = f1.readlines()
            for s in sentence:
                text.insert(END, s)
        messagebox.showinfo("情感分析系统", "分析结束")



    def Polarity():
        MySpider.show_polarity()

    Button(root2, text="显示总体极性", width=10, command=Polarity).grid(row=6, column=0, sticky=W, ipadx=40, ipady=20)

    def Scatter():
        MySpider.show_scatter()

    Button(root2, text="生成散点图", width=10, command=Scatter).grid(row=7, column=0, sticky=W, ipadx=40, ipady=20)

    def Wordcloud():
        MySpider.show_wordcloud()

    Button(root2, text="生成词云图", width=10, command=Wordcloud).grid(row=8, column=0, sticky=W, ipadx=40, ipady=20)

    def Bar_chart():
        MySpider.show_bar_chart()

    Button(root2, text="生成柱状图", width=10, command=Bar_chart).grid(row=9, column=0, sticky=W, ipadx=40, ipady=20)

    # def Scatter1():
    # MySpider.relation()

    # Button(root2, text="生成关系图", width=10, command=Scatter1).grid(row=9, column=0, sticky=W, ipadx=40, ipady=20)

    def click(event):  # 点击目标字段打开url函数
        url1 = t.get("1.0", END)
        webbrowser.open(url1)

    def show_hand_cursor(event):  # 进入目标字段显示图形函数
        t.config(cursor="arrow")

    def show_arrow_cursor(event):  # 离开目标字段显示图形函数
        t.config(cursor="xterm")

    Button(root2, text="情感分析", width=10, command=Analyse_comment).grid(row=5, column=0, sticky=W, ipadx=40, ipady=20)

    Button(root2, text="退出", width=10, command=root2.quit).place(relx=0.5, rely=0.93)

    Label(root2, text="目标URL：").grid(row=0, column=1, sticky=W, ipadx=40, ipady=20)

    t = Text(root2, width=110, height=1)  # 显示目标电影短评url的网站
    t.grid(row=0, column=2, ipadx=40, ipady=20, columnspan=5, padx=10, pady=5)
    t.tag_bind("link", "<Enter>", show_hand_cursor)  # 鼠标进入目标字段事件
    t.tag_bind("link", "<Leave>", show_arrow_cursor)  # 鼠标离开目标字段事件
    t.tag_bind("link", "<Button-1>", click)  # 鼠标点击目标字段事件

    l1 = Label(root2, text="目标的短评：")
    l1.grid(row=1, column=1, ipadx=40, ipady=20, columnspan=6)

    text = Text(root2, width=140, height=37)
    text.grid(row=2, column=1, rowspan=120, columnspan=6, padx=10)

    mainloop()


Register()
main()
