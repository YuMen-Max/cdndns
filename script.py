import os
import random
import requests

# 从环境变量中获取敏感信息
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")
DOMAIN_NAME = os.getenv("DOMAIN_NAME")

# 确保这些变量存在
if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID or not DOMAIN_NAME:
    raise ValueError("缺少必要的环境变量，请检查 GitHub Secrets 配置")

# 生成随机 IP 的函数
def generate_random_ips(base_ip="172.64.229"):
    ips = []
    for _ in range(3):
        random_tail = random.randint(0, 255)
        ips.append(f"{base_ip}.{random_tail}")
    return ips

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

# 删除特定 DNS 记录
def delete_dns_records(records):
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    for record in records:
        if "172.64.229." in record["content"]:  # 匹配 IP 前缀
            delete_url = f"{url}/{record['id']}"
            response = requests.delete(delete_url, headers=headers)
            response.raise_for_status()
            print(f"已删除记录: {record['name']} -> {record['content']}")

# 添加新的 A 记录
def add_a_records(ips):
    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    for ip in ips:
        data = {
            "type": "A",
            "name": DOMAIN_NAME,
            "content": ip,
            "ttl": 86400,  # TTL 设置为 24 小时
            "proxied": False  # 关闭代理
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print(f"已添加记录: {DOMAIN_NAME} -> {ip}")

# 主函数
def main():
    # 生成随机 IP
    random_ips = generate_random_ips()
    print(f"生成的 IP: {random_ips}")

    # 获取现有的 DNS 记录
    dns_records = get_dns_records()

    # 删除匹配的 DNS 记录
    delete_dns_records(dns_records)

    # 添加新的 A 记录
    add_a_records(random_ips)

if __name__ == "__main__":
    main()