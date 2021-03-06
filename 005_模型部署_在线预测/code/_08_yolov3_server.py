# 导入代码文件_06_yolov3.py的类Detector
from _06_yolov3 import Detector
# 导入常用的库
import time
import os
from PIL import Image
# 导入flask库
from flask import Flask, render_template, request, jsonify
# 加载把图片文件转换为字符串的base64库
import base64


# 实例化Flask对象
server = Flask(__name__)
# 设置开启web服务后，如果更新html文件，可以使更新立即生效
server.jinja_env.auto_reload = True
server.config['TEMPLATES_AUTO_RELOAD'] = True
# 实例化检测器对象
detector = Detector(
    weights_h5FilePath='../resources/yolov3/yolov3_weights.h5',
    anchor_txtFilePath='../resources/yolov3/yolov3_anchors.txt',
    category_txtFilePath='../resources/yolov3/coco.names'
    )
    
    
# 根据图片文件路径获取base64编码后内容
def get_imageBase64String(imageFilePath):
    if not os.path.exists(imageFilePath):
        image_base64_string = ''
    else:
        with open(imageFilePath, 'rb') as file:
            image_bytes = file.read()
        image_base64_bytes = base64.b64encode(image_bytes)
        image_base64_string = image_base64_bytes.decode('utf-8')  
    return image_base64_string
    
    
# 网络请求'/'的回调函数
@server.route('/')
def index():
    htmlFileName = '_08_yolov3.html'
    return render_template(htmlFileName)
    
    
# 网络请求'/get_drawedImage'的回调函数
@server.route('/get_drawedImage', methods=['POST']) 
def anyname_you_like():
    startTime = time.time()
    received_file = request.files['input_image']
    imageFileName = received_file.filename
    if received_file:
        # 保存接收的图片到指定文件夹
        received_dirPath = '../resources/received_images'
        if not os.path.isdir(received_dirPath):
            os.makedirs(received_dirPath)
        imageFilePath = os.path.join(received_dirPath, imageFileName)
        received_file.save(imageFilePath)
        print('接收图片文件保存到此路径：%s' % imageFilePath)
        usedTime = time.time() - startTime
        print('接收图片并保存，总共耗时%.2f秒' % usedTime)
        # 对指定图片路径的图片做目标检测，并打印耗时
        image = Image.open(imageFilePath)
        drawed_image = detector.detect_image(image)
        # 把目标检测结果图保存在服务端指定路径，返回指定路径对应的图片经过base64编码后的字符串
        drawed_imageFileName = 'drawed_' + os.path.splitext(imageFileName)[0] + '.jpg'
        drawed_imageFilePath = os.path.join(received_dirPath, drawed_imageFileName)
        drawed_image.save(drawed_imageFilePath)
        image_base64_string = get_imageBase64String(drawed_imageFilePath)
        return jsonify(image_base64_string=image_base64_string)
    

# 主函数
if __name__ == '__main__':
    server.run('127.0.0.1', port=5000)
    