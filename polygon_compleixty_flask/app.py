from flask import Flask, request, jsonify
from flask.views import MethodView
from extension import cors
from PIL import Image,ImageDraw
import io
import os

app = Flask(__name__)
cors.init_app(app)

def calculate_complexity(image):
    return {
        "Downsampling_boudary":{
            "complexity":0,
            "vertex_number":5,
        },
        "Downsampling_area":{
            "complexity":0,
            "area":5
        },
    }
    
class ImageComplexityAPI(MethodView):

    def get(self):
        return jsonify({"message": "This is GET"})

    def post(self):
        print("Request files:", request.files)
        data_type = request.form.get('type') or request.json.get('type')
        if data_type == 'image':
            if 'file' not in request.files:
                return jsonify({"error": "No File!"}), 400

            file = request.files['file']

            try:
                image = Image.open(file.stream)
                result = calculate_complexity(image)        
                return jsonify({
                    "message": "Succeed!",
                    "data": result
                }), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        elif data_type == "points":
            points = request.json.get('points')
            if not points:
                return jsonify({"error": "No Points!"}), 400
            
            print (points)
            polygon_points = [(point['x'], point['y']) for point in points]

            img_size = (500, 500)  # 设置图像大小
            img = Image.new('RGB', img_size, (255, 255, 255))  # 创建白色背景的图像
            draw = ImageDraw.Draw(img)
            
            # 绘制多边形
            draw.polygon(polygon_points, outline="black", fill=None)  # 用黑色描边
            
            # 生成文件名并保存到指定文件夹
            print('ok')
            image_path = os.path.join('.\\example', 'polygon_image.png')
            print(f"Saving image to: {image_path}")
            img.save(image_path)

            result = calculate_complexity(points)
            return jsonify({
                    "message": "Succeed!",
                    "data": result
                }), 200


image_complexity_view = ImageComplexityAPI.as_view('image_complexity_api')
app.add_url_rule('/api/complexity', view_func=image_complexity_view, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)