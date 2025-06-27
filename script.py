import os
import requests

# 从环境变量中获取敏感信息
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")

# 确保这些变量存在
if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID or not DOMAIN_NAME:
    raise ValueError("缺少必要的环境变量，请检查 GitHub Secrets 配置")

# 获取域名的所有 DNS 记录
def get_dns_records():
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["result"]

# 删除所有 A 记录
def delete_all_a_records(records):
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    for record in records:
        if record["type"] == "A":
            delete_url = f"{url}/{record['id']}"
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            print(f"已删除记录: {record['name']} -> {record['content']}")

# 主函数
def main():
    # 获取现有的 DNS 记录
    dns_records = get_dns_records()

    # 删除所有 A 记录
    delete_all_a_records(dns_records)

if __name__ == "__main__":
    main()