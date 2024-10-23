from flask import Flask, request, jsonify
from flask.views import MethodView
from extension import cors
from PIL import Image,ImageDraw
import os
from GetVertex import GetVertex
from DownsamplingBoundary import DownsamplingBoudary
from DownsamplingArea import DownsampingArea
import numpy as np

app = Flask(__name__)
cors.init_app(app)

def calculate_complexity(vertex,img_url):
    result = {}
    complexity_downsamplingboudary = DownsamplingBoudary(vertex)
    result['DownsamplingBoudary'] = complexity_downsamplingboudary
    complexity_downsamplingarea = DownsampingArea(img_url)
    result['DownsamplingArea'] = complexity_downsamplingarea
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
                   complexity = calculate_complexity(vertex,file_path)
                   print(complexity)   
                   response[file_key] = complexity
                print(response)
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
                #print(polygon_points)

                img_size = (500, 500)  # set image size
                img = Image.new('RGB', img_size, (0, 0, 0)) 
                draw = ImageDraw.Draw(img)
            
                # 绘制多边形
                draw.polygon(polygon_points, outline="white", fill="white")  
            
                # 生成文件名并保存到指定文件
                filename = 'file' + str(i) + '.jpg'
                image_path = os.path.join('.\\draw', filename)
                img.save(image_path)

                vertex = []
                for points in polygon_points:
                    vertex.append([points[0],points[1]])
                vertex = np.array(vertex)
                #print(vertex)
                complexity = calculate_complexity(vertex,image_path)  
                print(complexity)  
                file_key = "file" + str(i)
                #print(file_key)
                response[file_key] = complexity
                print(response)
            return jsonify({
                    "message": "Succeed!",
                    "data": response
                }), 200


image_complexity_view = ImageComplexityAPI.as_view('image_complexity_api')
app.add_url_rule('/api/complexity', view_func=image_complexity_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)