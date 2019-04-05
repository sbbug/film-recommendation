#以下是最常用的读取视频流的方法
import cv2
url = 'rtsp://admin:password@192.168.1.104:554/11'
cap = cv2.VideoCapture(url)


if __name__ =="__main__":

    while(cap.isOpened()):

        ret,frame = cap.read()
        if ret == False:
            break
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


