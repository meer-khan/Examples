import requests

url = "http://127.0.0.1:5000/idol_time/"
image_path = r"IMG-0211.jpg"

# Additional data
site_id = "123"
idol_time = "15"

# Prepare the data to be sent
data = {
    "siteID": site_id,
    "idolTime": idol_time
}

files = {'image': open(image_path, 'rb')}

response = requests.post(url, files=files, data=data)

print(response.json())
print(response.status_code)