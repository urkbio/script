import socket
import itertools
import time

def query_whois(domain, server="whois.nic.vg", port=43):
    """
    通过 socket 连接 WHOIS 服务器查询域名信息
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server, port))
        query = domain + "\r\n"
        s.send(query.encode())
        response = b""
        while True:
            data = s.recv(4096)
            if not data:
                break
            response += data
        s.close()
        return response.decode(errors='ignore')
    except Exception as e:
        print(f"查询 {domain} 时发生错误: {e}")
        return ""

def is_available(response):
    """
    根据 WHOIS 返回信息判断域名是否可用
    可根据实际返回信息调整判断关键词
    """
    keywords = ["No match", "NOT FOUND", "No Data Found", "Domain not found"]
    for keyword in keywords:
        if keyword.lower() in response.lower():
            return True
    return False

def main():
    available_domains = []
    # 使用字母 a-z 生成所有两个字符的组合
    characters = 'abcdefghijklmnopqrstuvwxyz'
    
    # 打开文件，写入未注册的域名
    with open("vg.txt", "w", encoding="utf-8") as f:
        for comb in itertools.product(characters, repeat=2):
            domain_name = "".join(comb)
            domain = domain_name + ".vg"
            print(f"正在查询 {domain} ...")
            response = query_whois(domain)
            if response:
                if is_available(response):
                    print(f">>> {domain} 未注册！")
                    available_domains.append(domain)
                    f.write(domain + "\n")
                    f.flush()  # 实时刷新文件内容
                else:
                    print(f">>> {domain} 已注册。")
            else:
                print(f">>> {domain} 查询无返回。")
            time.sleep(2)  # 每次暂停 2 秒以降低被封风险
    
    print("\n查询结束，以下为未注册的域名：")
    for d in available_domains:
        print(d)

if __name__ == '__main__':
    main()
