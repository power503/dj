import os

secret_value = os.getenv("pushplus_TOKEN")
print("Secret received (not printed): ",secret_value)
with open('gitee_stock_result.log', 'w', encoding='utf-8') as f:
    f.write(secret_value)
