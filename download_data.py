import requests
import os

url = "https://msmarco.z22.web.core.windows.net/msmarcoranking/msmarco-docs.trec.gz"
# المجلد الذي تريده
folder = "E:/IR_Project_Data/downloads/d4863e4f342982b51b9a8fc668b2d0c0"
file_path = os.path.join(folder, "msmarco-docs.trec.gz")

if not os.path.exists(folder):
    os.makedirs(folder)

file_mode = 'ab' if os.path.exists(file_path) else 'wb'
downloaded_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

headers = {'Range': f'bytes={downloaded_size}-'}

print(f"جاري التحميل/الاستئناف إلى: {file_path}")
response = requests.get(url, headers=headers, stream=True)

with open(file_path, file_mode) as f:
    for chunk in response.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
            print(f"تم تحميل {os.path.getsize(file_path) / (1024*1024):.2f} ميجابايت...")

print("اكتمل التحميل!")