import csv
import pickle

import dlib
import numpy as np
import cv2
import os
import shutil
import logging

from database.student_db import StudentDB
from face_recognition.operation import Operation
from database.face_db import FaceDB

cur_dir = os.path.dirname(__file__)

# Dlib 正向人脸检测器 / Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# 要读取人脸图像文件的路径 / Path of cropped faces
path_images_from_camera = cur_dir + "/data/data_faces_from_camera/"

# Dlib 人脸 landmark 特征点检测器 / Get face landmarks
predictor = dlib.shape_predictor(cur_dir + '/data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Dlib Resnet 人脸识别模型，提取 128D 的特征矢量 / Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1(cur_dir + "/data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")


class FaceRegister:
    def __init__(self):
        self.font = cv2.FONT_ITALIC
        self.ss_cnt = 0  # 录入 personX 人脸时图片计数器 / cnt for screen shots
        self.current_frame_faces_cnt = 0  # 录入人脸计数器 / cnt for counting faces in current frame
        self.save_flag = 1  # 之后用来控制是否保存图像的 flag / The flag to control if save

    # 新建保存人脸图像文件和数据 CSV 文件夹 / Mkdir for saving photos and csv
    def _pre_work_mkdir(self):
        # 新建文件夹 / Create folders to save face images and csv
        if os.path.isdir(path_images_from_camera):
            pass
        else:
            os.mkdir(path_images_from_camera)

    # 删除之前存的人脸数据文件夹 / Delete old face folders
    def _pre_work_del_old_face_folders(self):
        # 删除之前存的人脸数据文件夹, 删除 "/data_faces_from_camera/person_x/"...
        folders_rd = os.listdir(path_images_from_camera)
        for i in range(len(folders_rd)):
            shutil.rmtree(path_images_from_camera + folders_rd[i])
        if os.path.isfile("data/features_all.csv"):
            os.remove("data/features_all.csv")

    # 如果有之前录入的人脸, 在之前 person_x 的序号按照 person_x+1 开始录入 / Start from person_x+1
    def _check_existing_faces_cnt(self):
        if os.listdir(path_images_from_camera):
            # 获取已录入的最后一个人脸序号 / Get the order of latest person
            person_list = os.listdir(path_images_from_camera)
            person_num_list = []
            for person in person_list:
                person_num_list.append(int(person.split('_')[-1]))
            self.existing_faces_cnt = max(person_num_list)

        # 如果第一次存储或者没有之前录入的人脸, 按照 person_1 开始录入 / Start from person_1
        else:
            self.existing_faces_cnt = 0

    # 生成的 cv2 window 上面添加说明文字
    def _draw_note(self, img_rd):
        # 添加说明 / Add some notes
        cv2.putText(img_rd, "Registered Face: " + str(self.ss_cnt), (20, 180), self.font, 1, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(img_rd, "Faces: " + str(self.current_frame_faces_cnt), (20, 140), self.font, 1, (0, 255, 0), 1,
                    cv2.LINE_AA)

    # 获取人脸 / Main process of face detection and saving
    def prepare(self):
        # 1. 新建储存人脸图像文件目录 / Create folders to save photos
        self._pre_work_mkdir()
        # 2. 删除 "/data/data_faces_from_camera" 中已有人脸图像文件
        # / Uncomment if want to delete the saved faces and start from person_1
        # if os.path.isdir(self.path_photos_from_camera):
        #     self.pre_work_del_old_face_folders()

        # 3. 检查 "/data/data_faces_from_camera" 中已有人脸文件
        self._check_existing_faces_cnt()

    def record(self, img_rd, op, sid):
        # Get camera video stream
        faces = detector(img_rd, 0)
        current_face_dir = path_images_from_camera + sid
        face_frame = None
        if not os.path.exists(current_face_dir):
            os.makedirs(current_face_dir)
            logging.info("\n%-40s %s", "新建的人脸文件夹 / Create folders:", current_face_dir)

        if len(faces) != 0:
            # 矩形框 / Show the ROI of faces
            for k, d in enumerate(faces):
                # 计算矩形框大小 / Compute the size of rectangle box
                height = (d.bottom() - d.top())
                width = (d.right() - d.left())
                hh = int(height / 2)
                ww = int(width / 2)

                # 6. 判断人脸矩形框是否超出 1400*1200
                if (d.right() + ww) > 1400 or (d.bottom() + hh > 1200) or (d.left() - ww < 0) or (d.top() - hh < 0):
                    cv2.putText(img_rd, "OUT OF RANGE", (20, 300), self.font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    color_rectangle = (0, 0, 255)
                    save_flag = 0
                    if op == Operation.SAVE:
                        logging.warning("请调整位置 / Please adjust your position")
                else:
                    color_rectangle = (255, 255, 255)
                    save_flag = 1

                cv2.rectangle(img_rd,
                              tuple([d.left() - ww, d.top() - hh]),
                              tuple([d.right() + ww, d.bottom() + hh]),
                              color_rectangle, 2)

                # 7. 根据人脸大小生成空的图像
                face_frame = np.zeros((int(height * 2), width * 2, 3), np.uint8)

                # 8. 按下 'save' 保存摄像头中的人脸到本地
                if save_flag and op == Operation.SAVE:
                    self.ss_cnt += 1
                    for ii in range(height * 2):
                        for jj in range(width * 2):
                            face_frame[ii][jj] = img_rd[d.top() - hh + ii][d.left() - ww + jj]
                    cv2.imwrite(current_face_dir + "/" + str(sid) + "_face_" + str(self.ss_cnt) + ".jpg", face_frame)
                    logging.info("%-40s %s/%s_face_%s.jpg", "写入本地 / Save into：",
                                 str(current_face_dir), str(sid), str(self.ss_cnt))

        self.current_frame_faces_cnt = len(faces)
        # 9. 生成的窗口添加说明文字 / Add note on cv2 window
        self._draw_note(img_rd)

        frame = cv2.resize(img_rd, (800, 500))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if face_frame is not None:
            face_frame = cv2.resize(face_frame, (300, 300))
            face_frame = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)
        return frame, face_frame

    # 返回单张图像的 128D 特征 / Return 128D features for single image
    # Input:    path_img           <class 'str'>
    # Output:   face_descriptor    <class 'dlib.vector'>
    def _get_128d_features(self, path_to_face_img):
        img_rd = cv2.imread(path_to_face_img)
        faces = detector(img_rd, 1)

        logging.info("%s %s", "检测到人脸的图像 / Image with faces detected:", path_to_face_img)

        # 因为有可能截下来的人脸再去检测，检测不出来人脸了, 所以要确保是 检测到人脸的人脸图像拿去算特征
        # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
        if len(faces) != 0:
            shape = predictor(img_rd, faces[0])
            face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
        else:
            face_descriptor = 0
            logging.warning("no face")
        return face_descriptor

    # 返回 personX 的 128D 特征均值
    def _get_mean_features(self, path_to_face_dir):
        features = []
        photos_list = os.listdir(path_to_face_dir)
        if photos_list:
            for i in range(len(photos_list)):
                # 调用 return_128d_features() 得到 128D 特征 / Get 128D features for single image of personX
                logging.info("%s %s", "正在读的人脸图像",
                             path_to_face_dir + "/" + photos_list[i])
                features_128d = self._get_128d_features(path_to_face_dir + "/" + photos_list[i])
                # 遇到没有检测出人脸的图片跳过 / Jump if no face detected from image
                if features_128d == 0:
                    i += 1
                else:
                    features.append(features_128d)
        else:
            logging.warning("文件夹内图像文件为空 %s", path_to_face_dir)
        # 计算 128D 特征的均值 / Compute the mean
        # personX 的 N 张图像 x 128D -> 1 x 128D
        if features:
            return np.array(features, dtype=object).mean(axis=0)
        else:
            return np.zeros(128, dtype=object, order='C')

    def face_registered(self, sid):
        face_db = FaceDB()
        r = face_db.select_by_owner(sid)
        face_db.close()
        return r is not None

    # 将人脸特征数据保存到数据库中
    def save_to_database(self, sid, update=False):
        face_db = FaceDB()
        mean_features = self._get_mean_features(path_images_from_camera + sid)
        mean_features_serialized = pickle.dumps(mean_features)
        logging.debug(mean_features_serialized)
        if update:
            face_id = face_db.select_by_owner(sid)[0]
            face_db.update_face(face_id, mean_features_serialized, sid)
        else:
            face_db.insert_face(mean_features_serialized, sid)
        face_db.close()


