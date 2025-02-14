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
    result = {}
    complexity_downsamplingboudary = DownsamplingBoudary(vertex,file_key)
    result['DownsamplingBoundary'] = complexity_downsamplingboudary
    complexity_downsamplingarea = DownsampingArea(img_url,file_key)
    result['DownsamplingArea'] = complexity_downsamplingarea
    complexity_boundary = Boundary(img_url)
    result['Boundary'] = complexity_boundary
    complexity_triangulation = Triangulation(vertex,file_key)
    result['Triangulation'] = complexity_triangulation
    complexity_entropy = Entropy(vertex, file_key)
    result['Entropy'] = complexity_entropy
    complexity_mat = Mat(img_url, file_key)
    result['Mat'] = complexity_mat
    complexity_edf = Edf(img_url, file_key)
    result['Edf'] = complexity_edf
    complexity_weighted = Weighted(vertex)
    result['Weighted'] = complexity_weighted
    #print(result)
    return result
    
class ImageComplexityAPI(MethodView):

    def get(self):
        file_key1 = "preload1"
        file_key2 = "preload2"
        file_path1 = "./example/file6.jpg"
        file_path2 = "./example/file17.jpg"
        response = {}

        vertex1 = GetVertex(file_path1)
        complexity1 = calculate_complexity(vertex1,file_path1,file_key1)
        response[file_key1] = complexity1

        vertex2 = GetVertex(file_path2)
        complexity2 = calculate_complexity(vertex2,file_path2,file_key2)
        response[file_key2] = complexity2

        return jsonify({
            "message": "Succeed!",
            "data": response
            }), 200

    def post(self):
        data_type = request.form.get('type') or request.json.get('type')
        #print(data_type)
        response = {}
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
                #print(response)
                return jsonify({
                        "message": "Succeed!",
                        "data": response
                    }), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
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
            
                    # 绘制多边形
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
                       #print(vertex)
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
    app.run(debug=True)