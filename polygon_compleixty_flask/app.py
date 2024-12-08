from flask import Flask, request, jsonify
from flask.views import MethodView
from extension import cors
from PIL import Image,ImageDraw
import os
import numpy as np

from GetVertex import GetVertex
from DownsamplingBoundary import DownsamplingBoudary
from DownsamplingArea import DownsampingArea
from Boundary import Boundary
from Triangulation import Triangulation
from Entropy import Entropy


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
    #print(result)
    return result
    
class ImageComplexityAPI(MethodView):

    def get(self):
        return jsonify({"message": "This is GET"})

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
            polygons = request.json.get('points')

            if not polygons:
                return jsonify({"error": "No Points!"}), 400
            
            for i,polygon in enumerate(polygons):
                polygon_points = [(point['x'], point['y']) for point in polygon]
                print(polygon_points)

                img_size = (500, 500)  # set image size
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
                }), 200


image_complexity_view = ImageComplexityAPI.as_view('image_complexity_api')
app.add_url_rule('/api/complexity', view_func=image_complexity_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)