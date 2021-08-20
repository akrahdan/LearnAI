import requests

poly_url = 'http://127.0.0.1:8000/upload/policy/'
post_data = None
data = {
    'name': 'screen_shot.png',
    'raw_filename': 'screen_shot.png',
    'filetype': 'images/png'
}
r = requests.post(poly_url, json=data)
if r.status_code in range(200, 299):
    print(r.json())
    post_data = r.json()
# key = 'readux-test/screen_shot.png'

print('post-data', post_data)
print('policy', r.status_code)
# file_path = 'screen.png'
# with open(file_path, 'rb') as data:
#     files  = { 'file': data}
#     url = post_data['url']
#     request_data = post_data['fields']
#     key = request_data.get('key')
#     r = requests.post(url, data=request_data, files=files)
#     print('upload', r.status_code)
#     if r.status_code in range(200, 299):
#         data = {
#             'key': key,
#             'uploaded': True
#         }
#         new_r = requests.put(poly_url, json=data)
#         print(new_r.status_code)
    
    