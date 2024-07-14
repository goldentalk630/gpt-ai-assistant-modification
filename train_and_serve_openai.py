import pandas as pd
import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 讀取金箔產品資料庫的Excel文件
database_path = r'金箔產品資料庫.xlsx'
data = pd.read_excel(database_path)

# 轉換數據為訓練所需的格式
def prepare_training_data(data):
    training_data = []
    for index, row in data.iterrows():
        product_info = f"產品名稱: {{row['產品名稱']}}, 描述: {{row['描述']}}, 價格: {{row['價格']}}"
        training_data.append({{"prompt": product_info, "completion": row['庫存量']}})
    return training_data

training_data = prepare_training_data(data)

# 訓練OpenAI模型
openai.api_key = 'YOUR_OPENAI_API_KEY'

response = openai.FineTune.create(
  training_file="file-YOUR_FILE_ID",
  model="davinci"
)

print(response)

# 初始化Line Bot API
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 查詢純金箔價格與編號
def query_gold_foil(product_name):
    result = data[data['產品名稱'] == product_name]
    if not result.empty:
        product_info = result.iloc[0]
        return f"產品編號: {{product_info['產品編號']}}, 價格: {{product_info['價格']}}"
    else:
        return "找不到相關的產品資訊。"

# 處理Line訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    if "純金箔" in user_message:
        response_message = query_gold_foil("純金箔")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response_message)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="無法識別您的請求。")
        )

# 此處應包含啟動Web應用程式的相關程式碼，如Flask或其他框架
