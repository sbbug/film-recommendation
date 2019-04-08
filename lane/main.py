# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 22:16:16 2019

@author: sun
"""

import numpy as np
import cv2

fps = 120
size = (180, 640)

#定义数据源
cap = cv2.VideoCapture('./data.avi')

# #设置视频格式
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # fps = cap.get(cv2.CAP_PROP_FPS)
# #视频尺寸大小
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# out = cv2.VideoWriter('edgesResult.avi', fourcc,20.0, size)


if __name__ == "__main__":

    #保存边缘检测图
    while (cap.isOpened()):

        ret, frame = cap.read()
        # 读到结尾就退出
        if (ret == False):
            break;
        result = frame.copy()

        # 灰度转换
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        # 中值滤波
        # frame = cv2.medianBlur(gray,5)
        # 高斯滤波
        frame = cv2.GaussianBlur(gray, (3, 3), 0)
        # 边缘检测
        edges = cv2.Canny(frame, 50, 200)

       # out.write(edges)
        cv2.imshow("result", edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    #开始检测车道线
    cap = cv2.VideoCapture('./data.avi')
    # 设置视频格式
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # 视频尺寸大小
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter('edgesResult.avi', fourcc, 20.0, size)

    while(cap.isOpened()):

        ret,frame = cap.read()
         # 读到结尾就退出
        if (ret == False):
            break;
        result = frame.copy()

        #灰度转换
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w =  gray.shape
        #中值滤波
        #frame = cv2.medianBlur(gray,5)
        #高斯滤波
        frame = cv2.GaussianBlur(gray, (3, 3), 0)
        #边缘检测
        edges =  cv2.Canny(frame, 50, 200)

        #获取图像mask
        mask = edges[int(h/4):h,0:w]
        # 经验参数
        minLineLength = 100
        maxLineGap = 5
        #检测直线
        lines = cv2.HoughLinesP(mask,1,np.pi/720,5,minLineLength,maxLineGap)
        if (lines is None or len(lines) == 0):
            print("hello")
            break;
        else:
            for line in lines:
                for x1,y1,x2,y2 in line:
                    cv2.line(result,(x1,y1+int(h/4)),(x2,y2+int(h/4)),(0,0,255),6)

        #cv2.imshow("edges",edges)
        # out1.write(edges)

        #往视频上添加文字
        cv2.putText(result,
                    "lane detect result display",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 255, 0), 2)
        out.write(result)
        cv2.imshow("result",result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()