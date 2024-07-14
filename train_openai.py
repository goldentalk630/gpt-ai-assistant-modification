
import pandas as pd
import openai

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
