from flask import Flask, request, jsonify
from flask.views import MethodView
from extension import cors
from PIL import Image,ImageDraw
import os
import numpy as np
import json

from GetVertex import GetVertex
from DownsamplingBoundary import DownsamplingBoudary
from DownsamplingArea import DownsampingArea
from Boundary import Boundary
from Triangulation import Triangulation
from Entropy import Entropy
from Weighted import Weighted
from Mat import Mat
from Edf import Edf

app = Flask(__name__)
cors.init_app(app)

def calculate_complexity(vertex,img_url,file_key):
    #response result
    result = {}

    #downsampling boundary
    complexity_downsamplingboudary = DownsamplingBoudary(vertex,file_key)
    result['DownsamplingBoundary'] = complexity_downsamplingboudary

    #downsampling area
    complexity_downsamplingarea = DownsampingArea(img_url,file_key)
    result['DownsamplingArea'] = complexity_downsamplingarea

    #boundary
    complexity_boundary = Boundary(img_url)
    result['Boundary'] = complexity_boundary

    #triangulation
    complexity_triangulation = Triangulation(vertex,file_key)
    result['Triangulation'] = complexity_triangulation

    #entropy
    complexity_entropy = Entropy(vertex, file_key)
    result['Entropy'] = complexity_entropy

    #MAT
    complexity_mat = Mat(img_url, file_key)
    result['Mat'] = complexity_mat

    #EDF
    complexity_edf = Edf(img_url, file_key)
    result['Edf'] = complexity_edf

    #Weighted
    complexity_weighted = Weighted(vertex)
    result['Weighted'] = complexity_weighted
    #print(result)
    return result
    
