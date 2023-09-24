""" 图片鼠标取值HSV value  camera输出显示 """

import numpy as np
import copy as cp
import cv2 
import math
import time

import matplotlib.pyplot as plt
import seaborn as sns

photo_path='1.png'
picture_test = cv2.imread(photo_path)
img  = picture_test.copy()

########################################################################
max_record = [0,0,0]
min_record = [255,255,255]
plt_h = []
plt_s = []
plt_v = []
##########################################################################
color_range = {     
    'yellow_door': [(30 , 190 , 71), (35 , 255 , 103)],
    #'yellow_door': [(16 , 100 , 72), (29 , 226 , 185)],
    'black_door':[(25, 25, 10), (110, 150, 24)],

    'green_hole_chest':[(63 , 87 , 87), (73 , 250 , 177)],
    'green_hole_head':[(55 , 113 , 70), (75 , 241 , 144)],
    'blue_hole_chest':[(104 , 129 , 133), (113 , 227 , 225)],
    'blue_hole_head':[(106 , 113 , 102), (115 , 234 , 191)],
    

    'blue_baf':[(100 , 127 , 52), (112 , 245 , 170)],
    'black_dir':[(0, 0, 10), (170 , 180 , 59)],
    'gray_white':[(54 , 31 , 79), (80 , 90 , 166)],

    'blue_floor':[(104 , 142 , 73), (125 , 249 , 255)],
    'green_floor':[(61 , 99 , 72), (80 , 255 , 185)],
    'red_floor1':[(0 , 112 , 130), (14 , 207 , 245)],
    'red_floor2':[(173 , 145 , 139), (179 , 229 , 252)],
    'red_XP1':[(0 , 141 , 114), (4 , 250 , 254)],
    'red_XP2':[(177 , 182 , 139), (179 , 229 , 225)],

    'color11':[(104 , 141 , 154), (109 , 211 , 231)],
    'color22':[(63 , 73 , 88), (83 , 174 , 197)],
    'color33':[(0 , 86 , 135), (10 , 163 , 242)],

    'ball_red1':[(0 , 129 , 104), (5 , 234 , 193)],
    'ball_red2':[(177 , 75 , 122), (179 , 184 , 151)],
    'd_red_ball_floor1':[(171 , 71 , 113), (179 , 212 , 215)],
    'd_red_ball_floor2':[(0 , 91 , 123), (4 , 204 , 224)],
    'ball_red':[(30 , 3, 143), (173 , 44 , 237)],
    'blue_hole':[(109 , 35 , 94), (149 , 105 , 141)],
    'head_blue_door':[(93 , 95 , 62), (113 , 222 , 197)],
    'green_bridge':[(57 , 85 , 112), (81 , 237 , 228)],
    'blue_bridge':[(101 , 112 , 126), (111 , 216 , 251)],
    
    'green_bridge_rec':[(62 , 85 , 112), (74 , 201 , 228)],
    'blue_bridge_rec':[(101 , 112 , 126), (111 , 216 , 251)],
    'kick_ball_rec':[(4 , 38 , 49), (34 , 132 , 157)],
    'gray_dir':[(71 , 17 , 111), (85 , 41 , 143)],


    'black_line':[(60 , 23 , 25), (122 , 124 , 100)],
    'yellow_line':[(29 , 118 , 90), (38 , 209 , 187)],


    
    'test0':[(0 , 155 , 216), (1 , 177 , 232)],
    'test1':[(179 , 155 , 216), (180 , 177 , 232)],
    'test2':[(179 , 155 , 216), (180 , 177 , 232)]
                }


# 新建窗口
cv2.namedWindow("OriginalImg",cv2.WINDOW_NORMAL)
cv2.namedWindow("IMG_HSV",cv2.WINDOW_NORMAL)
cv2.namedWindow("ColorMask",cv2.WINDOW_NORMAL)

