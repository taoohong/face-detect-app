# Copyright (C) 2018-2021 coneypo
# SPDX-License-Identifier: MIT
import os
import pickle

# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera
# Mail:     coneypo@foxmail.com

# 摄像头实时人脸识别 / Real-time face detection and recognition

import dlib
import numpy as np
import cv2
import logging
from PIL import Image, ImageDraw, ImageFont
from database.face_db import FaceDB
from database.student_db import StudentDB

cur_dir = os.path.dirname(__file__)

# Dlib 正向人脸检测器 / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Dlib 人脸 landmark 特征点检测器 / Get face landmarks
predictor = dlib.shape_predictor(cur_dir + '/data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet 人脸识别模型, 提取 128D 的特征矢量 / Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1(cur_dir + "/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


class FaceRecognizer:
    def __init__(self):
        self.frame_cnt = 0
        self.face_feature_known_list = []  # 用来存放所有录入人脸特征的数组 / Save the features of faces in database
        self.face_owner_known_list = []  # 存储录入人脸名字 / Save the name of faces in database

        self.font = cv2.FONT_ITALIC
        self.font_chinese = ImageFont.truetype(cur_dir + "/simsun.ttc", 30)

    # 从数据库读取录入人脸特征
    def get_faces_from_database(self):
        faceDB = FaceDB()
        studentDB = StudentDB()
        faces = faceDB.select_all()
        if len(faces) == 0:
            return 0
        for face_row in faces:
            face = pickle.loads(face_row[1])
            logging.debug("face: %s", face)
            s = studentDB.select_student_by_sid(face_row[2])
            self.face_feature_known_list.append(face)
            self.face_owner_known_list.append(s)
        faceDB.close()
        studentDB.close()
        return 1

    # 计算两个128D向量间的欧式距离 / Compute the e-distance between two 128D features
    @staticmethod
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        return dist

    # 生成的 cv2 window 上面添加说明文字
    def _draw_note(self, img_rd, frame_face_cnt):
        cv2.putText(img_rd, "Face Recognizer", (20, 40), self.font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Frame:  " + str(self.frame_cnt), (20, 100), self.font, 0.8, (0, 255, 0), 1,
                    cv2.LINE_AA)
        cv2.putText(img_rd, "Faces:  " + str(frame_face_cnt), (20, 160), self.font, 0.8, (255, 0, 0), 1,
                    cv2.LINE_AA)

    def _draw_name(self, img_rd, name_list, name_pos_list):
        # 在人脸框下面写人脸名字
        img = Image.fromarray(cv2.cvtColor(img_rd, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        for i in range(len(name_list)):
            draw.text(xy=name_pos_list[i], text=name_list[i], font=self.font_chinese, fill=(0, 0, 0), fontScale=1.5)
            img_rd = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return img_rd

    # 处理获取的视频流，进行人脸识别
    def process(self, img_rd):
        # 1. 读取存放所有人脸特征的 csv / Read known faces from "features.all.csv"
        frame_face_owner_list = []  # 存储当前摄像头中捕获到的人脸所属个体信息
        frame_face_feature_list = []  # 存储当前摄像头中捕获到的人脸特征 / Features of faces in current frame
        frame_face_owner_name_list = []  # 存储当前摄像头中捕获到的所有人脸的名字 / Names of faces in current frame
        frame_face_owner_name_pos_list = []  # 存储当前摄像头中捕获到的所有人脸的名字坐标 / Positions of faces in current frame
        if self.get_faces_from_database():
            self.frame_cnt += 1
            logging.debug("Frame %d starts", self.frame_cnt)
            faces = detector(img_rd, 0)
            # 存储当前摄像头中捕获到的人脸数 / Counter for faces in current frame
            frame_face_cnt = len(faces)
            self._draw_note(img_rd, frame_face_cnt)
            # 2. 检测到人脸 / Face detected in current frame
            if frame_face_cnt:
                frame_face_owner_list = [None] * frame_face_cnt
                frame_face_owner_name_list = ["unknown"] * frame_face_cnt
                # 3. 获取当前捕获到的图像的所有人脸的特征 / Compute the face descriptors for faces in current frame
                for i in range(len(faces)):
                    features = predictor(img_rd, faces[i])
                    frame_face_feature_list.append(face_reco_model.compute_face_descriptor(img_rd, features))
                # 4. 遍历捕获到的图像中所有的人脸 / Traversal all the faces in the database
                for k in range(len(faces)):
                    logging.debug("For face %d in camera:", k + 1)
                    # 每个捕获人脸的名字坐标 / Positions of faces captured
                    frame_face_owner_name_pos_list.append(tuple(
                        [faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 4)]))

                    # 5. 对于某张人脸，遍历所有存储的人脸特征
                    # For every faces detected, compare the faces in the database
                    current_frame_e_distance_list = []
                    for i in range(len(self.face_feature_known_list)):
                        if str(self.face_feature_known_list[i][0]) != '0.0':
                            e_distance_tmp = self.return_euclidean_distance(frame_face_feature_list[k],
                                                                            self.face_feature_known_list[i])
                            logging.debug("  With person %s, the e-distance is %f", str(i + 1), e_distance_tmp)
                            current_frame_e_distance_list.append(e_distance_tmp)
                        else:
                            current_frame_e_distance_list.append(999999999)
                    # 6. 寻找出最小的欧式距离匹配 / Find the one with minimum e-distance
                    similar_person_num = current_frame_e_distance_list.index(min(current_frame_e_distance_list))
                    logging.debug("Minimum e-distance with %s: %f",
                                  self.face_owner_known_list[similar_person_num].name,
                                  min(current_frame_e_distance_list))

                    if min(current_frame_e_distance_list) < 0.4:
                        frame_face_owner_list[k] = self.face_owner_known_list[similar_person_num]
                        frame_face_owner_name_list[k] = frame_face_owner_list[k].name
                        logging.debug("Face recognition result: %s", frame_face_owner_name_list[k])
                    else:
                        logging.debug("Face recognition result: Unknown person")
                    logging.debug("\n")

                    # 矩形框 / Draw rectangle
                    for kk, d in enumerate(faces):
                        # 绘制矩形框
                        cv2.rectangle(img_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]),
                                      (255, 255, 255), 2)
                # 7. 写名字 / Draw name
                img_rd = self._draw_name(img_rd, frame_face_owner_name_list, frame_face_owner_name_pos_list)

        # 8. 返回结果
        frame = cv2.resize(img_rd, (800, 500))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_face_owner_list = [x for x in frame_face_owner_list if x is not None]
        return frame, frame_face_owner_list