class ImageComplexityAPI(MethodView):

    # get, return preload image result
    def get(self):
        file_key1 = "preload1"
        file_key2 = "preload2"
        file_path1 = "./draw/preload1.jpg"
        file_path2 = "./draw/preload2.jpg"
        vertex1 = [(223.35064697265625, 232.00694274902344), (171.35064697265625, 309.00694274902344), (183.35064697265625, 403.00694274902344), 
                   (261.35064697265625, 404.00694274902344), (259.35064697265625, 480.00694274902344), (174.35064697265625, 489.00694274902344), 
                   (170.35064697265625, 603.0069427490234), (297.35064697265625, 612.0069427490234), (449.35064697265625, 604.0069427490234), 
                   (515.3506469726562, 503.00694274902344), (536.3506469726562, 399.00694274902344), (468.35064697265625, 349.00694274902344), 
                   (486.35064697265625, 208.00694274902344), (371.35064697265625, 209.00694274902344), (316.35064697265625, 281.00694274902344)]
        vertex1 = np.array(vertex1)

        vertex2 = [(276.35064697265625, 225.67361068725586), (203.35064697265625, 306.67361068725586), (181.35064697265625, 354.67361068725586), 
                   (234.35064697265625, 385.67361068725586), (177.35064697265625, 475.67361068725586), (171.35064697265625, 488.67361068725586), 
                   (237.35064697265625, 579.6736106872559), (255.35064697265625, 599.6736106872559), (299.35064697265625, 550.6736106872559), 
                   (303.35064697265625, 528.6736106872559), (295.35064697265625, 487.67361068725586), (338.35064697265625, 485.67361068725586), 
                   (355.35064697265625, 512.6736106872559), (369.35064697265625, 455.67361068725586), (379.35064697265625, 427.67361068725586), 
                   (376.35064697265625, 424.67361068725586), (395.35064697265625, 394.67361068725586), (437.35064697265625, 435.67361068725586), 
                   (428.35064697265625, 488.67361068725586), (389.35064697265625, 544.6736106872559), (371.35064697265625, 557.6736106872559), 
                   (339.35064697265625, 586.6736106872559), (341.35064697265625, 606.6736106872559), (413.35064697265625, 644.6736106872559), 
                   (420.35064697265625, 642.6736106872559), (474.35064697265625, 619.6736106872559), (493.35064697265625, 603.6736106872559), 
                   (496.35064697265625, 592.6736106872559), (514.3506469726562, 562.6736106872559), (559.3506469726562, 524.6736106872559), 
                   (574.3506469726562, 515.6736106872559), (597.3506469726562, 515.6736106872559), (620.3506469726562, 473.67361068725586), 
                   (570.3506469726562, 416.67361068725586), (554.3506469726562, 407.67361068725586), (518.3506469726562, 395.67361068725586), 
                   (534.3506469726562, 377.67361068725586), (565.3506469726562, 353.67361068725586), (581.3506469726562, 360.67361068725586), 
                   (596.3506469726562, 364.67361068725586), (616.3506469726562, 370.67361068725586), (640.3506469726562, 356.67361068725586), 
                   (654.3506469726562, 330.67361068725586), (641.3506469726562, 295.67361068725586), (598.3506469726562, 285.67361068725586), 
                   (593.3506469726562, 285.67361068725586), (553.3506469726562, 293.67361068725586), (550.3506469726562, 292.67361068725586), 
                   (546.3506469726562, 240.67361068725586), (583.3506469726562, 194.67361068725586), (614.3506469726562, 160.67361068725586), 
                   (618.3506469726562, 118.67361068725586), (629.3506469726562, 83.67361068725586), (624.3506469726562, 30.67361068725586), 
                   (614.3506469726562, 29.67361068725586), (544.3506469726562, 44.67361068725586), (489.35064697265625, 54.67361068725586), 
                   (488.35064697265625, 54.67361068725586), (399.35064697265625, 23.67361068725586), (391.35064697265625, 48.67361068725586), 
                   (444.35064697265625, 58.67361068725586), (488.35064697265625, 63.67361068725586), (530.3506469726562, 69.67361068725586), 
                   (547.3506469726562, 88.67361068725586), (564.3506469726562, 125.67361068725586), (548.3506469726562, 159.67361068725586), 
                   (541.3506469726562, 176.67361068725586), (508.35064697265625, 219.67361068725586), (501.35064697265625, 228.67361068725586), 
                   (485.35064697265625, 245.67361068725586), (455.35064697265625, 258.67361068725586), (414.35064697265625, 267.67361068725586), 
                   (397.35064697265625, 244.67361068725586), (390.35064697265625, 217.67361068725586), (387.35064697265625, 198.67361068725586), 
                   (346.35064697265625, 198.67361068725586), (324.35064697265625, 198.67361068725586)]
        vertex2 = np.array(vertex2)
        
        response = {}
        complexity1 = calculate_complexity(vertex1,file_path1,file_key1)
        response[file_key1] = complexity1

        complexity2 = calculate_complexity(vertex2,file_path2,file_key2)
        response[file_key2] = complexity2

        return jsonify({
            "message": "Succeed!",
            "data": response
            }), 200

    #post, return input image result
    def post(self):
        data_type = request.form.get('type') or request.json.get('type')
        #print(data_type)
        response = {}
        #select or upload method
        if data_type == 'image':
            files = request.files
            if not files:
                return jsonify({"error": "No File!"}), 400

            try:
                for file_key in files:
                   file = files[file_key]
                   filename = file.name
                   filename = filename + ".jpg"
                   file_path = os.path.join(".\\upload",filename)
                   file.save(file_path)
                   vertex = GetVertex(file_path)
                   #print(vertex)
                   complexity = calculate_complexity(vertex,file_path,file_key)
                   #print(complexity)   
                   response[file_key] = complexity
                print(response)
                return jsonify({
                        "message": "Succeed!",
                        "data": response
                    }), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        #draw method
        elif data_type == "points":
            upload_type = request.form.get('type')
            if not upload_type:
                return jsonify({'error': 'Missing type'}), 400
        
            try:
                for file_key in request.form:
                    print(file_key)
                    if file_key.startswith("file"):
                       polygon = json.loads(request.form.get(file_key))
                       #print(polygon)
                       polygon_points = [(point['x'], point['y']) for point in polygon]
                       print(polygon_points)

                       img_size = (700, 700)  # set image size
                       img = Image.new('RGB', img_size, (0, 0, 0)) 
                       draw = ImageDraw.Draw(img)
            
                    # draw polygon
                       draw.polygon(polygon_points, outline="white", fill="white") 

                       filename = file_key
                       filename = filename + ".jpg"
                       #print(filename)
                       file_path = os.path.join(".\\draw",filename)
                       img.save(file_path)

                       vertex = []
                       for points in polygon_points:
                           vertex.append([points[0],points[1]])
                       vertex = np.array(vertex)
                       print(vertex)
                    #print(vertex)
                       complexity = calculate_complexity(vertex,file_path,file_key)  
                    #print(complexity)  
                       response[file_key] = complexity
                    #print(response)
                return jsonify({
                    "message": "Succeed!",
                    "data": response
                }), 200
            
            except Exception as e:
                return jsonify({"error": str(e)}), 500
                    
            """polygons = request.json.get('points')

            if not polygons:
                return jsonify({"error": "No Points!"}), 400
            
            for i,polygon in enumerate(polygons):
                polygon_points = [(point['x'], point['y']) for point in polygon]
                print(polygon_points)

                img_size = (700, 700)  # set image size
                img = Image.new('RGB', img_size, (0, 0, 0)) 
                draw = ImageDraw.Draw(img)
            
                # 绘制多边形
                draw.polygon(polygon_points, outline="white", fill="white")  
            
                # 生成文件名并保存到指定文件
                filename = 'file' + str(i) + '.jpg'
                image_path = os.path.join('.\\draw', filename)
                img.save(image_path)
                file_key = "file" + str(i)

                vertex = []
                for points in polygon_points:
                    vertex.append([points[0],points[1]])
                vertex = np.array(vertex)
                #print(vertex)
                complexity = calculate_complexity(vertex,image_path,file_key)  
                #print(complexity)  
                response[file_key] = complexity
                #print(response)
            return jsonify({
                    "message": "Succeed!",
                    "data": response
                }), 200"""


image_complexity_view = ImageComplexityAPI.as_view('image_complexity_api')
app.add_url_rule('/api/complexity', view_func=image_complexity_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=5000)