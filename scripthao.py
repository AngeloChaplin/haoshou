import os
import requests
import datetime
import base64

# GitHub配置
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN_haoshou")
REPO_OWNER = "AngeloChaplin"   # 你的 GitHub 用户名或组织名
REPO_NAME = "haoshou"           # 仓库名
BRANCH = "main"
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

file_name = "kline_K.txt"
file_path = f"logs/{file_name}"  # 远程仓库内的路径

# 获取 Binance K线数据
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

# 查询文件是否存在，获取 SHA
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{file_path}"
r = requests.get(url, headers=HEADERS)
payload = {
    "message": f"Update {file_name}",
    "content": base64.b64encode(content.encode()).decode(),
    "branch": BRANCH
}
if r.status_code == 200:
    sha = r.json()["sha"]
    payload["sha"] = sha

# 上传或更新文件
res_put = requests.put(url, headers=HEADERS, json=payload)
if res_put.status_code in [200, 201]:
    print(f"✅ 文件 {file_name} 上传或更新成功")
else:
    print(f"❌ 文件上传失败: {res_put.text}")
