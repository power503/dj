import os

secret_value = os.environ.get("pushplus_TOKEN")
if secret_value:
    # 正常工作
    print("Secret received (not printed): ",secret_value)
    with open('gitee_stock_result.log', 'w', encoding='utf-8') as f:
        f.write(secret_value)
