import requests

# 要上传的图片路径
image_path = "selection/apple-2.gif"

# 目标URL
url = 'http://localhost:5000/api/complexity'

# 打开图片并发送POST请求
with open(image_path, 'rb') as image_file:
    files = {'file': image_file}
    response = requests.post(url, files=files)

# 打印服务器返回的响应
print(response.json())