cv2.resizeWindow("OriginalImg", 640, 480)
cv2.resizeWindow("IMG_HSV", 640, 480)
cv2.resizeWindow("ColorMask", 640, 480)


def hsv_max(aa,bb):
    cc=[bb[0],bb[1],bb[2]]
    if aa[0] < 160:
        if aa[0]>bb[0]:
            cc[0]=aa[0]
        if aa[1]>bb[1]:
            cc[1]=aa[1]
        if aa[2]>bb[2]:
            cc[2]=aa[2]
    return cc

def hsv_min(aa,bb):
    cc=[bb[0],bb[1],bb[2]]
    if aa[0] <160:
        if aa[0]<bb[0]:
            cc[0]=aa[0]
        if aa[1]<bb[1]:
            cc[1]=aa[1]
        if aa[2]<bb[2]:
            cc[2]=aa[2]
    return cc

def onmouse(event, x, y, flags, param):   #标准鼠标交互函数
    global max_record,min_record
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if event==cv2.EVENT_MOUSEMOVE:      #当鼠标移动时
        if sampling_flag == True:
            xy_hsv = hsvimg[y,x]
            print(x,y,xy_hsv, "正在采集，w停止采集")           #显示鼠标所在像素的数值，注意像素表示方法和坐标位置的不同
            plt_h.append(xy_hsv[0])
            plt_s.append(xy_hsv[1])
            plt_v.append(xy_hsv[2])
            max_record = hsv_max(xy_hsv,max_record)
            min_record = hsv_min(xy_hsv,min_record)
        else:
            print(min_record,"min--停止采集, w 开始采集--max",max_record)
            print("[(" + str(min_record[0]) + " , " + str(min_record[1]) + " , " + str(min_record[2]) + "), (" + str(max_record[0]) + " , " + str(max_record[1]) + " , " + str(max_record[2]) + ")]," )


# 创建鼠标事件的回调函数
cv2.setMouseCallback("OriginalImg", onmouse)
num = 0
sampling_flag = False
while True:
    
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(img)

    #####################红色用这个#####################################################################################
    frame_red0 = cv2.inRange(hsvimg, color_range['test0'][0],color_range['test0'][1])  # 对原图像和掩模(颜色的字典)进行位运算
    frame_red1 = cv2.inRange(hsvimg, color_range['test1'][0],color_range['test1'][1]) 
    frame_rea_final=frame_red0+frame_red1

    cv2.imshow("ColorMask", frame_rea_final)
    cv2.imshow("IMG_HSV",hsvimg)
    cv2.imshow("OriginalImg",img)
    ##################################################################################################################

    #####################其他用这个#####################################################################################
    # frame_other = cv2.inRange(hsvimg, color_range['test2'][0],color_range['test2'][1])  # 对原图像和掩模(颜色的字典)进行位运算

    # cv2.imshow("ColorMask", frame_other)
    # cv2.imshow("IMG_HSV",hsvimg)
    # cv2.imshow("OriginalImg",img)
    ##################################################################################################################


    k = cv2.waitKey(500)
    # 如果按了'q'键，则关闭面板
    if k == ord('q'):
        break
    if k == ord('s'):
        num += 1
        name = 'photo_save' + str(num) + '.bmp'
        print(name)
        cv2.imwrite(name,img) #保存图片
    if k == ord('w'):
        if sampling_flag == True:
            sampling_flag = False
            print("停止采集")

            # 去掉下部分注释可以显示数据分布
            # sns.distplot(plt_h, bins = None, kde = False, hist_kws = {'color':'steelblue'}, label = 'h')
            # sns.distplot(plt_s, bins = None, kde = False, hist_kws = {'color':'purple'}, label = 's')
            # sns.distplot(plt_v, bins = None, kde = False, hist_kws = {'color':'darkgreen'}, label = 'v')
            # plt.title('hsv')
            # plt.legend()
            # plt.show()
            
        else:
            sampling_flag = True
            print("开始采集")




