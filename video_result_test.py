import cv2

color_range = {     
    'test0':[(0 , 155 , 205), (2 , 255 , 232)],
    'test1':[(174 , 155 , 195), (180 , 255 , 245)]
                }

cap = cv2.VideoCapture("input.avi")
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用XVID编解码器
out = cv2.VideoWriter('output.avi', fourcc, 10, (frame_width, frame_height), isColor=False)

while True:
    ret, frame = cap.read()

    if frame is not None:

        hsvimg = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame_red0 = cv2.inRange(hsvimg, color_range['test0'][0],color_range['test0'][1])  # 对原图像和掩模(颜色的字典)进行位运算
        frame_red1 = cv2.inRange(hsvimg, color_range['test1'][0],color_range['test1'][1]) 
        frame_red_final=frame_red0+frame_red1

        out.write(frame_red_final)

        cv2.imshow("Video", frame)
        cv2.imshow("Video1", frame_red_final)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()