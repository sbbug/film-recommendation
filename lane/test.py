import cv2
import numpy as np
# cap = cv2.VideoCapture('./data.avi')
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # fps = cap.get(cv2.CAP_PROP_FPS)
# size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
# out = cv2.VideoWriter('res.avi', fourcc,20.0, size)
# while True:
#     ret, frame = cap.read()
#     if (ret == False):
#         break;
#     # 横向翻转
#     #frame = cv2.flip(frame, 1)
#     out.write(frame)
#     # 在图像上显示 Press Q to save and quit
#     cv2.putText(frame,
#                 "Press Q to save and quit",
#                 (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
#                 (0, 255, 0), 2)
#     cv2.imshow('frame', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cap.release()
# out.release()
# cv2.destroyAllWindows()

a = np.array([[1,2,3],[3,4,5],[6,7,8]])
b = np.ones((3,3))
print(a)
print(b)
print(a+b)