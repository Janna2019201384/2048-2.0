import turtle
import random
boundary = turtle.Screen()
#创建一个画布（宽、高、位置）
boundary.setup(430, 630, 500, 10)
boundary.bgcolor('pink')
boundary.title('2048')
boundary.register_shape('2.gif')
boundary.register_shape('4.gif')
boundary.register_shape('8.gif')
boundary.register_shape('16.gif')
boundary.register_shape('32.gif')
boundary.register_shape('64.gif')
boundary.register_shape('128.gif')
boundary.register_shape('256.gif')
boundary.register_shape('512.gif')
boundary.register_shape('1024.gif')
boundary.register_shape('2048.gif')
boundary.register_shape('4096.gif')
boundary.register_shape('8192.gif')
boundary.register_shape('bg.gif')
boundary.register_shape('title.gif')
boundary.register_shape('score.gif')
boundary.register_shape('top_score.gif')
boundary.tracer(0)


#创建游戏窗口
class Background(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
#画标题和分割线
    def show_text(self):
        self.color('white', 'white')
        self.goto(-215, 120)#画笔起点
        self.begin_fill()
        self.pd()#移动时绘制图形
        self.goto(215, 120)
        self.goto(215, 110)
        self.goto(-215, 110)
        self.end_fill()
        self.pu()#提起笔移动，不绘制图形，用于另起一个地方绘制
        self.shape('title.gif')
        self.goto(-125, 210)
        self.stamp()
        self.shape('score.gif')
        self.goto(125, 245)
        self.stamp()
        self.shape('top_score.gif')
        self.goto(125, 170)
        self.stamp()
#画16个格子
    def show_back(self):
        for i in allpos:
            self.shape('bg.gif')
            self.goto(i)#将画笔移动到坐标为x,y的位置
            self.stamp()#盖章复制16个格子


#显示分数
    def show_score(self, score):
        self.color('white')
        self.goto(125, 210)
        self.clear()
        #先清除上一次的分数，再写新的分数
        self.write(f'{score}', align='center', font=("Arial", 30, "bold"))

    def show_top_score(self, top_score):
        self.color('white')
        self.goto(125, 138)
        self.clear()
        self.write(f'{top_score}', align='center', font=("Arial", 30, "bold"))

        
#随机出现一个2/4数字块
class Block(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()

    def grow(self):
        #2出现的几率是4的4倍
        num = random.choice([2,2,2,2,4])
        self.shape(f'{num}.gif')
        #16个格子随机一个位置
        a = random.choice(allpos)
        self.goto(a)
        allpos.remove(a)
        block_list.append(self)
        boundary.update()
        
        
#数字块的移动
#self.g0(a,b,c,px,py，true/false)
    def go_down(self):
        self.go(-150, -50, 50, 0, -100, True)

    def go_up(self):
        self.go(-50, -150, -250, 0, 100, True)

    def go_left(self):
        self.go(-50, 50, 150, -100, 0, False)

    def go_right(self):
        self.go(50, -50, -150, 100, 0, False)

    def go(self, b1, b2, b3, px, py, c):
        global move_time, z_bool
        #每一次调用move_time都要清零
        move_time = 0
        block_1, block_2, block_3 = [], [], []
        for i in block_list:
            if c is True:
                if i.ycor() == b1:
                    block_1.append(i)
                elif i.ycor() == b2:
                    block_2.append(i)
                elif i.ycor() == b3:
                    block_3.append(i)
            else:
                if i.xcor() == b1:
                    block_1.append(i)
                elif i.xcor() == b2:
                    block_2.append(i)
                elif i.xcor() == b3:
                    block_3.append(i)
        for j in block_1:
            j.move(j.xcor()+px, j.ycor()+py)
        for j in block_2:
            for k in range(2):
                j.move(j.xcor()+px, j.ycor()+py)
        for j in block_3:
            for k in range(3):
                j.move(j.xcor()+px, j.ycor()+py)
                
        #出现一个新的数字块
        if move_time != 0:
            block = Block()
            block.grow()
        bc_score.show_score(score)
        bc_top_score.show_top_score(top_score)
        
        #判断输赢。加个测试，出现8，就显示达成2048
        for k in block_list:
            if k.shape() == '2048.gif' and z_bool:
                #z—bool控制提示只出现一次
                win_lose.show_text('达成2048，继续请按回车键')
                z_bool = False
        #判断输
        if judge() is False:
            win_lose.show_text('游戏结束，重新开始请按空格键')

#如果有移动，movetime加一
    def move(self, gox, goy):
        global move_time, score, z, top_score
        if (gox, goy) in allpos:
            allpos.append(self.pos())
            self.goto(gox, goy)
            allpos.remove((gox, goy))
            move_time += 1
            
        #相同数字相加
        else:
            for i in block_list:
                if i.pos() == (gox, goy) and i.shape() == self.shape():
                    allpos.append(self.pos())
                    self.goto(gox, goy)
                    self.ht()#隐藏起来
                    block_list.remove(self)
                    #切掉.gif，取数字
                    z = int(i.shape()[0:-4])
                    i.shape(f'{z*2}.gif')
                    move_time += 1
                    score = score + z*2
                else:
                    continue
        if score > top_score:
            top_score = score
            


#显示输赢文字提示
class WinLose(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.ht()#要把海龟隐藏起来
        self.color('blue')

    def show_text(self, text):
        self.write(f'{text}', align='center', font=("黑体", 20, "bold"))

#没有空格子，且上下左右没有相同的，即判断失败
def judge():
    judge_a = 0
    if allpos == []:
        for i in block_list:
            for j in block_list:
                if i.shape() == j.shape() and i.distance(j) == 100:
                    judge_a += 1
        if judge_a == 0:
            return False
        else:
            return True
    else:
        return True


#游戏重新开始
def init():
    global z, z_bool, score, block_list, allpos
    #全局变量还原
    z = 0
    z_bool = True
    score = 0
    allpos = [(-150, 50), (-50, 50), (50, 50), (150, 50),
              (-150, -50), (-50, -50), (50, -50), (150, -50),
              (-150, -150), (-50, -150), (50, -150), (150, -150),
              (-150, -250), (-50, -250), (50, -250), (150, -250)]
    for i in block_list:
        i.clear()
        i.ht()
    win_lose.clear()
    block_list = []
    block = Block()
    block.grow()


z = 0
z_bool = True
score = 0
top_score = 0
block_list = []
#划分4*4=16个格子
allpos = [(-150, 50), (-50, 50), (50, 50), (150, 50),
          (-150, -50), (-50, -50), (50, -50), (150, -50),
          (-150, -150), (-50, -150), (50, -150), (150, -150),
          (-150, -250), (-50, -250), (50, -250), (150, -250)]
bc_title = Background()

#显示分数
bc_score = Background()
bc_top_score = Background()
bc_title.show_text()
bc_title.show_back()
bc_score.ht()
bc_top_score.ht()
bc_score.show_score(score)
bc_top_score.show_top_score(top_score)
block = Block()
block.grow()
move_time = 0
win_lose = WinLose()

boundary.listen()
boundary.onkey(block.go_right, 'Right')
boundary.onkey(block.go_left, 'Left')
boundary.onkey(block.go_up, 'Up')
boundary.onkey(block.go_down, 'Down')
boundary.onkey(win_lose.clear, 'Return')
boundary.onkey(init, 'space')

boundary.mainloop()
