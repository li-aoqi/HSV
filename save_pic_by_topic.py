#!/usr/bin/env python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
from pynput import keyboard


class ImageSaverNode:
    def __init__(self):
        rospy.init_node('image_saver_node', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber('/prometheus/sensor/monocular_front/image_raw', Image, self.image_callback)
        self.image = None
        self.save_count = 0
        self.keyboard_listener = keyboard.Listener(on_release=self.on_key_release)
        self.keyboard_listener.start()
        # self.timer = rospy.Timer(rospy.Duration(0.1), self.display_image)  # Use a rospy.Timer for display

    def image_callback(self, msg):
        try:
            self.image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')  # Convert ROS Image message to OpenCV image
        except CvBridgeError as e:
            rospy.logerr(e)

    def display_image(self, event):
        if self.image is not None:
            cv2.imshow('Image', self.image)
            cv2.waitKey(1)

    def save_image(self):
        # print("11111111111111")
        if self.image is not None:
            # Define the directory to save images
            save_dir = 'save_img/'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)

            # Generate a unique file name
            filename = os.path.join(save_dir, f'image_{self.save_count}.png')

            # Save the image
            cv2.imwrite(filename, self.image)
            rospy.loginfo(f'Saved image as {filename}')
            self.save_count += 1

    def on_key_release(self, key):
        if key == keyboard.Key.esc:
            # 退出程序
            rospy.signal_shutdown("Keyboard exit")
        elif key == keyboard.KeyCode.from_char('s'):
            # 按下's'键触发保存图像操作
            self.save_image()

if __name__ == '__main__':
    try:
        node = ImageSaverNode()
        rate = rospy.Rate(10)  # 调整循环频率
        while not rospy.is_shutdown():
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
