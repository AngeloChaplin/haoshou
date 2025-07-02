import os
import requests
import datetime
import base64

# ==== GitHub 配置 ====
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN_haoshou")  # ✅ 使用环境变量
REPO_OWNER = "BorgJennings"
REPO_NAME = "BorgJennings"
BRANCH = "main"

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ==== 文件信息 ====
file_name = "kline_K.txt"
file_path = f"logs/{file_name}"

# ==== 获取 Binance K线数据 ====
binance_url = 'https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDC&interval=3m&limit=1'
res = requests.get(binance_url)
if res.status_code == 200:
    d = res.json()[0]
    current_date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    content = "\n".join([
        current_date,
        str(d[0]), str(d[1]), str(d[2]), str(d[3]), str(d[4]), str(d[6])
    ])
else:
    content = "❌ 无法获取 Binance 数据"

# ==== 获取 GitHub 文件 SHA ====
get_file_api = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
res_get = requests.get(get_file_api, headers=HEADERS)

payload = {
    "message": f"Update {file_name}",
    "content": base64.b64encode(content.encode()).decode(),
    "branch": BRANCH
}

if res_get.status_code == 200:
    sha = res_get.json()["sha"]
    payload["sha"] = sha

# ==== 上传或更新文件 ====
res_put = requests.put(get_file_api, headers=HEADERS, json=payload)

if res_put.status_code in [200, 201]:
    print(f"✅ 文件 {file_name} 上传或更新成功")
else:
    print(f"❌ 文件上传失败: {res_put.text}")
