import os

secret_value = os.getenv("pushplus_TOKEN")
if secret_value:
    # 正常工作
    print("Secret received (not printed): ",secret_value)
