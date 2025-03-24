import pygame#构建图形界面
from pygame.locals import*
import serial#处理串口通信
import serial.tools.list_ports
#你可以使用该句检查可用的串口号，在此程序中并未使用到
#ports_list=list(serial.tools.list_ports.comports())


def pygame_test():
    #设置方框、字体大小颜色

    pygame.init()#初始化pygame
    #创建距离显示框
    myrect=pygame.Rect(300,150,400,70)
    myrect_color=(255,255,255)
    myrect_font=pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'],50)
    myrect_text_color=(0,0,0)
    myrect_text=myrect_font.render("distance=",True,myrect_text_color)
    #创建主窗口
    SCreen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("超声测距")
    #创建按钮
    x,y=100,70
    width,height=250,50
    button_rect=pygame.Rect(x,y,width,height)
    button_color=(255,255,255)
    text_color=(0,0,0)
    button_font= pygame.font.SysFont(['方正粗黑宋简体','microsoftsansserif'],50)
    button_text=button_font.render("start",True,text_color)

    running=True
    while running:

        SCreen.fill((0,0,0))#清空屏幕
        #绘制按钮以及信息框
        pygame.draw.rect(SCreen,button_color,button_rect)
        pygame.draw.rect(SCreen,myrect_color,myrect)
        #文字居中显示
        SCreen.blit(button_text,(button_rect.centerx-button_text.get_width()/2,button_rect.centery-button_text.get_height()/2))
        SCreen.blit(myrect_text,(myrect.centerx-myrect_text.get_width()/2,myrect.centery-myrect_text.get_height()/2))
        for event in pygame.event.get():#持续刷新界面
            
            if event.type == QUIT:#处理窗口关闭事件（点击×号退出）
                running=False

            #如果检测到鼠标点击
            if event.type == MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):#如果点击到button位置

                    reading=True
                    #打开串口，这里的串口设置需要根据你使用的的串口以及配置来进行改变
                    ser=serial.Serial(port="COM15",baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=None)
                    if ser.isOpen():
                        print("串口打开成功")
                    else:
                        print("串口打开失败")
                    receive_buffer=b''
                    while reading:#循环读取串口数据
                        com_input=ser.read()
                        if com_input:
                            receive_buffer+=com_input
                            if receive_buffer.endswith(b'\r\n'):#检测到结束符，这里的结束符是在Keil中设置的
                                line=receive_buffer[:-2]#去除结尾符
                                myrect_text=myrect_font.render(line.decode('utf-8'),True,myrect_text_color)#更新显示内容
                                print(line.decode('utf-8'))
                                receive_buffer=b''
                                reading=False#当采集完一次时，将reading赋值为False，不再循环            
                                ser.close()#关闭串口
                                
        pygame.display.flip()#更新

pygame_test()


            
